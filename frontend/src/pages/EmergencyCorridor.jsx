import React, { useState, useEffect } from 'react';
import { Ambulance, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { getEmergencyStatus, simulateEmergency } from '../services/api';

export default function EmergencyCorridor() {
  const [emergencyData, setEmergencyData] = useState(null);
  const [vehicleType, setVehicleType] = useState('Ambulance');
  const [origin, setOrigin] = useState('Central City Hospital');
  const [destination, setDestination] = useState('Trauma Care Gate 2');

  useEffect(() => {
    getEmergencyStatus().then(setEmergencyData);
  }, []);

  const handleSimulate = async () => {
    const res = await simulateEmergency({ vehicle_type: vehicleType, origin, destination });
    setEmergencyData({ active_corridor: res.corridor_details });
  };

  const corridor = emergencyData?.active_corridor;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <Ambulance className="w-5 h-5 text-emerald-400" />
          Emergency Green Corridor Simulation
        </h2>
        <p className="text-xs text-slate-400">
          Simulate priority green light waves & dedicated emergency routing for critical vehicles.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Emergency Status Card */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Active Green Corridor Priority
            </span>
            <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-mono border border-emerald-500/30">
              SIMULATED ONLY
            </span>
          </div>

          {corridor && (
            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400">Vehicle Type:</span>
                <span className="ml-2 font-semibold text-white">{corridor.type || corridor.vehicle_type}</span>
              </div>
              <div>
                <span className="text-slate-400">Origin:</span>
                <span className="ml-2 font-mono text-slate-200">{corridor.origin}</span>
              </div>
              <div>
                <span className="text-slate-400">Destination:</span>
                <span className="ml-2 font-mono text-slate-200">{corridor.destination}</span>
              </div>
              <div>
                <span className="text-slate-400">Priority Route:</span>
                <p className="mt-1 font-mono text-sky-400 bg-slate-900 p-2 rounded border border-slate-800">
                  {corridor.recommended_route || corridor.route}
                </p>
              </div>
              <div className="flex justify-between pt-2 border-t border-slate-800 font-mono text-xs">
                <span>Est. Response Time: <strong className="text-emerald-400">{corridor.estimated_eta_mins} mins</strong></span>
                <span>Time Saved: <strong className="text-sky-400">{corridor.time_saved_mins} mins</strong></span>
              </div>
            </div>
          )}
        </div>

        {/* Trigger Emergency Simulation Controls */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm">Simulate Emergency Corridor</h3>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Emergency Vehicle Type</label>
              <select 
                value={vehicleType} 
                onChange={(e) => setVehicleType(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
              >
                <option value="Ambulance">Ambulance</option>
                <option value="Fire Truck">Fire Truck</option>
                <option value="Police Dispatch">Police Dispatch</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Origin Point</label>
              <input 
                type="text" 
                value={origin} 
                onChange={(e) => setOrigin(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Destination</label>
              <input 
                type="text" 
                value={destination} 
                onChange={(e) => setDestination(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
              />
            </div>

            <button 
              onClick={handleSimulate}
              className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg transition"
            >
              Dispatch Simulated Green Corridor
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
