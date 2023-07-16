import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000, // Adjust the timeout as needed
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;