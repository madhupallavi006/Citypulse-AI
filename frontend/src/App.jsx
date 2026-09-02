import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';

import Overview from './pages/Overview';
import LiveTraffic from './pages/LiveTraffic';
import Predictions from './pages/Predictions';
import Incidents from './pages/Incidents';
import EmergencyCorridor from './pages/EmergencyCorridor';
import DigitalTwin from './pages/DigitalTwin';
import ExplainableAI from './pages/ExplainableAI';
import AIAssistant from './pages/AIAssistant';

import { getHealth } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [systemOnline, setSystemOnline] = useState(false);

  const checkBackendHealth = async () => {
    try {
      const data = await getHealth();
      setSystemOnline(data.status === 'online');
    } catch (err) {
      setSystemOnline(false);
    }
  };

  useEffect(() => {
    checkBackendHealth();
    const interval = setInterval(checkBackendHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const renderActivePage = () => {
    switch (activeTab) {
      case 'overview':
        return <Overview onNavigate={setActiveTab} />;
      case 'live-traffic':
        return <LiveTraffic />;
      case 'predictions':
        return <Predictions />;
      case 'incidents':
        return <Incidents />;
      case 'emergency':
        return <EmergencyCorridor />;
      case 'digital-twin':
        return <DigitalTwin />;
      case 'explainable-ai':
        return <ExplainableAI />;
      case 'ai-assistant':
        return <AIAssistant />;
      default:
        return <Overview onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col">
      <Header systemOnline={systemOnline} onRefresh={checkBackendHealth} />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        <main className="flex-1 p-6 overflow-y-auto">
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
}
