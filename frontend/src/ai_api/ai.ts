import axios from 'axios';
import BASE_URL from '@/constants';

const axiosAIInstance = axios.create({
    baseURL: `${BASE_URL}/ai`,
    withCredentials: true,
});

axiosAIInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('Axios error:', error);
        return Promise.reject(error);
    }
);

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axiosAIInstance.post('/upload/', formData, {
        responseType: 'text', // Для обработки текстового потока
    });

    return response.data;
};

// Для потоковой обработки с использованием Fetch API
export const uploadFileStream = async (file: File, onChunk: (chunk: string) => void) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${BASE_URL}/ai/upload`, {
            method: 'POST',
            credentials: 'include',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
            throw new Error('Failed to get response reader');
        }

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            onChunk(chunk);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
};