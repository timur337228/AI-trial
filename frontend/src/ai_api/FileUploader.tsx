'use client';
import { useState } from 'react';
import { uploadFile, uploadFileStream } from '@/ai_api/ai';

const FileUploader = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [responseText, setResponseText] = useState('');
    const [isStreaming, setIsStreaming] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    // Для обычной загрузки (весь ответ сразу)
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedFile) return;

        setIsLoading(true);
        try {
            const result = await uploadFile(selectedFile);
            setResponseText(result);
        } catch (error) {
            console.error('Upload failed:', error);
            setResponseText('Error during file upload');
        } finally {
            setIsLoading(false);
        }
    };

    // Для потоковой загрузки (обработка чанков)
    const handleStreamSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedFile) return;

        setIsStreaming(true);
        setResponseText('');

        try {
            await uploadFileStream(selectedFile, (chunk) => {
                setResponseText(prev => prev + chunk);
            });
        } catch (error) {
            console.error('Stream error:', error);
            setResponseText('Error during streaming');
        } finally {
            setIsStreaming(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-4">
            <form className="space-y-4">
                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                    className="block w-full file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />

                <div className="flex gap-4">

                    <button
                        type="button"
                        onClick={handleStreamSubmit}
                        disabled={!selectedFile || isStreaming}
                        className="px-4 py-2 bg-green-600 text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isStreaming ? 'Загрузка...' : 'Отправить запрос'}
                    </button>
                </div>
            </form>

            {responseText && (
                <div className="mt-8 p-4 bg-gray-50 rounded-md">
                    <h3 className="text-lg font-semibold mb-2">Ответ от ИИ:</h3>
                    <pre className="whitespace-pre-wrap">{responseText}</pre>
                </div>
            )}
        </div>
    );
};

export default FileUploader;