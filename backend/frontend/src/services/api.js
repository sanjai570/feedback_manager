import axios from 'axios';

const api = axios.create({
    baseURL: '/api/', // Uses Vite proxy
    headers: {
        'Content-Type': 'application/json',
    },
});

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('user');
            window.location.href = '/landing'; // Redirect to landing/login
            return Promise.reject(error);
        }

        let message = 'An error occurred';
        if (error.response?.data) {
            const data = error.response.data;
            if (data.detail) {
                message = data.detail;
            } else if (data.non_field_errors) {
                message = data.non_field_errors[0];
            } else {
                // Handle field errors: { email: ["Error"], password: ["Error"] }
                const fieldErrors = Object.keys(data).map(key => `${key}: ${data[key][0]}`);
                if (fieldErrors.length > 0) {
                    message = fieldErrors.join(', ');
                }
            }
        }
        error.message = message;
        return Promise.reject(error);
    }
);

// Add a request interceptor to include the JWT token
api.interceptors.request.use(
    (config) => {
        const user = JSON.parse(localStorage.getItem('user'));

        // Skip auth for reset password endpoints to avoid 401 if old token exists
        if (config.url.includes('reset-password')) {
            return config;
        }

        if (user && user.access) {
            config.headers.Authorization = `Bearer ${user.access}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const userApi = {
    getAll: (status) => api.get(`users/${status ? `?status=${status}` : ''}`),
    getById: (id) => api.get(`users/${id}/`),
    login: (email, password) => api.post('users/login/', { email, password }),
    getMe: () => api.get('users/me/'),
    create: (data) => api.post('users/', data),
    update: (id, data) => api.put(`users/${id}/`, data),
    delete: (id) => api.delete(`users/${id}/`),
};

export const resourceApi = {
    getAll: () => api.get('resources/'),
    getById: (id) => api.get(`resources/${id}/`),
    create: (data) => api.post('resources/', data),
    update: (id, data) => api.put(`resources/${id}/`, data),
    delete: (id) => api.delete(`resources/${id}/`),
};

export const bookingApi = {
    getAll: () => api.get('bookings/'),
    getById: (id) => api.get(`bookings/${id}/`),
    create: (data) => api.post('bookings/', data),
    updateStatus: (id, status) => api.patch(`bookings/${id}/`, { status }), // Assuming PATCH or PUT support
    delete: (id) => api.delete(`bookings/${id}/`),
};

export default api;
