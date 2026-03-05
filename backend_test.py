#!/usr/bin/env python3
"""
Backend API Testing Suite
Tests all critical endpoints for the crypto intelligence platform
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

class CryptoIntelAPITester:
    def __init__(self, base_url="https://exchange-system-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.results = []

    def log_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED - {details}")
            self.failed_tests.append({
                "test": test_name,
                "error": details,
                "response": response_data
            })
        
        self.results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def test_api_call(self, endpoint: str, method: str = "GET", expected_status: int = 200, 
                     data: Dict = None, test_name: str = None) -> tuple:
        """Generic API test method"""
        if not test_name:
            test_name = f"{method} {endpoint}"
        
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                self.log_result(test_name, False, f"Unsupported method: {method}")
                return False, {}

            success = response.status_code == expected_status
            
            if success:
                try:
                    response_data = response.json()
                    self.log_result(test_name, True, f"Status: {response.status_code}")
                    return True, response_data
                except json.JSONDecodeError:
                    self.log_result(test_name, True, f"Status: {response.status_code} (No JSON)")
                    return True, {}
            else:
                error_msg = f"Expected {expected_status}, got {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('detail', '')}"
                except:
                    error_msg += f" - {response.text[:200]}"
                
                self.log_result(test_name, False, error_msg, response.text[:500])
                return False, {}

        except requests.exceptions.Timeout:
            self.log_result(test_name, False, "Request timeout (30s)")
            return False, {}
        except requests.exceptions.ConnectionError:
            self.log_result(test_name, False, "Connection error - service may be down")
            return False, {}
        except Exception as e:
            self.log_result(test_name, False, f"Unexpected error: {str(e)}")
            return False, {}

    def test_health_endpoint(self):
        """Test backend health endpoint"""
        print("\n🔍 Testing Backend Health...")
        success, data = self.test_api_call("/api/health", test_name="Backend Health Check")
        
        if success:
            # Verify health response structure
            if data.get('ok') is True:
                self.log_result("Health Response Structure", True, "ok:true found")
            else:
                self.log_result("Health Response Structure", False, "ok:true not found in response")
        
        return success

    def test_exchange_providers_health(self):
        """Test exchange providers health"""
        print("\n🔍 Testing Exchange Providers Health...")
        success, data = self.test_api_call("/api/exchange/providers/health", 
                                         test_name="Exchange Providers Health")
        
        if success:
            providers = data.get('providers', {})
            
            # Check HyperLiquid
            hyperliquid = providers.get('hyperliquid', {})
            if hyperliquid.get('healthy'):
                self.log_result("HyperLiquid Health", True, "Provider is healthy")
            else:
                self.log_result("HyperLiquid Health", False, f"Provider unhealthy: {hyperliquid}")
            
            # Check Coinbase
            coinbase = providers.get('coinbase', {})
            if coinbase.get('healthy'):
                self.log_result("Coinbase Health", True, "Provider is healthy")
            else:
                self.log_result("Coinbase Health", False, f"Provider unhealthy: {coinbase}")
        
        return success

    def test_exchange_ticker_hyperliquid(self):
        """Test HyperLiquid ticker endpoint"""
        print("\n🔍 Testing HyperLiquid Ticker...")
        success, data = self.test_api_call("/api/exchange/ticker?venue=hyperliquid&symbol=BTC", 
                                         test_name="HyperLiquid BTC Ticker")
        
        if success:
            # Verify ticker data structure
            required_fields = ['last', 'instrument_id']
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                self.log_result("HyperLiquid Ticker Data", True, f"Price: {data.get('last')}")
            else:
                self.log_result("HyperLiquid Ticker Data", False, f"Missing fields: {missing_fields}")
        
        return success

    def test_exchange_ticker_coinbase(self):
        """Test Coinbase ticker endpoint"""
        print("\n🔍 Testing Coinbase Ticker...")
        success, data = self.test_api_call("/api/exchange/ticker?venue=coinbase&symbol=BTC-USD", 
                                         test_name="Coinbase BTC-USD Ticker")
        
        if success:
            # Verify ticker data structure
            required_fields = ['last', 'instrument_id']
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                self.log_result("Coinbase Ticker Data", True, f"Price: {data.get('last')}")
            else:
                self.log_result("Coinbase Ticker Data", False, f"Missing fields: {missing_fields}")
        
        return success

    def test_token_price_aggregation(self):
        """Test token price aggregation across venues"""
        print("\n🔍 Testing Token Price Aggregation...")
        success, data = self.test_api_call("/api/exchange/token/ETH/price", 
                                         test_name="ETH Price Aggregation")
        
        if success:
            # Verify aggregation data
            if 'prices' in data and len(data['prices']) > 0:
                self.log_result("Price Aggregation Data", True, 
                              f"Found {len(data['prices'])} venue prices, avg: {data.get('average_price')}")
            else:
                self.log_result("Price Aggregation Data", False, "No price data found")
        
        return success

    def test_intel_stats(self):
        """Test intel statistics endpoint"""
        print("\n🔍 Testing Intel Statistics...")
        success, data = self.test_api_call("/api/intel/stats", 
                                         test_name="Intel Statistics")
        
        if success:
            collections = data.get('collections', {})
            if collections:
                stats_msg = f"Collections: {len(collections)} types"
                for key, count in collections.items():
                    stats_msg += f", {key}: {count}"
                self.log_result("Intel Collections Data", True, stats_msg)
            else:
                self.log_result("Intel Collections Data", False, "No collections data found")
        
        return success

    def test_intel_curated_activity(self):
        """Test intel curated activity feed"""
        print("\n🔍 Testing Intel Curated Activity...")
        success, data = self.test_api_call("/api/intel/curated/activity", 
                                         test_name="Intel Curated Activity")
        
        if success:
            items = data.get('items', [])
            if items:
                self.log_result("Activity Feed Data", True, f"Found {len(items)} activity items")
                
                # Check item structure
                first_item = items[0]
                required_fields = ['type', 'name']
                missing_fields = [field for field in required_fields if field not in first_item]
                
                if not missing_fields:
                    self.log_result("Activity Item Structure", True, f"Type: {first_item.get('type')}")
                else:
                    self.log_result("Activity Item Structure", False, f"Missing fields: {missing_fields}")
            else:
                self.log_result("Activity Feed Data", False, "No activity items found")
        
        return success

    def test_intel_investors(self):
        """Test intel investors endpoint"""
        print("\n🔍 Testing Intel Investors...")
        success, data = self.test_api_call("/api/intel/investors", 
                                         test_name="Intel Investors")
        
        if success:
            items = data.get('items', [])
            total = data.get('total', 0)
            self.log_result("Investors Data", True, f"Found {len(items)} items, total: {total}")
        
        return success

    def test_intel_unlocks(self):
        """Test intel unlocks endpoint"""
        print("\n🔍 Testing Intel Unlocks...")
        success, data = self.test_api_call("/api/intel/unlocks", 
                                         test_name="Intel Unlocks")
        
        if success:
            items = data.get('items', [])
            count = data.get('count', 0)
            self.log_result("Unlocks Data", True, f"Found {count} unlock events")
        
        return success

    def test_proxy_status(self):
        """Test proxy status endpoint"""
        print("\n🔍 Testing Proxy Status...")
        success, data = self.test_api_call("/api/intel/admin/proxy/status", 
                                         test_name="Proxy Status")
        
        if success:
            configured = data.get('configured', False)
            total = data.get('total', 0)
            enabled = data.get('enabled', 0)
            self.log_result("Proxy Configuration", True, 
                          f"Configured: {configured}, Total: {total}, Enabled: {enabled}")
        
        return success

    def test_add_proxy(self):
        """Test adding a proxy"""
        print("\n🔍 Testing Add Proxy...")
        proxy_data = {
            "server": "http://test-proxy.example.com:8080",
            "username": "testuser",
            "password": "testpass",
            "priority": 1
        }
        
        success, data = self.test_api_call("/api/intel/admin/proxy/add", 
                                         method="POST",
                                         data=proxy_data,
                                         test_name="Add Test Proxy")
        
        if success:
            proxy_id = data.get('id')
            if proxy_id:
                self.log_result("Proxy Creation", True, f"Created proxy ID: {proxy_id}")
                # Store proxy ID for cleanup
                self.test_proxy_id = proxy_id
                return True, proxy_id
            else:
                self.log_result("Proxy Creation", False, "No proxy ID returned")
        
        return success, None

    def test_proxy_enable_disable(self, proxy_id):
        """Test enabling and disabling proxy"""
        if not proxy_id:
            return False
            
        print("\n🔍 Testing Proxy Enable/Disable...")
        
        # Test disable
        success1, _ = self.test_api_call(f"/api/intel/admin/proxy/{proxy_id}/disable", 
                                       method="POST",
                                       test_name="Disable Proxy")
        
        # Test enable
        success2, _ = self.test_api_call(f"/api/intel/admin/proxy/{proxy_id}/enable", 
                                       method="POST",
                                       test_name="Enable Proxy")
        
        return success1 and success2

    def test_proxy_connectivity(self):
        """Test proxy connectivity"""
        print("\n🔍 Testing Proxy Connectivity...")
        success, data = self.test_api_call("/api/intel/admin/proxy/test", 
                                         method="POST",
                                         test_name="Test Proxy Connectivity")
        
        if success:
            results = data.get('results', [])
            if results:
                self.log_result("Proxy Test Results", True, f"Tested {len(results)} proxies")
                for result in results:
                    proxy_id = result.get('id', 'N/A')
                    tests = result.get('tests', [])
                    success_count = sum(1 for test in tests if test.get('success'))
                    self.log_result(f"Proxy {proxy_id} Tests", True, 
                                  f"{success_count}/{len(tests)} tests passed")
            else:
                self.log_result("Proxy Test Results", False, "No test results returned")
        
        return success

    def test_remove_proxy(self, proxy_id):
        """Test removing a proxy"""
        if not proxy_id:
            return False
            
        print("\n🔍 Testing Remove Proxy...")
        success, _ = self.test_api_call(f"/api/intel/admin/proxy/{proxy_id}", 
                                      method="DELETE",
                                      test_name="Remove Test Proxy")
        return success

    def test_clear_all_proxies(self):
        """Test clearing all proxies"""
        print("\n🔍 Testing Clear All Proxies...")
        success, _ = self.test_api_call("/api/intel/admin/proxy/clear", 
                                      method="POST",
                                      test_name="Clear All Proxies")
        return success

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Crypto Intelligence API Test Suite")
        print(f"📡 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Initialize proxy ID tracker
        self.test_proxy_id = None
        
        # Core health tests
        self.test_health_endpoint()
        
        # Exchange provider tests
        self.test_exchange_providers_health()
        self.test_exchange_ticker_hyperliquid()
        self.test_exchange_ticker_coinbase()
        self.test_token_price_aggregation()
        
        # Intel module tests
        self.test_intel_stats()
        self.test_intel_curated_activity()
        self.test_intel_investors()
        self.test_intel_unlocks()
        
        # Proxy management tests
        print("\n🔧 PROXY MANAGEMENT TESTS")
        print("-" * 40)
        
        # Test initial proxy status
        self.test_proxy_status()
        
        # Test adding a proxy
        success, proxy_id = self.test_add_proxy()
        
        # Test proxy operations if proxy was created
        if success and proxy_id:
            self.test_proxy_enable_disable(proxy_id)
            self.test_proxy_connectivity()
            self.test_remove_proxy(proxy_id)
        
        # Test status after operations
        self.test_proxy_status()
        
        # Test clear all (cleanup)
        self.test_clear_all_proxies()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"❌ Tests Failed: {len(self.failed_tests)}/{self.tests_run}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for failure in self.failed_tests:
                print(f"  • {failure['test']}: {failure['error']}")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test runner"""
    tester = CryptoIntelAPITester()
    
    try:
        success = tester.run_all_tests()
        
        # Save results to file
        results_file = "/app/test_reports/backend_test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_tests": tester.tests_run,
                "passed_tests": tester.tests_passed,
                "failed_tests": len(tester.failed_tests),
                "success_rate": (tester.tests_passed/tester.tests_run*100) if tester.tests_run > 0 else 0,
                "results": tester.results,
                "failures": tester.failed_tests
            }, f, indent=2)
        
        print(f"\n📄 Results saved to: {results_file}")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())