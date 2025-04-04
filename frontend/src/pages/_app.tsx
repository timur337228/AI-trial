import type {AppProps} from 'next/app';
import { useEffect } from 'react';
import '@/styles/global.scss';

export default function MyApp({Component, pageProps}: AppProps) {
    if (process.env.NODE_ENV === 'production') {
        const noop = () => {};
        [
            'assert', 'clear', 'count', 'debug', 'dir', 'dirxml',
            'error', 'exception', 'group', 'groupCollapsed', 'groupEnd',
            'info', 'log', 'markTimeline', 'profile', 'profileEnd',
            'table', 'time', 'timeEnd', 'timeStamp', 'trace', 'warn'
        ].forEach((method) => {
            // @ts-ignore
            window.console[method] = noop;
        });
    }
    useEffect(() => {
        const link = document.createElement('link');
        link.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap';
        link.rel = 'stylesheet';
        document.head.appendChild(link);
    }, []);
    return (
        <Component {...pageProps} />
    );
}