import axios from 'axios';

import {UserSchema} from './schemes';
import BASE_URL from '@/constants';
import {headers} from "next/headers";

const BASE_URL_JWT = `${BASE_URL}/auth`;

const axiosInstance = axios.create({
    baseURL: BASE_URL_JWT,
    withCredentials: true,
    headers: {"Content-Type": "application/x-www-form-urlencoded"},
});

function convert(data) {
    return new URLSearchParams(data).toString();
}

// const isTokenValid = (token: string): boolean => {
//     try {
//         const decoded: DecodedToken = jwtDecode(token);
//         const currentTime = Date.now() / 1000;
//         return decoded.exp > currentTime;
//     } catch (error) {
//         console.error('Error decoding token:', error);
//         return false;
//     }
// };


axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('Axios error:', error);
        return Promise.reject(error);
    }
);


export const register = async (userData: UserSchema) => {
    const response = await axiosInstance.post('/register', convert(userData));
    const data = response.data;
    return data;
};

export const login = async (userData: UserSchema) => {
    const response = await axiosInstance.post("/login/", convert(userData));
    return response.data;
};

export const getCurrentUser = async () => {
    const response = await axiosInstance.get('/user/me/');
    return response.data;
};

export const confirm_email = async (token: string) => {
    await axiosInstance.post(`/confirm-email/?token=${token}`,
    ).then((response) => {
        const data = response.data;
        return data;
    });
};