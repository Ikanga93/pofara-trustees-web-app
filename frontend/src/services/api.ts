import axios from 'axios';

// Create axios instance with base configuration
export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/token/refresh/', {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials: { email: string; password: string }) =>
    api.post('auth/token/', credentials),
  
  register: (userData: { email: string; password: string; first_name: string; last_name: string; phone_number?: string }) =>
    api.post('auth/user/register/', userData),
  
  refresh: (refreshToken: string) =>
    api.post('auth/token/refresh/', { refresh: refreshToken }),
  
  logout: () => api.post('auth/logout/'),
  
  getProfile: () => api.get('auth/user/profile/'),
  
  updateProfile: (data: any) => api.patch('auth/user/profile/update/', data),
};

// Projects API
export const projectsAPI = {
  getProjects: (params?: any) => api.get('projects/', { params }),
  getProject: (id: string) => api.get(`projects/${id}/`),
  createProject: (data: any) => api.post('projects/', data),
  updateProject: (id: string, data: any) => api.patch(`projects/${id}/`, data),
  deleteProject: (id: string) => api.delete(`projects/${id}/`),
};

// Inspectors API
export const inspectorsAPI = {
  getInspectors: (params?: any) => api.get('inspectors/', { params }),
  getInspector: (id: number) => api.get(`inspectors/${id}/`),
  bookInspector: (data: any) => api.post('inspectors/book/', data),
};

// Messages API
export const messagesAPI = {
  getConversations: () => api.get('messaging/conversations/'),
  getMessages: (conversationId: number) => api.get(`messaging/conversations/${conversationId}/messages/`),
  sendMessage: (data: any) => api.post('messaging/', data),
};

export default api; 