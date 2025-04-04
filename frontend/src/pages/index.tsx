import { useEffect, useState } from 'react';
import { getCurrentUser } from '@/auth_api/api';
import FileUploader from '@/ai_api/FileUploader';

export default function AIPage() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [authError, setAuthError] = useState(false);

    useEffect(() => {
        const checkAuthentication = async () => {
            try {
                await getCurrentUser();
                setIsAuthenticated(true);
                setAuthError(false);
            } catch (error) {
                setIsAuthenticated(false);
                setAuthError(true);
            } finally {
                setIsLoading(false);
            }
        };

        checkAuthentication();
    }, []);

    if (isLoading) {
        return null;
    }

    if (authError) {
        return <div className="container mx-auto p-4 text-red-600">Ошибка входа</div>;
    }

    if (!isAuthenticated) {
        return <div className="container mx-auto p-4">Нет доступа</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-8">Распознаватель</h1>
            <FileUploader />
        </div>
    );
}