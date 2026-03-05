import React, { useState, useEffect, useCallback } from 'react';
import { 
  Search, BarChart3, Database, Settings, Activity, 
  TrendingUp, Users, Calendar, Layers, Globe, 
  ChevronRight, RefreshCw, ExternalLink, Clock,
  Zap, Target, Shield, Server, Terminal, FileText,
  DollarSign, Unlock, LineChart, Box, Rss, Radio,
  Network, Plus, Trash2, CheckCircle, XCircle, Play, Wifi
} from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

// Design System (FOMO.cx style - Light theme)
const colors = {
  background: '#ffffff',
  surface: '#f7f8fb',
  surfaceHover: '#f0f2f5',
  border: '#e7e9ee',
  borderLight: '#f0f2f5',
  text: '#0f172a',
  textSecondary: '#64748b',
  textMuted: '#94a3b8',
  accent: '#4f46e5',
  accentSoft: '#eef2ff',
  success: '#10b981',
  successSoft: '#ecfdf5',
  warning: '#f59e0b',
  warningSoft: '#fffbeb',
  error: '#ef4444',
  errorSoft: '#fef2f2',
};

// Stat Card Component
function StatCard({ title, value, change, icon: Icon, color = 'accent' }) {
  const isPositive = change && change > 0;
  const colorMap = {
    accent: { bg: colors.accentSoft, icon: colors.accent },
    success: { bg: colors.successSoft, icon: colors.success },
    warning: { bg: colors.warningSoft, icon: colors.warning },
    error: { bg: colors.errorSoft, icon: colors.error }
  };
  const c = colorMap[color] || colorMap.accent;

  return (
    <div 
      data-testid={`stat-card-${title.toLowerCase().replace(/\s/g, '-')}`}
      className="bg-white rounded-2xl p-6 border transition-all hover:shadow-lg hover:-translate-y-0.5"
      style={{ borderColor: colors.border }}
    >
      <div className="flex items-start justify-between mb-4">
        <div 
          className="w-12 h-12 rounded-xl flex items-center justify-center"
          style={{ backgroundColor: c.bg }}
        >
          <Icon size={22} style={{ color: c.icon }} />
        </div>
        {change !== undefined && (
          <span 
            className="text-sm font-medium px-2 py-1 rounded-lg"
            style={{ 
              backgroundColor: isPositive ? colors.successSoft : colors.errorSoft,
              color: isPositive ? colors.success : colors.error
            }}
          >
            {isPositive ? '+' : ''}{change}%
          </span>
        )}
      </div>
      <p className="text-sm mb-1" style={{ color: colors.textSecondary }}>{title}</p>
      <p className="text-3xl font-bold" style={{ color: colors.text }}>{value}</p>
    </div>
  );
}

// Navigation Item
function NavItem({ icon: Icon, label, active, onClick, badge }) {
  return (
    <button
      data-testid={`nav-${label.toLowerCase().replace(/\s/g, '-')}`}
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
        active ? 'font-medium' : ''
      }`}
      style={{ 
        backgroundColor: active ? colors.accentSoft : 'transparent',
        color: active ? colors.accent : colors.textSecondary
      }}
    >
      <Icon size={20} />
      <span className="flex-1 text-left">{label}</span>
      {badge && (
        <span 
          className="text-xs px-2 py-0.5 rounded-full"
          style={{ backgroundColor: colors.accent, color: 'white' }}
        >
          {badge}
        </span>
      )}
    </button>
  );
}

// Section Header
function SectionHeader({ title, action, onAction }) {
  return (
    <div className="flex items-center justify-between mb-4">
      <h2 className="text-lg font-semibold" style={{ color: colors.text }}>{title}</h2>
      {action && (
        <button 
          onClick={onAction}
          className="text-sm flex items-center gap-1 hover:gap-2 transition-all"
          style={{ color: colors.accent }}
        >
          {action} <ChevronRight size={16} />
        </button>
      )}
    </div>
  );
}

// Data Table
function DataTable({ columns, data, loading }) {
  if (loading) {
    return (
      <div className="bg-white rounded-2xl border p-8" style={{ borderColor: colors.border }}>
        <div className="flex items-center justify-center">
          <RefreshCw className="animate-spin" style={{ color: colors.accent }} />
          <span className="ml-2" style={{ color: colors.textSecondary }}>Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border overflow-hidden" style={{ borderColor: colors.border }}>
      <table className="w-full">
        <thead>
          <tr style={{ backgroundColor: colors.surface }}>
            {columns.map((col, i) => (
              <th 
                key={i} 
                className="px-6 py-4 text-left text-sm font-medium"
                style={{ color: colors.textSecondary }}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td 
                colSpan={columns.length} 
                className="px-6 py-12 text-center"
                style={{ color: colors.textMuted }}
              >
                No data available
              </td>
            </tr>
          ) : (
            data.map((row, i) => (
              <tr 
                key={i} 
                className="border-t transition-colors hover:bg-gray-50"
                style={{ borderColor: colors.borderLight }}
              >
                {columns.map((col, j) => (
                  <td key={j} className="px-6 py-4 text-sm" style={{ color: colors.text }}>
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

// System Status Badge
function StatusBadge({ status }) {
  const statusStyles = {
    running: { bg: colors.successSoft, color: colors.success, label: 'Running' },
    healthy: { bg: colors.successSoft, color: colors.success, label: 'Healthy' },
    active: { bg: colors.successSoft, color: colors.success, label: 'Active' },
    idle: { bg: colors.warningSoft, color: colors.warning, label: 'Idle' },
    error: { bg: colors.errorSoft, color: colors.error, label: 'Error' },
    offline: { bg: colors.surface, color: colors.textMuted, label: 'Offline' }
  };
  const s = statusStyles[status] || statusStyles.offline;

  return (
    <span 
      className="px-3 py-1 rounded-full text-xs font-medium inline-flex items-center gap-1"
      style={{ backgroundColor: s.bg, color: s.color }}
    >
      <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: s.color }} />
      {s.label}
    </span>
  );
}

// Search Input
function SearchInput({ value, onChange, placeholder }) {
  return (
    <div className="relative">
      <Search 
        size={20} 
        className="absolute left-4 top-1/2 -translate-y-1/2"
        style={{ color: colors.textMuted }}
      />
      <input
        data-testid="search-input"
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-12 pr-4 py-3 rounded-xl border transition-all focus:outline-none focus:ring-2"
        style={{ 
          borderColor: colors.border,
          backgroundColor: colors.surface,
          color: colors.text
        }}
      />
    </div>
  );
}

// Main Dashboard Component
function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [searchQuery, setSearchQuery] = useState('');
  const [stats, setStats] = useState(null);
  const [exchangeHealth, setExchangeHealth] = useState([]);
  const [trustScores, setTrustScores] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch dashboard data
  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    try {
      const [healthRes, statsRes, trustRes, engineRes] = await Promise.all([
        fetch(`${API_URL}/api/health`).then(r => r.json()).catch(() => ({})),
        fetch(`${API_URL}/api/intel/stats`).then(r => r.json()).catch(() => ({})),
        fetch(`${API_URL}/api/intel/engine/trust/scores`).then(r => r.json()).catch(() => ({ sources: [] })),
        fetch(`${API_URL}/api/intel/engine/status`).then(r => r.json()).catch(() => ({ engines: {} }))
      ]);

      setStats({
        health: healthRes,
        intel: statsRes,
        engines: engineRes.engines || {}
      });
      setTrustScores(trustRes.sources || []);
    } catch (e) {
      console.error('Failed to fetch dashboard data:', e);
    }
    setLoading(false);
  }, []);

  // Fetch exchange providers
  const fetchExchangeData = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/api/exchange/providers/health`);
      const data = await res.json();
      setExchangeHealth(Object.values(data.providers || {}));
    } catch (e) {
      console.error('Failed to fetch exchange data:', e);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
    fetchExchangeData();
  }, [fetchDashboardData, fetchExchangeData]);

  // Render Dashboard View
  const renderDashboard = () => (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Entities" 
          value={stats?.intel?.collections?.entities || '0'}
          icon={Box}
          color="accent"
        />
        <StatCard 
          title="Events" 
          value={stats?.intel?.collections?.events || '0'}
          icon={Activity}
          color="success"
        />
        <StatCard 
          title="Investors" 
          value={stats?.intel?.collections?.investors || '0'}
          icon={Users}
          color="warning"
        />
        <StatCard 
          title="Unlocks" 
          value={stats?.intel?.collections?.unlocks || '0'}
          icon={Unlock}
          color="error"
        />
      </div>

      {/* System Status */}
      <div>
        <SectionHeader title="System Status" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {['correlation', 'trust', 'query'].map(engine => (
            <div 
              key={engine}
              className="bg-white rounded-2xl border p-5 flex items-center justify-between"
              style={{ borderColor: colors.border }}
            >
              <div className="flex items-center gap-3">
                <div 
                  className="w-10 h-10 rounded-xl flex items-center justify-center"
                  style={{ backgroundColor: colors.accentSoft }}
                >
                  <Zap size={18} style={{ color: colors.accent }} />
                </div>
                <div>
                  <p className="font-medium capitalize" style={{ color: colors.text }}>
                    {engine} Engine
                  </p>
                  <p className="text-sm" style={{ color: colors.textSecondary }}>
                    Intelligence Module
                  </p>
                </div>
              </div>
              <StatusBadge status={stats?.engines?.[engine]?.initialized ? 'active' : 'offline'} />
            </div>
          ))}
        </div>
      </div>

      {/* Exchange Providers */}
      <div>
        <SectionHeader title="Exchange Providers" action="View All" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {exchangeHealth.map((provider, i) => (
            <div 
              key={i}
              className="bg-white rounded-2xl border p-5"
              style={{ borderColor: colors.border }}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium capitalize" style={{ color: colors.text }}>
                  {provider.venue}
                </span>
                <StatusBadge status={provider.healthy ? 'healthy' : 'error'} />
              </div>
              <p className="text-sm" style={{ color: colors.textSecondary }}>
                Latency: {provider.latency_ms?.toFixed(0) || 'N/A'}ms
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Source Trust Scores */}
      {trustScores.length > 0 && (
        <div>
          <SectionHeader title="Source Trust Scores" />
          <div className="bg-white rounded-2xl border overflow-hidden" style={{ borderColor: colors.border }}>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 p-6">
              {trustScores.map((source, i) => (
                <div key={i} className="text-center">
                  <div 
                    className="w-16 h-16 mx-auto rounded-2xl flex items-center justify-center mb-2"
                    style={{ 
                      backgroundColor: source.trust_score > 0.8 ? colors.successSoft : 
                                       source.trust_score > 0.6 ? colors.warningSoft : colors.errorSoft
                    }}
                  >
                    <span className="text-lg font-bold" style={{ 
                      color: source.trust_score > 0.8 ? colors.success : 
                             source.trust_score > 0.6 ? colors.warning : colors.error
                    }}>
                      {(source.trust_score * 100).toFixed(0)}
                    </span>
                  </div>
                  <p className="text-sm font-medium capitalize" style={{ color: colors.text }}>
                    {source.source_id}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );

  // Render Explorer View
  const renderExplorer = () => {
    const collections = stats?.intel?.collections || {};
    const explorerData = [
      { name: 'Projects', count: collections.projects || 0, icon: Layers },
      { name: 'Investors', count: collections.investors || 0, icon: Users },
      { name: 'Funding', count: collections.funding || 0, icon: DollarSign },
      { name: 'Unlocks', count: collections.unlocks || 0, icon: Unlock },
      { name: 'Sales', count: collections.sales || 0, icon: TrendingUp },
      { name: 'Events', count: collections.events || 0, icon: Activity },
    ];

    return (
      <div className="space-y-8">
        <SearchInput 
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search entities by name, symbol, or address..."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {explorerData.map((item, i) => (
            <div 
              key={i}
              data-testid={`explorer-${item.name.toLowerCase()}`}
              className="bg-white rounded-2xl border p-6 cursor-pointer transition-all hover:shadow-lg hover:-translate-y-0.5"
              style={{ borderColor: colors.border }}
            >
              <div className="flex items-center gap-4">
                <div 
                  className="w-14 h-14 rounded-2xl flex items-center justify-center"
                  style={{ backgroundColor: colors.accentSoft }}
                >
                  <item.icon size={24} style={{ color: colors.accent }} />
                </div>
                <div>
                  <p className="text-sm" style={{ color: colors.textSecondary }}>{item.name}</p>
                  <p className="text-2xl font-bold" style={{ color: colors.text }}>
                    {item.count.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render Discovery View
  const renderDiscovery = () => (
    <div className="space-y-8">
      <div className="bg-white rounded-2xl border p-8" style={{ borderColor: colors.border }}>
        <div className="text-center mb-8">
          <div 
            className="w-20 h-20 mx-auto rounded-3xl flex items-center justify-center mb-4"
            style={{ backgroundColor: colors.accentSoft }}
          >
            <Globe size={36} style={{ color: colors.accent }} />
          </div>
          <h2 className="text-2xl font-bold mb-2" style={{ color: colors.text }}>
            Network Discovery
          </h2>
          <p style={{ color: colors.textSecondary }}>
            Search for data across the network even if it's not in the database
          </p>
        </div>

        <SearchInput 
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search project, investor, or token..."
        />

        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          {['Project', 'Investor', 'Funding', 'Unlock'].map(type => (
            <button
              key={type}
              className="px-4 py-3 rounded-xl border text-sm font-medium transition-all hover:border-indigo-500"
              style={{ borderColor: colors.border, color: colors.text }}
            >
              Search {type}
            </button>
          ))}
        </div>
      </div>

      <div>
        <SectionHeader title="Seed Sources" />
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {['CryptoRank', 'Dropstab', 'CoinGecko', 'Messari', 'DefiLlama', 'RootData'].map(source => (
            <div 
              key={source}
              className="bg-white rounded-xl border p-4 text-center"
              style={{ borderColor: colors.border }}
            >
              <p className="font-medium" style={{ color: colors.text }}>{source}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Render Developer View
  const renderDeveloper = () => (
    <div className="space-y-8">
      {/* System Health */}
      <div>
        <SectionHeader title="System Health" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div 
            className="bg-white rounded-2xl border p-5"
            style={{ borderColor: colors.border }}
          >
            <div className="flex items-center gap-3 mb-4">
              <Server size={20} style={{ color: colors.accent }} />
              <span className="font-medium" style={{ color: colors.text }}>Backend</span>
            </div>
            <StatusBadge status={stats?.health?.ok ? 'running' : 'error'} />
          </div>
          <div 
            className="bg-white rounded-2xl border p-5"
            style={{ borderColor: colors.border }}
          >
            <div className="flex items-center gap-3 mb-4">
              <Database size={20} style={{ color: colors.accent }} />
              <span className="font-medium" style={{ color: colors.text }}>MongoDB</span>
            </div>
            <StatusBadge status="running" />
          </div>
          <div 
            className="bg-white rounded-2xl border p-5"
            style={{ borderColor: colors.border }}
          >
            <div className="flex items-center gap-3 mb-4">
              <Zap size={20} style={{ color: colors.accent }} />
              <span className="font-medium" style={{ color: colors.text }}>Scheduler</span>
            </div>
            <StatusBadge status="active" />
          </div>
        </div>
      </div>

      {/* API Endpoints */}
      <div>
        <SectionHeader title="API Endpoints" />
        <DataTable 
          columns={[
            { header: 'Endpoint', key: 'endpoint' },
            { header: 'Method', key: 'method', render: (r) => (
              <span 
                className="px-2 py-1 rounded text-xs font-medium"
                style={{ backgroundColor: colors.successSoft, color: colors.success }}
              >
                {r.method}
              </span>
            )},
            { header: 'Description', key: 'description' }
          ]}
          data={[
            { endpoint: '/api/intel/entity/{query}', method: 'GET', description: 'Get entity by any identifier' },
            { endpoint: '/api/intel/entity/{query}/timeline', method: 'GET', description: 'Get entity event timeline' },
            { endpoint: '/api/intel/engine/query/events', method: 'POST', description: 'Query events with filters' },
            { endpoint: '/api/intel/engine/correlation/run', method: 'POST', description: 'Run correlation engine' },
            { endpoint: '/api/intel/engine/trust/scores', method: 'GET', description: 'Get source trust scores' },
            { endpoint: '/api/exchange/ticker', method: 'GET', description: 'Get exchange ticker' },
          ]}
          loading={false}
        />
      </div>

      {/* Logs */}
      <div>
        <SectionHeader title="Recent Activity" />
        <div 
          className="bg-white rounded-2xl border p-6 font-mono text-sm"
          style={{ borderColor: colors.border, backgroundColor: colors.surface }}
        >
          <div className="space-y-2" style={{ color: colors.textSecondary }}>
            <p>[INFO] Entity Intelligence Engine initialized</p>
            <p>[INFO] Query Engine ready</p>
            <p>[INFO] Source Trust Engine loaded 8 default scores</p>
            <p>[INFO] Correlation Engine active</p>
          </div>
        </div>
      </div>
    </div>
  );

  // Render API Docs View
  const [docsLang, setDocsLang] = useState('en');
  const [apiDocs, setApiDocs] = useState([]);
  const [docsCategories, setDocsCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [expandedEndpoint, setExpandedEndpoint] = useState(null);
  const [docsLoading, setDocsLoading] = useState(false);

  // Fetch API documentation
  const fetchApiDocs = useCallback(async () => {
    setDocsLoading(true);
    try {
      const [docsRes, catsRes] = await Promise.all([
        fetch(`${API_URL}/api/docs/?lang=${docsLang}`).then(r => r.json()),
        fetch(`${API_URL}/api/docs/categories`).then(r => r.json())
      ]);
      setApiDocs(docsRes.endpoints || []);
      setDocsCategories(catsRes.categories || []);
    } catch (e) {
      console.error('Failed to fetch API docs:', e);
    }
    setDocsLoading(false);
  }, [docsLang]);

  useEffect(() => {
    if (activeTab === 'api') {
      fetchApiDocs();
    }
  }, [activeTab, docsLang, fetchApiDocs]);

  const renderApiDocs = () => {
    const filteredDocs = selectedCategory 
      ? apiDocs.filter(d => d.category === selectedCategory)
      : apiDocs;

    const methodColors = {
      GET: { bg: colors.successSoft, color: colors.success },
      POST: { bg: colors.accentSoft, color: colors.accent },
      PUT: { bg: colors.warningSoft, color: colors.warning },
      DELETE: { bg: colors.errorSoft, color: colors.error }
    };

    return (
      <div className="space-y-6">
        {/* Header with Language Toggle */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold" style={{ color: colors.text }}>
              {docsLang === 'en' ? 'API Documentation' : 'Документация API'}
            </h2>
            <p style={{ color: colors.textSecondary }}>
              {docsLang === 'en' 
                ? 'Complete API reference. All endpoints return JSON.' 
                : 'Полная справка по API. Все endpoints возвращают JSON.'}
            </p>
          </div>
          
          {/* Language Toggle */}
          <div 
            className="flex rounded-xl overflow-hidden border"
            style={{ borderColor: colors.border }}
          >
            <button
              data-testid="lang-en"
              onClick={() => setDocsLang('en')}
              className="px-4 py-2 text-sm font-medium transition-all"
              style={{ 
                backgroundColor: docsLang === 'en' ? colors.accent : colors.background,
                color: docsLang === 'en' ? 'white' : colors.textSecondary
              }}
            >
              EN
            </button>
            <button
              data-testid="lang-ru"
              onClick={() => setDocsLang('ru')}
              className="px-4 py-2 text-sm font-medium transition-all"
              style={{ 
                backgroundColor: docsLang === 'ru' ? colors.accent : colors.background,
                color: docsLang === 'ru' ? 'white' : colors.textSecondary
              }}
            >
              RU
            </button>
          </div>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCategory(null)}
            className="px-4 py-2 rounded-xl text-sm font-medium transition-all"
            style={{ 
              backgroundColor: !selectedCategory ? colors.accent : colors.surface,
              color: !selectedCategory ? 'white' : colors.textSecondary
            }}
          >
            {docsLang === 'en' ? 'All' : 'Все'}
          </button>
          {docsCategories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className="px-4 py-2 rounded-xl text-sm font-medium transition-all"
              style={{ 
                backgroundColor: selectedCategory === cat.id ? colors.accent : colors.surface,
                color: selectedCategory === cat.id ? 'white' : colors.textSecondary
              }}
            >
              {docsLang === 'en' ? cat.name_en : cat.name_ru}
            </button>
          ))}
        </div>

        {/* Loading State */}
        {docsLoading ? (
          <div className="flex items-center justify-center py-12">
            <RefreshCw className="animate-spin" style={{ color: colors.accent }} />
            <span className="ml-2" style={{ color: colors.textSecondary }}>
              {docsLang === 'en' ? 'Loading...' : 'Загрузка...'}
            </span>
          </div>
        ) : (
          /* Endpoints List */
          <div className="space-y-4">
            {filteredDocs.map((endpoint, i) => {
              const mc = methodColors[endpoint.method] || methodColors.GET;
              const isExpanded = expandedEndpoint === endpoint.endpoint_id;
              
              return (
                <div 
                  key={i}
                  className="bg-white rounded-2xl border overflow-hidden transition-all"
                  style={{ borderColor: colors.border }}
                >
                  {/* Endpoint Header */}
                  <button
                    onClick={() => setExpandedEndpoint(isExpanded ? null : endpoint.endpoint_id)}
                    className="w-full p-5 flex items-center gap-4 text-left hover:bg-gray-50 transition-colors"
                  >
                    <span 
                      className="px-3 py-1 rounded-lg text-xs font-bold"
                      style={{ backgroundColor: mc.bg, color: mc.color }}
                    >
                      {endpoint.method}
                    </span>
                    <code className="text-sm font-medium" style={{ color: colors.accent }}>
                      {endpoint.path}
                    </code>
                    <span className="flex-1 text-sm truncate" style={{ color: colors.textSecondary }}>
                      {endpoint.title}
                    </span>
                    <ChevronRight 
                      size={20} 
                      style={{ 
                        color: colors.textMuted,
                        transform: isExpanded ? 'rotate(90deg)' : 'none',
                        transition: 'transform 0.2s'
                      }} 
                    />
                  </button>

                  {/* Expanded Details */}
                  {isExpanded && (
                    <div 
                      className="px-5 pb-5 border-t"
                      style={{ borderColor: colors.borderLight }}
                    >
                      {/* Description */}
                      <div className="py-4">
                        <p style={{ color: colors.text }}>{endpoint.description}</p>
                      </div>

                      {/* Parameters */}
                      {endpoint.parameters && endpoint.parameters.length > 0 && (
                        <div className="mb-4">
                          <h4 className="text-sm font-semibold mb-3" style={{ color: colors.text }}>
                            {docsLang === 'en' ? 'Parameters' : 'Параметры'}
                          </h4>
                          <div className="space-y-2">
                            {endpoint.parameters.map((param, j) => (
                              <div 
                                key={j}
                                className="flex items-start gap-3 p-3 rounded-xl"
                                style={{ backgroundColor: colors.surface }}
                              >
                                <code className="text-sm font-medium" style={{ color: colors.accent }}>
                                  {param.name}
                                </code>
                                <span 
                                  className="px-2 py-0.5 rounded text-xs"
                                  style={{ backgroundColor: colors.border, color: colors.textSecondary }}
                                >
                                  {param.type}
                                </span>
                                {param.required && (
                                  <span 
                                    className="px-2 py-0.5 rounded text-xs"
                                    style={{ backgroundColor: colors.errorSoft, color: colors.error }}
                                  >
                                    {docsLang === 'en' ? 'required' : 'обязательный'}
                                  </span>
                                )}
                                <span className="text-sm flex-1" style={{ color: colors.textSecondary }}>
                                  {param.description}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Responses */}
                      {endpoint.responses && endpoint.responses.length > 0 && (
                        <div>
                          <h4 className="text-sm font-semibold mb-3" style={{ color: colors.text }}>
                            {docsLang === 'en' ? 'Responses' : 'Ответы'}
                          </h4>
                          {endpoint.responses.map((resp, j) => (
                            <div key={j} className="mb-3">
                              <div className="flex items-center gap-2 mb-2">
                                <span 
                                  className="px-2 py-0.5 rounded text-xs font-medium"
                                  style={{ 
                                    backgroundColor: resp.status_code < 300 ? colors.successSoft : colors.errorSoft,
                                    color: resp.status_code < 300 ? colors.success : colors.error
                                  }}
                                >
                                  {resp.status_code}
                                </span>
                                <span className="text-sm" style={{ color: colors.textSecondary }}>
                                  {resp.description}
                                </span>
                              </div>
                              {resp.example && (
                                <pre 
                                  className="p-4 rounded-xl text-xs overflow-auto"
                                  style={{ backgroundColor: colors.surface, color: colors.text }}
                                >
                                  {JSON.stringify(resp.example, null, 2)}
                                </pre>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  // Intelligence Feed State
  const [feedEvents, setFeedEvents] = useState([]);
  const [feedLoading, setFeedLoading] = useState(false);
  const [feedFilter, setFeedFilter] = useState('all');

  // Fetch feed events
  const fetchFeedEvents = useCallback(async () => {
    setFeedLoading(true);
    try {
      // Fetch from multiple sources
      const [activityRes, trendingRes] = await Promise.all([
        fetch(`${API_URL}/api/intel/curated/activity?limit=20`).then(r => r.json()).catch(() => ({ items: [] })),
        fetch(`${API_URL}/api/intel/curated/trending?limit=10`).then(r => r.json()).catch(() => ({ items: [] }))
      ]);
      
      // Combine and sort by date
      const events = [
        ...(activityRes.items || []).map(e => ({ ...e, type: 'activity' })),
        ...(trendingRes.items || []).map(e => ({ ...e, type: 'trending' }))
      ].sort((a, b) => new Date(b.date || b.ts) - new Date(a.date || a.ts));
      
      setFeedEvents(events.slice(0, 30));
    } catch (e) {
      console.error('Failed to fetch feed:', e);
    }
    setFeedLoading(false);
  }, []);

  useEffect(() => {
    if (activeTab === 'feed') {
      fetchFeedEvents();
    }
  }, [activeTab, fetchFeedEvents]);

  // Render Intelligence Feed
  const renderFeed = () => {
    const eventTypeIcons = {
      funding: { icon: DollarSign, color: colors.success, bg: colors.successSoft, label: 'Funding' },
      unlock: { icon: Unlock, color: colors.warning, bg: colors.warningSoft, label: 'Unlock' },
      listing: { icon: TrendingUp, color: colors.accent, bg: colors.accentSoft, label: 'Listing' },
      sale: { icon: Target, color: colors.error, bg: colors.errorSoft, label: 'Token Sale' },
      activity: { icon: Activity, color: colors.accent, bg: colors.accentSoft, label: 'Activity' },
      trending: { icon: TrendingUp, color: colors.success, bg: colors.successSoft, label: 'Trending' }
    };

    const formatDate = (date) => {
      if (!date) return '';
      const d = new Date(date);
      const now = new Date();
      const diff = now - d;
      
      if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
      return d.toLocaleDateString('en-US', { day: 'numeric', month: 'short' });
    };

    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div 
              className="w-3 h-3 rounded-full animate-pulse"
              style={{ backgroundColor: colors.success }}
            />
            <h2 className="text-xl font-bold" style={{ color: colors.text }}>
              Intelligence Feed
            </h2>
          </div>
          <button
            onClick={fetchFeedEvents}
            className="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
            style={{ backgroundColor: colors.surface, color: colors.textSecondary }}
          >
            <RefreshCw size={16} className={feedLoading ? 'animate-spin' : ''} />
            Refresh
          </button>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-2">
          {['all', 'funding', 'unlock', 'listing', 'trending'].map(filter => (
            <button
              key={filter}
              onClick={() => setFeedFilter(filter)}
              className="px-4 py-2 rounded-xl text-sm font-medium capitalize transition-all"
              style={{ 
                backgroundColor: feedFilter === filter ? colors.accent : colors.surface,
                color: feedFilter === filter ? 'white' : colors.textSecondary
              }}
            >
              {filter}
            </button>
          ))}
        </div>

        {/* Event Stream */}
        <div className="space-y-3">
          {feedLoading ? (
            <div className="flex items-center justify-center py-16">
              <RefreshCw className="animate-spin" size={32} style={{ color: colors.accent }} />
            </div>
          ) : feedEvents.length === 0 ? (
            <div 
              className="bg-white rounded-2xl border p-12 text-center"
              style={{ borderColor: colors.border }}
            >
              <Radio size={48} className="mx-auto mb-4" style={{ color: colors.textMuted }} />
              <p className="font-medium" style={{ color: colors.text }}>No events yet</p>
              <p className="text-sm" style={{ color: colors.textSecondary }}>
                Sync data sources to populate the feed
              </p>
            </div>
          ) : (
            feedEvents
              .filter(e => feedFilter === 'all' || e.type === feedFilter)
              .map((event, i) => {
                const et = eventTypeIcons[event.type] || eventTypeIcons.activity;
                const Icon = et.icon;
                
                return (
                  <div 
                    key={i}
                    className="bg-white rounded-2xl border p-5 transition-all hover:shadow-md"
                    style={{ borderColor: colors.border }}
                  >
                    <div className="flex items-start gap-4">
                      <div 
                        className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                        style={{ backgroundColor: et.bg }}
                      >
                        <Icon size={22} style={{ color: et.color }} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span 
                            className="px-2 py-0.5 rounded text-xs font-medium"
                            style={{ backgroundColor: et.bg, color: et.color }}
                          >
                            {et.label}
                          </span>
                          <span className="text-xs" style={{ color: colors.textMuted }}>
                            {formatDate(event.date || event.ts || event.timestamp)}
                          </span>
                        </div>
                        <p className="font-medium" style={{ color: colors.text }}>
                          {event.name || event.symbol || event.project || 'Unknown'}
                        </p>
                        {event.description && (
                          <p className="text-sm mt-1 truncate" style={{ color: colors.textSecondary }}>
                            {event.description}
                          </p>
                        )}
                        {(event.amount || event.value_usd || event.market_cap) && (
                          <p className="text-sm mt-1 font-medium" style={{ color: colors.success }}>
                            ${((event.amount || event.value_usd || event.market_cap) / 1e6).toFixed(2)}M
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })
          )}
        </div>

        {/* Stats Summary */}
        <div 
          className="bg-white rounded-2xl border p-6"
          style={{ borderColor: colors.border }}
        >
          <h3 className="font-semibold mb-4" style={{ color: colors.text }}>Feed Statistics</h3>
          <div className="grid grid-cols-4 gap-4">
            {Object.entries(
              feedEvents.reduce((acc, e) => {
                acc[e.type] = (acc[e.type] || 0) + 1;
                return acc;
              }, {})
            ).map(([type, count]) => {
              const et = eventTypeIcons[type] || eventTypeIcons.activity;
              return (
                <div key={type} className="text-center">
                  <p className="text-2xl font-bold" style={{ color: et.color }}>{count}</p>
                  <p className="text-sm capitalize" style={{ color: colors.textSecondary }}>{type}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════
  // ADMIN - PROXY MANAGEMENT
  // ═══════════════════════════════════════════════════════════════
  
  const [proxyStatus, setProxyStatus] = useState(null);
  const [proxyLoading, setProxyLoading] = useState(false);
  const [newProxy, setNewProxy] = useState({ server: '', username: '', password: '', priority: 1 });
  const [testResults, setTestResults] = useState(null);
  
  const fetchProxyStatus = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/api/intel/admin/proxy/status`);
      const data = await res.json();
      setProxyStatus(data);
    } catch (err) {
      console.error('Failed to fetch proxy status:', err);
    }
  }, []);
  
  const addProxy = async () => {
    if (!newProxy.server) return;
    setProxyLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/intel/admin/proxy/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newProxy)
      });
      await res.json();
      setNewProxy({ server: '', username: '', password: '', priority: 1 });
      await fetchProxyStatus();
    } catch (err) {
      console.error('Failed to add proxy:', err);
    }
    setProxyLoading(false);
  };
  
  const removeProxy = async (proxyId) => {
    setProxyLoading(true);
    try {
      await fetch(`${API_URL}/api/intel/admin/proxy/${proxyId}`, { method: 'DELETE' });
      await fetchProxyStatus();
    } catch (err) {
      console.error('Failed to remove proxy:', err);
    }
    setProxyLoading(false);
  };
  
  const toggleProxy = async (proxyId, enabled) => {
    setProxyLoading(true);
    try {
      const endpoint = enabled ? 'disable' : 'enable';
      await fetch(`${API_URL}/api/intel/admin/proxy/${proxyId}/${endpoint}`, { method: 'POST' });
      await fetchProxyStatus();
    } catch (err) {
      console.error('Failed to toggle proxy:', err);
    }
    setProxyLoading(false);
  };
  
  const testProxies = async (proxyId = null) => {
    setProxyLoading(true);
    setTestResults(null);
    try {
      const url = proxyId 
        ? `${API_URL}/api/intel/admin/proxy/test?proxy_id=${proxyId}`
        : `${API_URL}/api/intel/admin/proxy/test`;
      const res = await fetch(url, { method: 'POST' });
      const data = await res.json();
      setTestResults(data);
    } catch (err) {
      console.error('Failed to test proxies:', err);
    }
    setProxyLoading(false);
  };
  
  const clearAllProxies = async () => {
    if (!window.confirm('Clear all proxies? Exchanges will use direct connection.')) return;
    setProxyLoading(true);
    try {
      await fetch(`${API_URL}/api/intel/admin/proxy/clear`, { method: 'POST' });
      await fetchProxyStatus();
    } catch (err) {
      console.error('Failed to clear proxies:', err);
    }
    setProxyLoading(false);
  };
  
  useEffect(() => {
    if (activeTab === 'admin') {
      fetchProxyStatus();
    }
  }, [activeTab, fetchProxyStatus]);
  
  const renderAdmin = () => {
    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold" style={{ color: colors.text }}>
              Proxy Management
            </h2>
            <p className="text-sm" style={{ color: colors.textSecondary }}>
              Configure proxies for Binance, Bybit and parsers
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => testProxies()}
              disabled={proxyLoading}
              className="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
              style={{ backgroundColor: colors.accentSoft, color: colors.accent }}
            >
              <Play size={16} />
              Test All
            </button>
            <button
              onClick={fetchProxyStatus}
              disabled={proxyLoading}
              className="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
              style={{ backgroundColor: colors.surface, color: colors.textSecondary }}
            >
              <RefreshCw size={16} className={proxyLoading ? 'animate-spin' : ''} />
              Refresh
            </button>
          </div>
        </div>
        
        {/* Add Proxy Form */}
        <div 
          className="bg-white rounded-2xl border p-6"
          style={{ borderColor: colors.border }}
        >
          <h3 className="font-semibold mb-4 flex items-center gap-2" style={{ color: colors.text }}>
            <Plus size={18} />
            Add Proxy
          </h3>
          <div className="grid grid-cols-4 gap-4">
            <div className="col-span-2">
              <label className="text-sm mb-1 block" style={{ color: colors.textSecondary }}>
                Server URL *
              </label>
              <input
                type="text"
                value={newProxy.server}
                onChange={(e) => setNewProxy({...newProxy, server: e.target.value})}
                placeholder="http://proxy.example.com:8080"
                className="w-full px-4 py-2 rounded-xl border"
                style={{ borderColor: colors.border }}
              />
            </div>
            <div>
              <label className="text-sm mb-1 block" style={{ color: colors.textSecondary }}>
                Username
              </label>
              <input
                type="text"
                value={newProxy.username}
                onChange={(e) => setNewProxy({...newProxy, username: e.target.value})}
                placeholder="optional"
                className="w-full px-4 py-2 rounded-xl border"
                style={{ borderColor: colors.border }}
              />
            </div>
            <div>
              <label className="text-sm mb-1 block" style={{ color: colors.textSecondary }}>
                Password
              </label>
              <input
                type="password"
                value={newProxy.password}
                onChange={(e) => setNewProxy({...newProxy, password: e.target.value})}
                placeholder="optional"
                className="w-full px-4 py-2 rounded-xl border"
                style={{ borderColor: colors.border }}
              />
            </div>
          </div>
          <div className="flex items-center gap-4 mt-4">
            <div>
              <label className="text-sm mb-1 block" style={{ color: colors.textSecondary }}>
                Priority (1 = highest)
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={newProxy.priority}
                onChange={(e) => setNewProxy({...newProxy, priority: parseInt(e.target.value) || 1})}
                className="w-24 px-4 py-2 rounded-xl border"
                style={{ borderColor: colors.border }}
              />
            </div>
            <button
              onClick={addProxy}
              disabled={proxyLoading || !newProxy.server}
              className="mt-5 flex items-center gap-2 px-6 py-2 rounded-xl font-medium transition-all"
              style={{ 
                backgroundColor: newProxy.server ? colors.accent : colors.surface, 
                color: newProxy.server ? 'white' : colors.textMuted 
              }}
            >
              <Plus size={16} />
              Add Proxy
            </button>
          </div>
        </div>
        
        {/* Proxy List */}
        <div 
          className="bg-white rounded-2xl border p-6"
          style={{ borderColor: colors.border }}
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold flex items-center gap-2" style={{ color: colors.text }}>
              <Network size={18} />
              Configured Proxies
            </h3>
            {proxyStatus?.total > 0 && (
              <button
                onClick={clearAllProxies}
                className="text-sm px-3 py-1 rounded-lg"
                style={{ backgroundColor: colors.errorSoft, color: colors.error }}
              >
                Clear All
              </button>
            )}
          </div>
          
          {!proxyStatus || proxyStatus.total === 0 ? (
            <div className="text-center py-8">
              <Wifi size={48} className="mx-auto mb-4" style={{ color: colors.textMuted }} />
              <p className="font-medium" style={{ color: colors.text }}>No proxies configured</p>
              <p className="text-sm" style={{ color: colors.textSecondary }}>
                Add a proxy above to route Binance/Bybit traffic
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {proxyStatus.proxies?.map((proxy) => (
                <div 
                  key={proxy.id}
                  className="flex items-center justify-between p-4 rounded-xl border"
                  style={{ 
                    borderColor: proxy.enabled ? colors.border : colors.errorSoft,
                    backgroundColor: proxy.enabled ? 'white' : colors.surface
                  }}
                >
                  <div className="flex items-center gap-4">
                    <div 
                      className="w-10 h-10 rounded-xl flex items-center justify-center"
                      style={{ 
                        backgroundColor: proxy.enabled ? colors.successSoft : colors.errorSoft 
                      }}
                    >
                      {proxy.enabled ? (
                        <CheckCircle size={20} style={{ color: colors.success }} />
                      ) : (
                        <XCircle size={20} style={{ color: colors.error }} />
                      )}
                    </div>
                    <div>
                      <p className="font-medium" style={{ color: colors.text }}>
                        {proxy.server}
                        {proxy.has_auth && (
                          <span 
                            className="ml-2 text-xs px-2 py-0.5 rounded"
                            style={{ backgroundColor: colors.warningSoft, color: colors.warning }}
                          >
                            Auth
                          </span>
                        )}
                      </p>
                      <p className="text-sm" style={{ color: colors.textSecondary }}>
                        Priority: {proxy.priority} • 
                        Success: {proxy.success_count} • 
                        Errors: {proxy.error_count}
                        {proxy.last_error && (
                          <span style={{ color: colors.error }}> • Last error: {proxy.last_error.slice(0, 50)}...</span>
                        )}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => testProxies(proxy.id)}
                      className="p-2 rounded-lg transition-all"
                      style={{ backgroundColor: colors.surface }}
                      title="Test this proxy"
                    >
                      <Play size={16} style={{ color: colors.accent }} />
                    </button>
                    <button
                      onClick={() => toggleProxy(proxy.id, proxy.enabled)}
                      className="p-2 rounded-lg transition-all"
                      style={{ backgroundColor: proxy.enabled ? colors.warningSoft : colors.successSoft }}
                      title={proxy.enabled ? 'Disable' : 'Enable'}
                    >
                      {proxy.enabled ? (
                        <XCircle size={16} style={{ color: colors.warning }} />
                      ) : (
                        <CheckCircle size={16} style={{ color: colors.success }} />
                      )}
                    </button>
                    <button
                      onClick={() => removeProxy(proxy.id)}
                      className="p-2 rounded-lg transition-all"
                      style={{ backgroundColor: colors.errorSoft }}
                      title="Remove"
                    >
                      <Trash2 size={16} style={{ color: colors.error }} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {/* Test Results */}
        {testResults && (
          <div 
            className="bg-white rounded-2xl border p-6"
            style={{ borderColor: colors.border }}
          >
            <h3 className="font-semibold mb-4 flex items-center gap-2" style={{ color: colors.text }}>
              <Activity size={18} />
              Test Results
            </h3>
            <div className="space-y-4">
              {testResults.results?.map((result, i) => (
                <div key={i} className="border rounded-xl p-4" style={{ borderColor: colors.border }}>
                  <p className="font-medium mb-2" style={{ color: colors.text }}>
                    Proxy #{result.id}: {result.server}
                  </p>
                  <div className="grid grid-cols-3 gap-4">
                    {result.tests?.map((test, j) => (
                      <div 
                        key={j}
                        className="p-3 rounded-lg"
                        style={{ 
                          backgroundColor: test.success ? colors.successSoft : colors.errorSoft 
                        }}
                      >
                        <div className="flex items-center gap-2">
                          {test.success ? (
                            <CheckCircle size={16} style={{ color: colors.success }} />
                          ) : (
                            <XCircle size={16} style={{ color: colors.error }} />
                          )}
                          <span className="font-medium">{test.target}</span>
                        </div>
                        <p className="text-xs mt-1" style={{ color: colors.textSecondary }}>
                          Status: {test.status}
                          {test.error && ` - ${test.error.slice(0, 40)}...`}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Info Box */}
        <div 
          className="rounded-2xl p-6"
          style={{ backgroundColor: colors.accentSoft }}
        >
          <h4 className="font-medium mb-2" style={{ color: colors.accent }}>
            How Proxy Failover Works
          </h4>
          <ul className="text-sm space-y-1" style={{ color: colors.text }}>
            <li>• Proxies are used in priority order (1 = highest)</li>
            <li>• If primary proxy fails, system automatically switches to next</li>
            <li>• Binance and Bybit require proxy due to IP restrictions</li>
            <li>• CryptoRank parser also uses configured proxies</li>
          </ul>
        </div>
      </div>
    );
  };

  // Main content router
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard': return renderDashboard();
      case 'feed': return renderFeed();
      case 'explorer': return renderExplorer();
      case 'discovery': return renderDiscovery();
      case 'developer': return renderDeveloper();
      case 'api': return renderApiDocs();
      case 'admin': return renderAdmin();
      default: return renderDashboard();
    }
  };

  return (
    <div 
      data-testid="intel-dashboard"
      className="min-h-screen flex"
      style={{ backgroundColor: colors.surface }}
    >
      {/* Sidebar */}
      <aside 
        className="w-64 border-r p-6 flex flex-col"
        style={{ backgroundColor: colors.background, borderColor: colors.border }}
      >
        {/* Logo */}
        <div className="mb-8">
          <img 
            src="/logo.svg" 
            alt="FOMO" 
            style={{ height: '46px', width: 'auto' }}
          />
          <p className="text-xs mt-2" style={{ color: colors.textMuted }}>
            Crypto Intelligence Terminal
          </p>
        </div>

        {/* Navigation */}
        <nav className="space-y-1 flex-1">
          <p className="text-xs font-medium uppercase tracking-wider mb-3 px-4" 
             style={{ color: colors.textMuted }}>
            Overview
          </p>
          <NavItem 
            icon={BarChart3} 
            label="Dashboard" 
            active={activeTab === 'dashboard'}
            onClick={() => setActiveTab('dashboard')}
          />
          <NavItem 
            icon={Radio} 
            label="Intel Feed" 
            active={activeTab === 'feed'}
            onClick={() => setActiveTab('feed')}
            badge="Live"
          />
          
          <p className="text-xs font-medium uppercase tracking-wider mt-6 mb-3 px-4"
             style={{ color: colors.textMuted }}>
            Explorer
          </p>
          <NavItem 
            icon={Database} 
            label="Data Explorer" 
            active={activeTab === 'explorer'}
            onClick={() => setActiveTab('explorer')}
          />
          <NavItem 
            icon={Globe} 
            label="Discovery" 
            active={activeTab === 'discovery'}
            onClick={() => setActiveTab('discovery')}
          />

          <p className="text-xs font-medium uppercase tracking-wider mt-6 mb-3 px-4"
             style={{ color: colors.textMuted }}>
            Developer
          </p>
          <NavItem 
            icon={Terminal} 
            label="Console" 
            active={activeTab === 'developer'}
            onClick={() => setActiveTab('developer')}
          />
          <NavItem 
            icon={FileText} 
            label="API Docs" 
            active={activeTab === 'api'}
            onClick={() => setActiveTab('api')}
          />
          
          <p className="text-xs font-medium uppercase tracking-wider mt-6 mb-3 px-4"
             style={{ color: colors.textMuted }}>
            System
          </p>
          <NavItem 
            icon={Network} 
            label="Proxy Admin" 
            active={activeTab === 'admin'}
            onClick={() => setActiveTab('admin')}
          />
        </nav>

        {/* Version */}
        <div 
          className="pt-6 border-t text-sm"
          style={{ borderColor: colors.border, color: colors.textMuted }}
        >
          <p>Version 2.0.0</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-auto">
        {/* Header */}
        <header className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold capitalize" style={{ color: colors.text }}>
              {activeTab === 'api' ? 'API Documentation' : activeTab === 'feed' ? 'Intel Feed' : activeTab}
            </h1>
            <p style={{ color: colors.textSecondary }}>
              {activeTab === 'dashboard' && 'System overview and metrics'}
              {activeTab === 'feed' && 'Real-time crypto intelligence stream'}
              {activeTab === 'explorer' && 'Browse and search intel data'}
              {activeTab === 'discovery' && 'Find data across the network'}
              {activeTab === 'developer' && 'System status and configuration'}
              {activeTab === 'api' && 'Complete API reference'}
              {activeTab === 'admin' && 'Configure proxies for exchange providers'}
            </p>
          </div>
          <button
            data-testid="refresh-btn"
            onClick={fetchDashboardData}
            className="flex items-center gap-2 px-4 py-2 rounded-xl border transition-all hover:shadow-md"
            style={{ borderColor: colors.border, color: colors.text }}
          >
            <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
        </header>

        {/* Content */}
        {loading && !stats ? (
          <div className="flex items-center justify-center h-64">
            <RefreshCw className="animate-spin" size={32} style={{ color: colors.accent }} />
          </div>
        ) : (
          renderContent()
        )}
      </main>
    </div>
  );
}

export default App;
