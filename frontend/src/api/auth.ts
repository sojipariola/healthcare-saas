import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1'; // Use your backend URL

export async function login(email: string, password: string) {
  const response = await axios.post(`${API_URL}/auth/token/`, { email, password });
  return response.data;
}

export async function getCurrentUser(token: string) {
  const response = await axios.get(`${API_URL}/auth/me/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}