import React, { useState, useEffect } from 'react';
import KPICard from '../components/KPICard';
import { 
  Car, 
  ShieldAlert, 
  AlertTriangle, 
  Gauge, 
  Activity, 
  Ambulance, 
  TrendingUp,
  MapPin,
  Clock,
  Zap
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { getTrafficOverview, getIncidents } from '../services/api';

const simulatedTrendData = [
  { time: '17:00', riskIndex: 32, speed: 48 },
  { time: '17:15', riskIndex: 40, speed: 42 },
  { time: '17:30', riskIndex: 58, speed: 36 },
  { time: '17:45', riskIndex: 72, speed: 29 },
  { time: '18:00', riskIndex: 87, speed: 22 },
  { time: '18:15', riskIndex: 82, speed: 25 },
  { time: '18:30', riskIndex: 76, speed: 28 },
];

const riskDistributionData = [
  { category: 'LOW (0-30)', count: 24, fill: '#10b981' },
  { category: 'MEDIUM (31-60)', count: 11, fill: '#f59e0b' },
  { category: 'HIGH (61-80)', count: 5, fill: '#f97316' },
  { category: 'CRITICAL (81-100)', count: 2, fill: '#ef4444' },
];

export default function Overview({ onNavigate }) {
  const [metrics, setMetrics] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [overviewData, incidentsData] = await Promise.all([
          getTrafficOverview(),
          getIncidents()
        ]);
        setMetrics(overviewData);
        setIncidents(incidentsData.incidents || []);
      } catch (err) {
        console.error('Failed to load overview data:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner / Announcement */}
      <div className="bg-gradient-to-r from-sky-900/40 via-slate-900 to-indigo-900/30 border border-sky-500/20 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-sky-400 font-semibold text-sm">
            <Zap className="w-4 h-4" />
            <span>PREDICTIVE ACCELERATION ACTIVE</span>
          </div>
          <p className="text-xs text-slate-300 mt-1">
            Analyzing 42 urban road corridors in real time. Predicts potential bottleneck risk 15–30 minutes ahead.
          </p>
        </div>
        <div className="flex space-x-2 shrink-0">
          <button
            onClick={() => onNavigate('live-traffic')}
            className="px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-medium transition"
          >
            Open Traffic Map
          </button>
          <button
            onClick={() => onNavigate('predictions')}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition"
          >
            Prediction Center
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Monitored Roads"
          value={metrics?.total_monitored_roads || 42}
          unit="Corridors"
          subtitle="Full Telemetry Coverage"
          icon={MapPin}
          color="sky"
        />
        <KPICard
          title="Active Vehicles"
          value={metrics?.active_vehicles?.toLocaleString() || '18,450'}
          unit="Units"
          subtitle="Simulated GPS / CCTV feed"
          icon={Car}
          trend="+5.4%"
          color="emerald"
        />
        <KPICard
          title="Critical Risk Corridors"
          value={metrics?.critical_roads || 2}
          unit="Corridors"
          subtitle="Congestion Score > 80"
          icon={ShieldAlert}
          color="rose"
        />
        <KPICard
          title="Average Speed"
          value={metrics?.average_speed_kmh || 34.2}
          unit="km/h"
          subtitle="Citywide Corridor Avg"
          icon={Gauge}
          trend="-3.1 km/h"
          color="amber"
        />
      </div>

      {/* Secondary Metrics Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <KPICard
          title="Active Incidents"
          value={metrics?.active_incidents || 3}
          subtitle="Breakdowns & Rain Logging"
          icon={AlertTriangle}
          color="amber"
        />
        <KPICard
          title="Predicted Congestion Rate"
          value={`${metrics?.predicted_congestion_rate || 14.5}%`}
          subtitle="Next 20 mins forecast"
          icon={TrendingUp}
          color="purple"
        />
        <KPICard
          title="Emergency Vehicles Active"
          value={metrics?.emergency_vehicles_active || 1}
          subtitle="Active Priority Corridors"
          icon={Ambulance}
          color="emerald"
        />
      </div>

      {/* Visualizations Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Congestion Risk Trend Chart */}
        <div className="lg:col-span-2 bg-[#131b2e] border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-semibold text-slate-100 text-sm">Citywide Congestion Risk & Speed Trend</h3>
              <p className="text-xs text-slate-400">15-30 Minute Predictive Model Output vs Current Speed</p>
            </div>
            <span className="text-xs font-mono px-2 py-1 bg-slate-800 text-slate-300 rounded border border-slate-700">
              Live Horizon: +20 mins
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={simulatedTrendData}>
                <defs>
                  <linearGradient id="riskGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0284c7" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#0284c7" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} 
                  labelStyle={{ color: '#94a3b8' }}
                />
                <Area type="monotone" dataKey="riskIndex" name="Congestion Risk Index" stroke="#38bdf8" fillOpacity={1} fill="url(#riskGrad)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Level Distribution Bar Chart */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5">
          <h3 className="font-semibold text-slate-100 text-sm mb-1">Corridor Risk Breakdown</h3>
          <p className="text-xs text-slate-400 mb-4">Risk score distribution across 42 corridors</p>

          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskDistributionData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                <XAxis type="number" stroke="#64748b" fontSize={11} />
                <YAxis dataKey="category" type="category" stroke="#94a3b8" fontSize={10} width={100} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                <Bar dataKey="count" name="Road Count" radius={[0, 4, 4, 0]} fill="#0284c7" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-800 flex justify-between text-xs font-mono text-slate-400">
            <span>LOW: 24 Corridors</span>
            <span className="text-rose-400">CRITICAL: 2 Corridors</span>
          </div>
        </div>
      </div>

      {/* Active Incidents Stream */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <h3 className="font-semibold text-slate-100 text-sm">Active Incident & Disruption Stream</h3>
          </div>
          <button 
            onClick={() => onNavigate('incidents')}
            className="text-xs text-sky-400 hover:underline"
          >
            Manage Incidents &rarr;
          </button>
        </div>

        <div className="space-y-3">
          {incidents.map((inc) => (
            <div 
              key={inc.id}
              className="p-3 bg-slate-900/60 border border-slate-800 rounded-lg flex items-center justify-between text-xs"
            >
              <div className="flex items-center space-x-3">
                <span className={`px-2 py-0.5 rounded font-mono font-semibold text-[10px] ${
                  inc.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                }`}>
                  {inc.severity}
                </span>
                <div>
                  <span className="font-semibold text-slate-200">{inc.type}</span>
                  <span className="text-slate-400 ml-2">on corridor <code className="text-sky-300">{inc.road_id}</code></span>
                </div>
              </div>

              <div className="flex items-center space-x-4 text-slate-400 font-mono text-[11px]">
                <div className="flex items-center space-x-1">
                  <Clock className="w-3.5 h-3.5 text-slate-500" />
                  <span>Reported {inc.reported_time}</span>
                </div>
                <span className="text-slate-300 font-sans bg-slate-800 px-2 py-0.5 rounded">
                  Est. Clear: {inc.estimated_clearance_mins} mins
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
