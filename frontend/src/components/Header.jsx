import React, { useState, useEffect } from 'react';
import { Activity, Radio, Cpu, RefreshCw, Zap, CloudRain, Ambulance, Users } from 'lucide-react';
import axios from 'axios';

export default function Header({ systemOnline, onRefresh }) {
  const [time, setTime] = useState(new Date().toLocaleTimeString());
  const [activeScenario, setActiveScenario] = useState('');

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  const triggerDemo = async (scenarioId, name) => {
    try {
      await axios.post(`http://localhost:8000/api/demo/trigger/${scenarioId}`);
      setActiveScenario(name);
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error('Failed to trigger demo scenario:', err);
    }
  };

  return (
    <header className="bg-[#0f172a] border-b border-slate-800 px-6 py-3 space-y-2 text-slate-200">
      <div className="flex items-center justify-between">
        {/* Brand & Subtitle */}
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-sky-500/10 border border-sky-500/30 rounded-lg text-sky-400">
            <Activity className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-bold text-lg text-white tracking-wide">CITYPULSE AI</h1>
              <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 font-semibold border border-sky-500/30">
                PREDICTIVE ORCHESTRATION PLATFORM
              </span>
            </div>
            <p className="text-xs text-slate-400">AI-Powered Intelligent Urban Traffic Management & Congestion Prevention</p>
          </div>
        </div>

        {/* Center Status Indicators */}
        <div className="hidden lg:flex items-center space-x-6 text-xs font-mono">
          <div className="flex items-center space-x-2">
            <Radio className="w-4 h-4 text-emerald-400 animate-pulse" />
            <span className="text-slate-400">Telemetry:</span>
            <span className="text-emerald-400 font-semibold">100% SIMULATED FEED</span>
          </div>
          <div className="flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-sky-400" />
            <span className="text-slate-400">Backend API:</span>
            <span className={`font-semibold ${systemOnline ? 'text-emerald-400' : 'text-amber-400'}`}>
              {systemOnline ? 'ONLINE (FastAPI)' : 'CONNECTING...'}
            </span>
          </div>
        </div>

        {/* Right Controls */}
        <div className="flex items-center space-x-4">
          <div className="text-right hidden sm:block">
            <div className="text-xs font-mono font-medium text-slate-300">{time}</div>
            <div className="text-[10px] text-slate-500">Live Telemetry Synchronized</div>
          </div>

          <button
            onClick={onRefresh}
            className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-300 hover:text-white transition border border-slate-700"
            title="Refresh Data"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-700 text-xs font-mono">
            <span className={`w-2 h-2 rounded-full ${systemOnline ? 'bg-emerald-500 animate-ping' : 'bg-amber-500'}`} />
            <span className="text-slate-300">{systemOnline ? 'READY' : 'STANDBY'}</span>
          </div>
        </div>
      </div>

      {/* One-Click Interactive Demo Scenario Quick Launcher */}
      <div className="flex flex-wrap items-center justify-between pt-1 border-t border-slate-800/60 text-xs font-mono">
        <div className="flex items-center space-x-2 text-slate-400">
          <Zap className="w-3.5 h-3.5 text-amber-400" />
          <span>One-Click Demo Presets:</span>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => triggerDemo('morning_peak', 'Morning Peak')}
            className="px-2.5 py-1 bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded flex items-center gap-1 transition text-[11px]"
          >
            <Users className="w-3 h-3" /> Morning Peak Commute
          </button>
          <button
            onClick={() => triggerDemo('monsoon_disaster', 'Monsoon Heavy Rain')}
            className="px-2.5 py-1 bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 border border-sky-500/30 rounded flex items-center gap-1 transition text-[11px]"
          >
            <CloudRain className="w-3 h-3" /> Monsoon Heavy Rain
          </button>
          <button
            onClick={() => triggerDemo('emergency_ambulance', 'Ambulance Green Corridor')}
            className="px-2.5 py-1 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded flex items-center gap-1 transition text-[11px]"
          >
            <Ambulance className="w-3 h-3" /> Ambulance Green Wave
          </button>
          <button
            onClick={() => triggerDemo('stadium_event', 'Stadium Event Surge')}
            className="px-2.5 py-1 bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 border border-purple-500/30 rounded flex items-center gap-1 transition text-[11px]"
          >
            <Zap className="w-3 h-3" /> Stadium Event Surge
          </button>
        </div>

        {activeScenario && (
          <span className="text-[10px] text-emerald-400 font-bold">
            [Active Preset: {activeScenario}]
          </span>
        )}
      </div>
    </header>
  );
}
