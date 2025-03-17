import axios from 'axios';

// Use environment variable for API URL, with fallback for local development
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001';

export const testRegister = async (email: string, password: string) => {
  try {
    console.log(`Testing registration with ${email} to ${apiUrl}/register`);
    const response = await axios.post(`${apiUrl}/register`, { email, password });
    console.log('Registration response:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('Registration error:', error.response?.data || error.message);
    throw error;
  }
};

export const testLogin = async (email: string, password: string) => {
  try {
    console.log(`Testing login with ${email} to ${apiUrl}/token`);
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await axios.post(`${apiUrl}/token`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    console.log('Login response:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('Login error:', error.response?.data || error.message);
    throw error;
  }
};

export const testHealth = async () => {
  try {
    console.log(`Testing health endpoint at ${apiUrl}/health`);
    const response = await axios.get(`${apiUrl}/health`);
    console.log('Health response:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('Health check error:', error.response?.data || error.message);
    throw error;
  }
}; 