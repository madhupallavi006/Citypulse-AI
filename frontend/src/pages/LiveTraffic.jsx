import React, { useState, useEffect } from 'react';
import { Map, Layers, RefreshCw, Radio } from 'lucide-react';
import { getLiveTraffic } from '../services/api';

export default function LiveTraffic() {
  const [trafficData, setTrafficData] = useState([]);

  useEffect(() => {
    getLiveTraffic().then((data) => setTrafficData(data.roads || []));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Map className="w-5 h-5 text-sky-400" />
            Live Traffic Map & Corridor Telemetry
          </h2>
          <p className="text-xs text-slate-400">Interactive corridor congestion risk and real-time vehicle flow metrics.</p>
        </div>
        <span className="px-3 py-1 bg-sky-500/10 border border-sky-500/30 text-sky-300 text-xs font-mono rounded-full">
          Leaflet Map Component Ready for Phase 5 Integration
        </span>
      </div>

      {/* Simulated Map Container Placeholder */}
      <div className="h-96 bg-[#111827] border border-slate-800 rounded-xl flex flex-col items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:16px_16px]" />
        <div className="z-10 text-center space-y-3 p-6 bg-slate-900/90 border border-slate-800 rounded-xl max-w-md">
          <Layers className="w-10 h-10 text-sky-400 mx-auto animate-bounce" />
          <h3 className="font-semibold text-slate-200">Interactive OpenStreetMap Grid</h3>
          <p className="text-xs text-slate-400">
            Road network coordinates with risk color-coded polylines (LOW / MEDIUM / HIGH / CRITICAL) will render here.
          </p>
        </div>
      </div>

      {/* Road Telemetry Table */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5">
        <h3 className="font-semibold text-slate-100 text-sm mb-4">Corridor Telemetry Data Feed</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider font-mono">
              <tr>
                <th className="p-3">Corridor ID</th>
                <th className="p-3">Corridor Name</th>
                <th className="p-3">Current Speed</th>
                <th className="p-3">Vehicle Count</th>
                <th className="p-3">Density</th>
                <th className="p-3">Congestion Risk</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {trafficData.map((road) => (
                <tr key={road.road_id} className="hover:bg-slate-800/40">
                  <td className="p-3 text-sky-400 font-semibold">{road.road_id}</td>
                  <td className="p-3 font-sans text-slate-200">{road.name}</td>
                  <td className="p-3">{road.current_speed} km/h</td>
                  <td className="p-3">{road.vehicle_count}</td>
                  <td className="p-3">{road.traffic_density}%</td>
                  <td className="p-3 font-bold text-rose-400">{road.congestion_risk}/100</td>
                  <td className="p-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] ${
                      road.risk_level === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    }`}>
                      {road.risk_level}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
