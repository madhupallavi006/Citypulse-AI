import React, { useState, useEffect } from 'react';
import { Map, Layers, RefreshCw, Radio, ShieldAlert } from 'lucide-react';
import { MapContainer, TileLayer, Polyline, Popup, Marker } from 'react-leaflet';
import { getLiveTraffic } from '../services/api';
import L from 'leaflet';

// Fix default Leaflet icon paths in React Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Map 42 Road Corridors to Realistic Lat/Lng Geographic Coordinates
const ROAD_COORDINATES = {
  // 10 NH16 Corridors
  "NH16-01": [[20.2971, 85.8245], [20.3071, 85.8345]],
  "NH16-02": [[20.3071, 85.8345], [20.3171, 85.8445]],
  "NH16-03": [[20.3171, 85.8445], [20.3271, 85.8545]],
  "NH16-04": [[20.3271, 85.8545], [20.3371, 85.8645]],
  "NH16-05": [[20.3371, 85.8645], [20.3471, 85.8745]],
  "NH16-06": [[20.2871, 85.8145], [20.2971, 85.8245]],
  "NH16-07": [[20.2771, 85.8045], [20.2871, 85.8145]],
  "NH16-08": [[20.2671, 85.7945], [20.2771, 85.8045]],
  "NH16-09": [[20.2571, 85.7845], [20.2671, 85.7945]],
  "NH16-10": [[20.2471, 85.7745], [20.2571, 85.7845]],

  // 12 ORR Corridors
  "ORR-01": [[20.2500, 85.8000], [20.2620, 85.8080]],
  "ORR-02": [[20.2620, 85.8080], [20.2740, 85.8160]],
  "ORR-03": [[20.2740, 85.8160], [20.2860, 85.8240]],
  "ORR-04": [[20.2860, 85.8240], [20.2980, 85.8320]],
  "ORR-05": [[20.2980, 85.8320], [20.3100, 85.8400]],
  "ORR-06": [[20.3100, 85.8400], [20.3220, 85.8480]],
  "ORR-07": [[20.3220, 85.8480], [20.3340, 85.8560]],
  "ORR-08": [[20.3340, 85.8560], [20.3460, 85.8640]],
  "ORR-09": [[20.3460, 85.8640], [20.3580, 85.8720]],
  "ORR-10": [[20.3580, 85.8720], [20.3700, 85.8800]],
  "ORR-11": [[20.2380, 85.7920], [20.2500, 85.8000]],
  "ORR-12": [[20.2260, 85.7840], [20.2380, 85.7920]],

  // 10 CBD Corridors
  "CBD-01": [[20.2800, 85.8400], [20.2850, 85.8450]],
  "CBD-02": [[20.2850, 85.8450], [20.2900, 85.8500]],
  "CBD-03": [[20.2900, 85.8500], [20.2950, 85.8550]],
  "CBD-04": [[20.2950, 85.8550], [20.3000, 85.8600]],
  "CBD-05": [[20.3000, 85.8600], [20.3050, 85.8650]],
  "CBD-06": [[20.2750, 85.8350], [20.2800, 85.8400]],
  "CBD-07": [[20.2700, 85.8300], [20.2750, 85.8350]],
  "CBD-08": [[20.2650, 85.8250], [20.2700, 85.8300]],
  "CBD-09": [[20.2600, 85.8200], [20.2650, 85.8250]],
  "CBD-10": [[20.2550, 85.8150], [20.2600, 85.8200]],

  // 10 Metro Corridors
  "METRO-01": [[20.3100, 85.8150], [20.3170, 85.8210]],
  "METRO-02": [[20.3170, 85.8210], [20.3240, 85.8270]],
  "METRO-03": [[20.3240, 85.8270], [20.3310, 85.8330]],
  "METRO-04": [[20.3310, 85.8330], [20.3380, 85.8390]],
  "METRO-05": [[20.3380, 85.8390], [20.3450, 85.8450]],
  "METRO-06": [[20.3030, 85.8090], [20.3100, 85.8150]],
  "METRO-07": [[20.2960, 85.8030], [20.3030, 85.8090]],
  "METRO-08": [[20.2890, 85.7970], [20.2960, 85.8030]],
  "METRO-09": [[20.2820, 85.7910], [20.2890, 85.7970]],
  "METRO-10": [[20.2750, 85.7850], [20.2820, 85.7910]],
};

export default function LiveTraffic() {
  const [trafficData, setTrafficData] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTraffic = async () => {
    try {
      const data = await getLiveTraffic();
      setTrafficData(data.roads || []);
    } catch (err) {
      console.error('Failed to load live traffic:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTraffic();
    const interval = setInterval(fetchTraffic, 10000);
    return () => clearInterval(interval);
  }, []);

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'CRITICAL':
        return '#ef4444'; // Red
      case 'HIGH':
        return '#f97316'; // Orange
      case 'MEDIUM':
        return '#f59e0b'; // Yellow
      case 'LOW':
      default:
        return '#10b981'; // Green
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Map className="w-5 h-5 text-sky-400" />
            Live Traffic Map & OpenStreetMap Telemetry
          </h2>
          <p className="text-xs text-slate-400">Interactive color-coded corridor network with live risk telemetry.</p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="flex items-center space-x-1.5 px-3 py-1 bg-slate-900 border border-slate-800 rounded-full">
            <Radio className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
            <span className="text-slate-300">Live Telemetry Refreshing (10s)</span>
          </div>
          <button
            onClick={fetchTraffic}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition border border-slate-700"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Interactive Leaflet Map Container */}
      <div className="h-[460px] bg-[#111827] border border-slate-800 rounded-xl overflow-hidden relative shadow-lg">
        <MapContainer
          center={[20.2971, 85.8245]}
          zoom={12}
          style={{ height: '100%', width: '100%', backgroundColor: '#0b0f19' }}
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://carto.com/">CARTO</a> & OpenStreetMap'
          />

          {trafficData.map((road) => {
            const coords = ROAD_COORDINATES[road.road_id];
            if (!coords) return null;
            const color = getRiskColor(road.risk_level);

            return (
              <Polyline
                key={road.road_id}
                positions={coords}
                pathOptions={{ color: color, weight: 6, opacity: 0.85 }}
              >
                <Popup className="custom-leaflet-popup">
                  <div className="p-2 bg-slate-900 text-slate-200 text-xs rounded space-y-1 font-sans">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-1">
                      <strong className="text-sky-400 font-mono">{road.road_id}</strong>
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-bold" style={{ backgroundColor: `${color}33`, color: color }}>
                        {road.risk_level} ({road.congestion_risk}/100)
                      </span>
                    </div>
                    <div><span className="text-slate-400">Speed:</span> <strong>{road.average_speed} km/h</strong></div>
                    <div><span className="text-slate-400">Vehicles:</span> <strong>{road.vehicle_count}</strong></div>
                    <div><span className="text-slate-400">Density:</span> <strong>{road.traffic_density}%</strong></div>
                    <div><span className="text-slate-400">Occupancy:</span> <strong>{road.road_occupancy}%</strong></div>
                    <div className="pt-1 text-[11px] text-slate-300 italic">
                      Forecast: {road.congestion_risk > 60 ? 'Bottleneck Expected (+20m)' : 'Stable Flow Expected'}
                    </div>
                  </div>
                </Popup>
              </Polyline>
            );
          })}
        </MapContainer>
      </div>

      {/* Corridor Risk Legend & Table */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-slate-100 text-sm">Monitored Corridor Telemetry Feed</h3>
          <div className="flex items-center space-x-4 text-xs font-mono">
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> LOW (0-30)</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> MEDIUM (31-60)</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-orange-500" /> HIGH (61-80)</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> CRITICAL (81-100)</span>
          </div>
        </div>

        <div className="overflow-x-auto max-h-[300px] overflow-y-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider font-mono sticky top-0">
              <tr>
                <th className="p-3">Corridor ID</th>
                <th className="p-3">Speed (km/h)</th>
                <th className="p-3">Vehicles</th>
                <th className="p-3">Density</th>
                <th className="p-3">Occupancy</th>
                <th className="p-3">Risk Score</th>
                <th className="p-3">Status Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {trafficData.map((road) => {
                const color = getRiskColor(road.risk_level);
                return (
                  <tr key={road.road_id} className="hover:bg-slate-800/40">
                    <td className="p-3 text-sky-400 font-semibold">{road.road_id}</td>
                    <td className="p-3">{road.average_speed}</td>
                    <td className="p-3">{road.vehicle_count}</td>
                    <td className="p-3">{road.traffic_density}%</td>
                    <td className="p-3">{road.road_occupancy}%</td>
                    <td className="p-3 font-bold" style={{ color: color }}>{road.congestion_risk}/100</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold" style={{ backgroundColor: `${color}22`, color: color, border: `1px solid ${color}44` }}>
                        {road.risk_level}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
