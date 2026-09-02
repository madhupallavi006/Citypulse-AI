import React from 'react';
import { 
  LayoutDashboard, 
  Map, 
  TrendingUp, 
  AlertTriangle, 
  Ambulance, 
  Cpu, 
  BarChart3, 
  MessageSquareCode,
  ShieldCheck
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'live-traffic', label: 'Live Traffic', icon: Map },
    { id: 'predictions', label: 'Prediction Center', icon: TrendingUp },
    { id: 'incidents', label: 'Incidents & Anomalies', icon: AlertTriangle },
    { id: 'emergency', label: 'Emergency Corridor', icon: Ambulance },
    { id: 'digital-twin', label: 'Digital Twin', icon: Cpu },
    { id: 'explainable-ai', label: 'Explainable AI', icon: BarChart3 },
    { id: 'ai-assistant', label: 'AI Assistant & RAG', icon: MessageSquareCode },
  ];

  return (
    <aside className="w-64 bg-[#0d1322] border-r border-slate-800 flex flex-col justify-between p-4 shrink-0">
      <div>
        <div className="px-3 py-2 text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
          Control Center Modules
        </div>

        <nav className="mt-2 space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                  isActive
                    ? 'bg-sky-600/20 text-sky-400 border border-sky-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Safety Banner Footnote */}
      <div className="p-3 bg-slate-900/80 border border-slate-800 rounded-lg text-[11px] text-slate-400 space-y-1">
        <div className="flex items-center space-x-1.5 text-amber-400 font-semibold">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Safety Boundary</span>
        </div>
        <p className="leading-tight text-slate-500">
          Simulated recommendations only. Does not control physical infrastructure.
        </p>
      </div>
    </aside>
  );
}
