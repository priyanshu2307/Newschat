import axios from 'axios';

// Base API URL - change this to your backend URL
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API methods
export const createSession = async () => {
  const response = await api.post('/sessions');
  return response.data;
};

export const getSessionHistory = async (sessionId) => {
  const response = await api.get(`/sessions/${sessionId}`);
  return response.data;
};

export const clearSession = async (sessionId) => {
  const response = await api.delete(`/sessions/${sessionId}`);
  return response.data;
};

export const sendMessage = async (sessionId, message) => {
  const response = await api.post(`/sessions/${sessionId}/messages`, { message });
  return response.data;
};

export const getStatus = async () => {
  const response = await api.get('/status');
  return response.data;
};

export default api;