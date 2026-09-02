import React, { useState } from 'react';
import { Cpu, CloudRain, Car, AlertOctagon, Play } from 'lucide-react';
import { triggerScenario } from '../services/api';

export default function DigitalTwin() {
  const [scenario, setScenario] = useState('Heavy Rain');
  const [result, setResult] = useState(null);

  const handleScenarioRun = async (selectedScenario) => {
    const activeScenario = selectedScenario || scenario;
    const res = await triggerScenario({ scenario_name: activeScenario });
    setResult(res);
  };

  const presetScenarios = [
    { name: 'Heavy Rain', icon: CloudRain, color: 'sky' },
    { name: 'Peak Hour Rush', icon: Car, color: 'amber' },
    { name: 'Road Closure', icon: AlertOctagon, color: 'rose' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <Cpu className="w-5 h-5 text-sky-400" />
          Smart City Traffic Digital Twin Simulator
        </h2>
        <p className="text-xs text-slate-400">
          Simulate how traffic congestion propagates across intersections under macro weather and event scenarios.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scenario Controls */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm">Preset Urban Scenarios</h3>

          <div className="space-y-2">
            {presetScenarios.map((s) => {
              const Icon = s.icon;
              return (
                <button
                  key={s.name}
                  onClick={() => {
                    setScenario(s.name);
                    handleScenarioRun(s.name);
                  }}
                  className="w-full p-3 bg-slate-900 border border-slate-800 hover:border-sky-500/40 rounded-lg flex items-center justify-between text-xs text-slate-200 transition"
                >
                  <div className="flex items-center space-x-2">
                    <Icon className="w-4 h-4 text-sky-400" />
                    <span>{s.name}</span>
                  </div>
                  <Play className="w-3.5 h-3.5 text-slate-500" />
                </button>
              );
            })}
          </div>
        </div>

        {/* Output Display */}
        <div className="lg:col-span-2 bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm">Digital Twin Simulation Impact Output</h3>

          {result ? (
            <div className="space-y-3 text-xs bg-slate-900 p-4 rounded-lg border border-slate-800">
              <div className="text-sky-400 font-semibold font-mono">{result.message}</div>
              <div>
                <span className="text-slate-400">Predicted Risk Impact:</span>
                <span className="ml-2 font-mono text-rose-400 font-bold">{result.impact.congestion_score_increase}</span>
              </div>
              <div>
                <span className="text-slate-400">Affected Corridors:</span>
                <div className="flex space-x-2 mt-1">
                  {result.impact.affected_roads.map((r) => (
                    <span key={r} className="px-2 py-0.5 bg-slate-800 text-slate-300 font-mono rounded">
                      {r}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-500 italic">Select a scenario control to observe simulated traffic propagation.</p>
          )}
        </div>
      </div>
    </div>
  );
}
