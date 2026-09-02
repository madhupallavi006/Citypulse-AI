import React, { useState, useEffect } from 'react';
import { AlertTriangle, PlusCircle, ShieldAlert, Cpu, Activity, Clock, CheckCircle2 } from 'lucide-react';
import { getIncidents, createIncident } from '../services/api';
import axios from 'axios';

export default function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [incidentType, setIncidentType] = useState('Accident');
  const [roadId, setRoadId] = useState('NH16-03');
  const [severity, setSeverity] = useState('HIGH');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [incRes, anoRes] = await Promise.all([
        getIncidents(),
        axios.get('http://localhost:8000/api/incidents/anomalies')
      ]);
      setIncidents(incRes.incidents || []);
      setAnomalies(anoRes.data.anomalies || []);
    } catch (err) {
      console.error('Error loading incidents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

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
      loadData();
    } catch (err) {
      setMessage('Failed to inject incident');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Incidents & Isolation Forest Anomaly Detection
          </h2>
          <p className="text-xs text-slate-400">Unsupervised outlier isolation & real-time traffic disruption management.</p>
        </div>
        <span className="px-3 py-1 bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-mono rounded-full flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5" /> Isolation Forest Model Active
        </span>
      </div>

      {/* Main Grid: Incident Form & Anomaly Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Incident Injector Form */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
            <PlusCircle className="w-4 h-4 text-sky-400" /> Inject Simulated Disruption
          </h3>

          {message && (
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs rounded-lg flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" /> {message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Disruption Type</label>
              <select 
                value={incidentType} 
                onChange={(e) => setIncidentType(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200"
              >
                <option value="Accident">Accident</option>
                <option value="Road Construction">Road Construction</option>
                <option value="Rainwater Logging">Rainwater Logging</option>
                <option value="Vehicle Breakdown">Vehicle Breakdown</option>
                <option value="Traffic Signal Failure">Traffic Signal Failure</option>
                <option value="Road Closure">Road Closure</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Target Corridor ID</label>
              <select 
                value={roadId} 
                onChange={(e) => setRoadId(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono"
              >
                <option value="NH16-01">NH16-01 (Express Corridor North)</option>
                <option value="NH16-03">NH16-03 (Express Central)</option>
                <option value="ORR-03">ORR-03 (Outer Ring Junction)</option>
                <option value="CBD-02">CBD-02 (Downtown Boulevard)</option>
                <option value="METRO-05">METRO-05 (Transit Arterial)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Severity</label>
              <select 
                value={severity} 
                onChange={(e) => setSeverity(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200"
              >
                <option value="MEDIUM">MEDIUM</option>
                <option value="HIGH">HIGH</option>
                <option value="CRITICAL">CRITICAL</option>
              </select>
            </div>

            <button 
              type="submit"
              className="w-full py-2.5 bg-amber-600 hover:bg-amber-500 text-white font-semibold rounded-lg transition"
            >
              Simulate Incident & Update Telemetry
            </button>
          </form>
        </div>

        {/* Isolation Forest Anomaly Stream */}
        <div className="lg:col-span-2 bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-rose-400" />
                Isolation Forest Detected Outlier Stream
              </h3>
              <p className="text-xs text-slate-400">Unsupervised outlier scores flagging abnormal speed drops & density spikes.</p>
            </div>
            <span className="text-xs font-mono px-2.5 py-1 bg-slate-900 text-rose-300 rounded border border-slate-800">
              {anomalies.length} Detected
            </span>
          </div>

          <div className="space-y-3 max-h-[380px] overflow-y-auto">
            {anomalies.length > 0 ? (
              anomalies.map((ano) => (
                <div key={ano.id} className="p-3.5 bg-slate-900/80 border border-slate-800 rounded-lg space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-sky-400 font-bold">{ano.road_id}</span>
                      <span className={`px-2 py-0.5 rounded font-mono text-[10px] ${
                        ano.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                      }`}>
                        {ano.severity}
                      </span>
                      <span className="font-semibold text-slate-200">{ano.anomaly_type}</span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-400">Score: {ano.anomaly_score}</span>
                  </div>

                  <div className="text-slate-300">
                    <span className="text-slate-400">Recommended Action:</span> {ano.recommended_investigation}
                  </div>

                  <div className="flex items-center space-x-4 text-[11px] font-mono text-slate-400 pt-1 border-t border-slate-800/60">
                    <span>Speed: <strong className="text-rose-400">{ano.current_speed} km/h</strong></span>
                    <span>Density: <strong className="text-amber-400">{ano.traffic_density}%</strong></span>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-8 text-center text-slate-500 text-xs italic">
                No active traffic anomalies detected by Isolation Forest.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
