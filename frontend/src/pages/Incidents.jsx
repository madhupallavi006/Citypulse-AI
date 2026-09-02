import React, { useState } from 'react';
import { AlertTriangle, PlusCircle } from 'lucide-react';
import { createIncident } from '../services/api';

export default function Incidents() {
  const [incidentType, setIncidentType] = useState('Accident');
  const [roadId, setRoadId] = useState('NH16-03');
  const [severity, setSeverity] = useState('HIGH');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await createIncident({
        type: incidentType,
        road_id: roadId,
        severity: severity,
        duration_mins: 30
      });
      setMessage(res.message);
    } catch (err) {
      setMessage('Failed to inject incident');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          Incidents & Isolation Forest Anomaly Detection
        </h2>
        <p className="text-xs text-slate-400">Simulate and manage hyper-local traffic disruptions.</p>
      </div>

      {/* Incident Creator */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 max-w-xl">
        <h3 className="font-semibold text-slate-100 text-sm mb-4 flex items-center gap-2">
          <PlusCircle className="w-4 h-4 text-sky-400" /> Inject Simulated Traffic Disruption
        </h3>

        {message && (
          <div className="mb-4 p-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs rounded-lg">
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-400 mb-1">Disruption Type</label>
            <select 
              value={incidentType} 
              onChange={(e) => setIncidentType(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
            >
              <option value="Accident">Accident</option>
              <option value="Road Construction">Road Construction</option>
              <option value="Rainwater Logging">Rainwater Logging</option>
              <option value="Vehicle Breakdown">Vehicle Breakdown</option>
              <option value="Traffic Signal Failure">Traffic Signal Failure</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-400 mb-1">Target Corridor ID</label>
            <input 
              type="text" 
              value={roadId} 
              onChange={(e) => setRoadId(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200 font-mono"
            />
          </div>

          <div>
            <label className="block text-slate-400 mb-1">Severity</label>
            <select 
              value={severity} 
              onChange={(e) => setSeverity(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
            >
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
              <option value="CRITICAL">CRITICAL</option>
            </select>
          </div>

          <button 
            type="submit"
            className="w-full py-2 bg-amber-600 hover:bg-amber-500 text-white font-semibold rounded-lg transition"
          >
            Simulate Incident
          </button>
        </form>
      </div>
    </div>
  );
}
