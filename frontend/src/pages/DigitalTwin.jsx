import React, { useState } from 'react';
import { Cpu, Play, CloudRain, Users, ShieldAlert, Sparkles, Sliders, AlertTriangle } from 'lucide-react';
import { runScenarioSimulation } from '../services/api';

export default function DigitalTwin() {
  const [rainSeverity, setRainSeverity] = useState(0);
  const [demandMultiplier, setDemandMultiplier] = useState(1.0);
  const [signalOverrideSec, setSignalOverrideSec] = useState(0);
  const [closedRoad, setClosedRoad] = useState('');
  const [scenarioResult, setScenarioResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRunSimulation = async () => {
    setLoading(true);
    try {
      const closedRoadsList = closedRoad ? [closedRoad] : [];
      const res = await runScenarioSimulation({
        rain_severity: rainSeverity,
        demand_multiplier: demandMultiplier,
        closed_roads: closedRoadsList,
        signal_override_sec: signalOverrideSec,
        transit_surge_factor: 1.0
      });
      setScenarioResult(res.digital_twin_scenario);
    } catch (err) {
      console.error('Scenario simulation failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const baseline = scenarioResult?.baseline;
  const scenario = scenarioResult?.scenario;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-purple-400" />
            Digital Twin & What-If Scenario Modeler
          </h2>
          <p className="text-xs text-slate-400">
            Simulate weather disruptions, sports event demand surges, and road closures in real time.
          </p>
        </div>
        <span className="px-3 py-1 bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-mono rounded-full flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5" /> What-If Neural Engine Ready
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scenario Controls Panel */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-5">
          <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
            <Sliders className="w-4 h-4 text-sky-400" /> Interactive Scenario Parameters
          </h3>

          {/* Rain Intensity */}
          <div className="space-y-2 text-xs">
            <div className="flex justify-between text-slate-300">
              <span className="flex items-center gap-1.5"><CloudRain className="w-3.5 h-3.5 text-sky-400" /> Rain Intensity</span>
              <span className="font-mono text-sky-400 font-bold">{rainSeverity}%</span>
            </div>
            <input 
              type="range" 
              min="0" 
              max="100" 
              value={rainSeverity} 
              onChange={(e) => setRainSeverity(Number(e.target.value))}
              className="w-full accent-sky-500 bg-slate-900 h-1.5 rounded cursor-pointer"
            />
          </div>

          {/* Traffic Demand Multiplier */}
          <div className="space-y-2 text-xs">
            <div className="flex justify-between text-slate-300">
              <span className="flex items-center gap-1.5"><Users className="w-3.5 h-3.5 text-amber-400" /> Traffic Demand Multiplier</span>
              <span className="font-mono text-amber-400 font-bold">{demandMultiplier.toFixed(1)}x</span>
            </div>
            <input 
              type="range" 
              min="1.0" 
              max="3.0" 
              step="0.1"
              value={demandMultiplier} 
              onChange={(e) => setDemandMultiplier(Number(e.target.value))}
              className="w-full accent-amber-500 bg-slate-900 h-1.5 rounded cursor-pointer"
            />
          </div>

          {/* Signal Timing Override */}
          <div className="space-y-2 text-xs">
            <div className="flex justify-between text-slate-300">
              <span>Signal Green Phase Override</span>
              <span className="font-mono text-emerald-400 font-bold">+{signalOverrideSec}s</span>
            </div>
            <input 
              type="range" 
              min="-15" 
              max="30" 
              step="5"
              value={signalOverrideSec} 
              onChange={(e) => setSignalOverrideSec(Number(e.target.value))}
              className="w-full accent-emerald-500 bg-slate-900 h-1.5 rounded cursor-pointer"
            />
          </div>

          {/* Road Closure Picker */}
          <div className="space-y-2 text-xs">
            <label className="block text-slate-300">Simulate Road Closure</label>
            <select 
              value={closedRoad}
              onChange={(e) => setClosedRoad(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono"
            >
              <option value="">None (All Corridors Open)</option>
              <option value="NH16-03">NH16-03 (Express Central)</option>
              <option value="ORR-03">ORR-03 (Outer Ring Link)</option>
              <option value="CBD-02">CBD-02 (Downtown Boulevard)</option>
            </select>
          </div>

          <button
            onClick={handleRunSimulation}
            disabled={loading}
            className="w-full py-3 bg-purple-600 hover:bg-purple-500 text-white font-semibold rounded-lg transition flex items-center justify-center gap-2"
          >
            <Play className="w-4 h-4" /> {loading ? 'Computing Neural Scenario...' : 'Run Scenario Simulation'}
          </button>
        </div>

        {/* Baseline vs Scenario Dashboard */}
        <div className="lg:col-span-2 space-y-6">
          {scenarioResult ? (
            <>
              {/* Metric Cards Comparison */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                <div className="p-4 bg-[#131b2e] border border-slate-800 rounded-xl space-y-1">
                  <span className="text-xs text-slate-400">Average City Speed</span>
                  <div className="flex items-baseline space-x-2">
                    <span className="text-lg font-bold font-mono text-white">{scenario.avg_city_speed_kmh} km/h</span>
                    <span className="text-xs text-slate-400 font-mono">Baseline: {baseline.avg_city_speed_kmh}</span>
                  </div>
                </div>

                <div className="p-4 bg-[#131b2e] border border-slate-800 rounded-xl space-y-1">
                  <span className="text-xs text-slate-400">Congestion Risk Index</span>
                  <div className="flex items-baseline space-x-2">
                    <span className="text-lg font-bold font-mono text-rose-400">{scenario.congestion_index}/100</span>
                    <span className="text-xs text-slate-400 font-mono">Baseline: {baseline.congestion_index}</span>
                  </div>
                </div>

                <div className="p-4 bg-[#131b2e] border border-slate-800 rounded-xl space-y-1">
                  <span className="text-xs text-slate-400">System Impact Rating</span>
                  <span className="text-lg font-bold font-mono text-amber-400 block">{scenario.system_impact_score}/100</span>
                </div>
              </div>

              {/* Bottleneck Formations */}
              <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-3">
                <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-400" />
                  Simulated Bottleneck Corridors ({scenario.bottlenecks?.length})
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-[180px] overflow-y-auto">
                  {scenario.bottlenecks?.map((b) => (
                    <div key={b.road_id} className="p-3 bg-slate-900 border border-slate-800 rounded-lg text-xs space-y-1">
                      <div className="flex justify-between font-mono">
                        <span className="text-sky-400 font-bold">{b.road_id}</span>
                        <span className="text-rose-400 font-bold">{b.simulated_speed} km/h</span>
                      </div>
                      <div className="text-slate-400 text-[11px]">Primary Cause: {b.cause}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* AI Recommended Countermeasures */}
              <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-3">
                <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-purple-400" /> AI Recommended Countermeasures
                </h3>

                <div className="space-y-2">
                  {scenario.ai_recommended_countermeasures?.map((cm, idx) => (
                    <div key={idx} className="p-3 bg-purple-500/10 border border-purple-500/30 text-purple-200 text-xs rounded-lg flex items-start gap-2">
                      <span className="font-mono font-bold text-purple-400">#{idx + 1}</span>
                      <span>{cm}</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="h-full bg-[#131b2e] border border-slate-800 rounded-xl p-12 text-center text-slate-500 flex flex-col items-center justify-center space-y-3">
              <Cpu className="w-10 h-10 text-slate-600 animate-pulse" />
              <p className="text-sm">Adjust scenario parameters on the left and click "Run Scenario Simulation".</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
