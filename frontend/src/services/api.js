import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export const getTrafficOverview = async () => {
  const response = await api.get('/api/traffic/overview');
  return response.data;
};

export const getLiveTraffic = async () => {
  const response = await api.get('/api/traffic/live');
  return response.data;
};

export const getPredictions = async () => {
  const response = await api.get('/api/traffic/predictions');
  return response.data;
};

export const getIncidents = async () => {
  const response = await api.get('/api/incidents');
  return response.data;
};

export const createIncident = async (payload) => {
  const response = await api.post('/api/incidents', payload);
  return response.data;
};

export const getEmergencyStatus = async () => {
  const response = await api.get('/api/emergency');
  return response.data;
};

export const simulateEmergency = async (payload) => {
  const response = await api.post('/api/emergency', payload);
  return response.data;
};

export const getDigitalTwin = async () => {
  const response = await api.get('/api/simulation/state');
  return response.data;
};

export const runScenarioSimulation = async (payload) => {
  const response = await api.post('/api/simulation/what-if', payload);
  return response.data;
};

export const triggerScenario = async (payload) => {
  const response = await api.post('/api/simulation/override', payload);
  return response.data;
};

export const sendChatMessage = async (message) => {
  const response = await api.post('/api/chat', { message });
  return response.data;
};

export default api;
