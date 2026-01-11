import axios from 'axios';


const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

function getCookie(name: string) {
    if (typeof document === 'undefined') return null;
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift();
    return null;
}

api.interceptors.request.use((config) => {
    const token = getCookie('csrftoken');
    if (token) {
        config.headers['X-CSRFToken'] = token;
    }
    return config;
});

export default api;
