"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { googleAuthCallback } from "@/auth_api/api";

const GoogleCallbackPage = () => {
    const router = useRouter();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const handleGoogleCallback = async () => {
            const urlParams = new URLSearchParams(window.location.search);
            const code = urlParams.get("code");
            const state = urlParams.get("state");

            if (!code || !state) {
                setError("Ошибка: отсутствует код или state.");
                setLoading(false);
                return;
            }

            try {
                const data = await googleAuthCallback(code, state);
                router.push("/");
            } catch (err) {
                setError("Ошибка при входе через Google.");
            } finally {
                setLoading(false);
            }
        };

        handleGoogleCallback();
    }, [router]);

    if (loading) return <p>Загрузка...</p>;
    if (error) return <p style={{ color: "red" }}>{error}</p>;

    return null;
};

export default GoogleCallbackPage;
