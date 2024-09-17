/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  i18n: {
    locales: ['de', 'en'],
    defaultLocale: 'de',
  },
  images: {
    unoptimized: false,
  },
  async redirects(){
    return [
      {
        source: '/',
        destination: '/start',
        permanent: true,
      },
    ]
  },
  async rewrites() {
    if(process.env.NODE_ENV === 'development'){
      return [
        {
          source: '/images/:path*',
          destination: 'https://monitoring.localzero.net/images/:path*',
        }
      ]
    }
    return [
    ]
  },
};

export default nextConfig;
