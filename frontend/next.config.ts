import type { NextConfig } from "next";
import BASE_URL from '@/constants'

const fs = require('fs');
const path = require('path');
const main_dir = 'src'


// const certPath = path.join(__dirname, `${main_dir}/certs`);
// const key = fs.readFileSync(path.join(certPath, 'key.pem'));
// const cert = fs.readFileSync(path.join(certPath, 'cert.pem'));

// module.exports = {
//     server: {
//         https: {
//             key,
//             cert,
//         },
//     },
// };
module.exports = {
    serverRuntimeConfig: {
        __NEXT_DISABLE_SERVER_LOGS: true,
    },

    // Отключение build logs
    logging: {
        level: 'error',
        fetches: {
            fullUrl: false
        }
    },

    // Отключение webpack logs
    webpack: (config, { isServer }) => {
        config.infrastructureLogging = {
            level: 'error',
            debug: false
        };
        return config;
    },
    cssModules: true,
    cssLoaderOptions: {
        importLoaders: 1,
        localIdentName: '[local]___[hash:base64:5]',
    },
    sassOptions: {
        includePaths: [path.join(__dirname, 'src/styles')],
        prependData: `@import 'variables.scss';`,
    },
    async rewrites() {
        return [
            {
                source: '/:path*',
                destination: `http://localhost:8080/:path*`,
            },
        ];
    },
};

const nextConfig: NextConfig = {
    /* config options here */
};

export default nextConfig;
