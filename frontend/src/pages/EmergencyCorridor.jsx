import React, { useState, useEffect } from 'react';
import { Ambulance, ShieldAlert, CheckCircle2, Bus, ArrowRight, Zap, Clock } from 'lucide-react';
import { getEmergencyStatus, simulateEmergency } from '../services/api';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function EmergencyCorridor() {
  const [emergencyData, setEmergencyData] = useState(null);
  const [transitData, setTransitData] = useState([]);
  const [vehicleType, setVehicleType] = useState('Ambulance');
  const [origin, setOrigin] = useState('J01');
  const [destination, setDestination] = useState('J08');
  const [loading, setLoading] = useState(true);

  const loadCorridorData = async () => {
    try {
      const [emgRes, transRes] = await Promise.all([
        getEmergencyStatus(),
        axios.get(`${API_BASE_URL}/api/emergency/transit`)
      ]);
      setEmergencyData(emgRes);
      setTransitData(transRes.data.bus_priorities || []);
    } catch (err) {
      console.error('Failed to load emergency corridor status:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCorridorData();
  }, []);

  const handleSimulate = async () => {
    try {
      const res = await simulateEmergency({ vehicle_type: vehicleType, origin, destination });
      setEmergencyData({ active_corridor: res.corridor_details });
    } catch (err) {
      console.error('Simulation failed:', err);
    }
  };

  const corridor = emergencyData?.active_corridor;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Ambulance className="w-5 h-5 text-emerald-400" />
            Emergency Green Corridor & Public Transit Priority
          </h2>
          <p className="text-xs text-slate-400">
            Simulated green light pre-emption wave and bus priority dispatch.
          </p>
        </div>
        <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono rounded-full flex items-center gap-1">
          <Zap className="w-3.5 h-3.5" /> Green Wave Override Active
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Emergency Corridor Panel */}
        <div className="lg:col-span-2 bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Active Emergency Priority Sequence
            </span>
            <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-mono border border-emerald-500/30">
              SIMULATED RECOMMENDATION
            </span>
          </div>

          {corridor && (
            <div className="space-y-4 text-xs">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-900/80 p-3 rounded-lg border border-slate-800 font-mono">
                <div>
                  <span className="text-slate-400 block text-[10px]">Vehicle ID</span>
                  <span className="text-white font-bold">{corridor.vehicle_id || corridor.vehicle_type}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px]">Vehicle Type</span>
                  <span className="text-emerald-400 font-bold">{corridor.vehicle_type}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px]">Est. Response Time</span>
                  <span className="text-emerald-400 font-bold">{corridor.estimated_eta_mins} mins</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px]">Time Saved</span>
                  <span className="text-sky-400 font-bold">{corridor.time_saved_mins} mins</span>
                </div>
              </div>

              <div>
                <span className="text-slate-400 block mb-1">Recommended Emergency Route:</span>
                <p className="font-mono text-sky-300 bg-slate-900 p-2.5 rounded border border-slate-800">
                  {corridor.recommended_route}
                </p>
              </div>

              {/* Intersection Sequence Steps */}
              <div>
                <span className="text-slate-400 block mb-2 font-semibold">Pre-emption Intersection Sequence ({corridor.intersections?.length} Nodes):</span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {corridor.intersections?.map((node) => (
                    <div key={node.intersection_id} className="p-2.5 bg-slate-900/60 border border-slate-800 rounded-lg flex items-center justify-between font-mono">
                      <div className="flex items-center space-x-2">
                        <span className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-[10px] font-bold border border-emerald-500/30">
                          {node.sequence}
                        </span>
                        <div>
                          <span className="font-bold text-slate-200 text-[11px]">{node.intersection_id}</span>
                          <span className="text-slate-400 text-[10px] block font-sans">{node.name}</span>
                        </div>
                      </div>
                      <span className="px-1.5 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded text-[9px]">
                        SIGNAL OVERRIDE
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Dispatch Controls */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
            <Ambulance className="w-4 h-4 text-emerald-400" /> Dispatch Simulated Emergency Vehicle
          </h3>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Emergency Vehicle Type</label>
              <select 
                value={vehicleType} 
                onChange={(e) => setVehicleType(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200"
              >
                <option value="Ambulance">Ambulance (Medical Trauma Dispatch)</option>
                <option value="Fire Truck">Fire Truck (Emergency Response)</option>
                <option value="Police Dispatch">Police Dispatch (Rapid Response)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Origin Node</label>
              <select 
                value={origin} 
                onChange={(e) => setOrigin(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono"
              >
                <option value="J01">J01 (Vani Vihar Square)</option>
                <option value="J04">J04 (Master Canteen Square)</option>
                <option value="J06">J06 (Khandagiri Square)</option>
                <option value="J10">J10 (Fire Station Square)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Destination Node</label>
              <select 
                value={destination} 
                onChange={(e) => setDestination(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono"
              >
                <option value="J08">J08 (KIIT Campus / Trauma Center)</option>
                <option value="J12">J12 (Kalpana Square Hospital)</option>
                <option value="J19">J19 (Infocity Health Zone)</option>
              </select>
            </div>

            <button 
              onClick={handleSimulate}
              className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg transition"
            >
              Simulate Emergency Green Corridor
            </button>
          </div>
        </div>
      </div>

      {/* Public Transport Bus Priority Section */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bus className="w-4 h-4 text-sky-400" />
            <h3 className="font-semibold text-slate-100 text-sm">Public Transport Bus Priority Recommendations</h3>
          </div>
          <span className="text-xs font-mono text-slate-400">Automated Bus Delay Signal Pre-emption</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {transitData.map((bus) => (
            <div key={bus.bus_id} className="p-4 bg-slate-900/80 border border-slate-800 rounded-lg space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-mono text-sky-400 font-bold">{bus.bus_id}</span>
                <span className="px-2 py-0.5 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded font-mono text-[10px]">
                  Delayed: +{bus.delay_mins} mins
                </span>
              </div>

              <div className="text-slate-200 font-semibold">{bus.route_name}</div>
              <div className="text-slate-400 text-[11px]">Location: {bus.current_location}</div>

              <div className="pt-2 border-t border-slate-800 text-[11px]">
                <span className="text-slate-400">Recommended Action:</span>
                <p className="text-emerald-400 font-semibold font-mono mt-0.5">{bus.recommended_action}</p>
                <p className="text-slate-400 mt-1">Est. Delay Reduction: <strong className="text-sky-300">{bus.estimated_delay_reduction_mins} mins</strong></p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
