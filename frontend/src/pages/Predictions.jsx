import React, { useState, useEffect } from 'react';
import { TrendingUp, Clock, AlertCircle } from 'lucide-react';
import { getPredictions } from '../services/api';

export default function Predictions() {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    getPredictions().then((data) => setPredictions(data.predictions || []));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-sky-400" />
          Predictive Congestion Forecast Center
        </h2>
        <p className="text-xs text-slate-400">15–30 Minute Advance ML Prediction Horizon</p>
      </div>

      <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5">
        <h3 className="font-semibold text-slate-100 text-sm mb-4">Predicted High-Risk Corridors</h3>
        <div className="space-y-3">
          {predictions.map((p) => (
            <div key={p.road_id} className="p-4 bg-slate-900/80 border border-slate-800 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center space-x-3">
                  <span className="font-mono text-sm font-bold text-sky-400">{p.road_id}</span>
                  <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 border border-rose-500/30 rounded font-mono">
                    Predicted Risk: {p.predicted_risk}%
                  </span>
                  <span className="text-xs text-slate-400 flex items-center gap-1 font-mono">
                    <Clock className="w-3.5 h-3.5 text-slate-500" /> Horizon: {p.prediction_horizon_mins}m
                  </span>
                </div>
                <p className="text-xs text-slate-300">
                  <span className="text-slate-400">Cause:</span> {p.main_cause}
                </p>
              </div>

              <div className="text-right">
                <div className="text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-lg inline-block">
                  Action: {p.recommended_action}
                </div>
                <div className="text-[11px] text-slate-500 mt-1 font-mono">ML Confidence: {(p.confidence * 100).toFixed(0)}%</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
