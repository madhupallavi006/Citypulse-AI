import React, { useState, useEffect } from 'react';
import { HelpCircle, BarChart2, Lightbulb, Sparkles, SlidersHorizontal, ShieldCheck } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function ExplainableAI() {
  const [selectedRoad, setSelectedRoad] = useState('NH16-03');
  const [explanationData, setExplanationData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchExplanation = async (roadId) => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE_URL}/api/traffic/explain/${roadId}`);
      setExplanationData(res.data.explanation);
    } catch (err) {
      console.error('Failed to load XAI explanation:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExplanation(selectedRoad);
  }, [selectedRoad]);

  const featureImportance = explanationData?.feature_importance || [];
  const counterfactual = explanationData?.counterfactual_analysis;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-indigo-400" />
            Explainable AI (XAI) Risk Decomposition
          </h2>
          <p className="text-xs text-slate-400">
            Feature contribution breakdown & counterfactual reasoning for ML predictions.
          </p>
        </div>

        {/* Target Corridor Picker */}
        <div className="flex items-center space-x-2">
          <label className="text-xs text-slate-400 font-mono">Target Corridor:</label>
          <select 
            value={selectedRoad} 
            onChange={(e) => setSelectedRoad(e.target.value)}
            className="bg-[#131b2e] border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-sky-400 font-mono font-bold focus:outline-none"
          >
            <option value="NH16-01">NH16-01 (Express North)</option>
            <option value="NH16-03">NH16-03 (Express Central)</option>
            <option value="ORR-03">ORR-03 (Outer Ring Link)</option>
            <option value="CBD-02">CBD-02 (Downtown Boulevard)</option>
            <option value="METRO-05">METRO-05 (Metro Avenue)</option>
          </select>
        </div>
      </div>

      {explanationData && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Feature Importance Bar Chart */}
          <div className="lg:col-span-2 bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-indigo-400" /> Feature Importance Contribution (%)
              </h3>
              <span className="text-xs font-mono text-indigo-300 px-2 py-0.5 bg-indigo-500/10 rounded border border-indigo-500/30">
                Risk Score: {explanationData.predicted_risk_score}/100 ({explanationData.risk_level})
              </span>
            </div>

            <div className="h-[260px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={featureImportance} layout="vertical" margin={{ left: 40, right: 30, top: 10, bottom: 10 }}>
                  <XAxis type="number" domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 10 }} unit="%" />
                  <YAxis type="category" dataKey="feature" stroke="#94a3b8" tick={{ fontSize: 11 }} width={160} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }}
                    formatter={(val) => [`${val}%`, 'Contribution']}
                  />
                  <Bar dataKey="contribution" radius={[0, 6, 6, 0]}>
                    {featureImportance.map((entry, idx) => (
                      <Cell key={idx} fill={idx === 0 ? '#6366f1' : idx === 1 ? '#38bdf8' : '#64748b'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Natural Language Explanation & Counterfactual Analysis */}
          <div className="space-y-6">
            {/* Explanation Summary */}
            <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-3">
              <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                <Lightbulb className="w-4 h-4 text-amber-400" /> Natural Language Explanation
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/80 p-3.5 rounded-lg border border-slate-800">
                {explanationData.natural_language_explanation}
              </p>
            </div>

            {/* Counterfactual Analysis */}
            {counterfactual && (
              <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-3">
                <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-emerald-400" /> Counterfactual What-If Analysis
                </h3>
                <div className="space-y-2 text-xs">
                  <div className="font-mono text-sky-300 font-bold bg-slate-900 p-2.5 rounded border border-slate-800">
                    {counterfactual.hypothesis}
                  </div>
                  <p className="text-slate-300 leading-relaxed bg-emerald-500/10 border border-emerald-500/30 p-3 rounded-lg text-emerald-200">
                    {counterfactual.impact_summary}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
