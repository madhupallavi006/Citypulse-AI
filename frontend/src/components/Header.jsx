import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, Cpu, Radio, RefreshCw } from 'lucide-react';

export default function Header({ systemOnline, onRefresh }) {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-16 bg-[#0f172a] border-b border-slate-800 px-6 flex items-center justify-between text-slate-200">
      {/* Brand & Subtitle */}
      <div className="flex items-center space-x-3">
        <div className="p-2 bg-sky-500/10 border border-sky-500/30 rounded-lg text-sky-400">
          <Activity className="w-5 h-5 animate-pulse" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="font-bold text-lg text-white tracking-wide">CITYPULSE AI</h1>
            <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 font-semibold border border-sky-500/30">
              SIMULATION PLATFORM
            </span>
          </div>
          <p className="text-xs text-slate-400">Predictive Urban Traffic Orchestration & Prevention System</p>
        </div>
      </div>

      {/* Center Status Indicators */}
      <div className="hidden md:flex items-center space-x-6 text-xs font-mono">
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
          <div className="text-[10px] text-slate-500">Live Orchestration</div>
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
    </header>
  );
}
