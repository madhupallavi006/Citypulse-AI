import React from 'react';
import { BarChart3, HelpCircle, CheckCircle2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const sampleFeatureImportance = [
  { feature: 'Traffic Density (%)', importance: 32 },
  { feature: 'Speed Drop (km/h)', importance: 24 },
  { feature: 'Rainfall Intensity', importance: 18 },
  { feature: 'Peak Hour Factor', importance: 13 },
  { feature: 'Active Incidents', importance: 9 },
  { feature: 'Signal Cycle Time', importance: 4 },
];

export default function ExplainableAI() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-purple-400" />
          Explainable AI (XAI) & SHAP Interpretability Center
        </h2>
        <p className="text-xs text-slate-400">
          Transparent model feature contributions and natural language prediction rationales.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Feature Importance Bar Chart */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5">
          <h3 className="font-semibold text-slate-100 text-sm mb-1">Feature Contribution Breakdown</h3>
          <p className="text-xs text-slate-400 mb-4">Random Forest / Gradient Boosting SHAP feature impact</p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sampleFeatureImportance} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                <XAxis type="number" stroke="#64748b" fontSize={11} />
                <YAxis dataKey="feature" type="category" stroke="#94a3b8" fontSize={11} width={130} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                <Bar dataKey="importance" name="Contribution (%)" radius={[0, 4, 4, 0]} fill="#a855f7" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Natural Language Explanation Box */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
            <HelpCircle className="w-4 h-4 text-purple-400" />
            Natural Language Explanation Output
          </h3>

          <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg space-y-3 text-xs leading-relaxed">
            <div className="flex items-center space-x-2 font-mono text-purple-300 font-semibold">
              <CheckCircle2 className="w-4 h-4 text-purple-400" />
              <span>Corridor: NH16-01 (Risk Score: 87 / 100)</span>
            </div>

            <p className="text-slate-300">
              "The machine learning model predicted high congestion primarily because 
              <strong className="text-purple-300"> vehicle density increased by +32%</strong> while average 
              corridor speed dropped below 28 km/h. Localized rainwater logging accounted for an 
              additional <strong className="text-purple-300">18% risk inflation</strong>."
            </p>

            <div className="pt-2 border-t border-slate-800 font-mono text-[11px] text-slate-400">
              Model Type: Random Forest Classifier v1.0 | SHAP Value Compatibility Verified
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
