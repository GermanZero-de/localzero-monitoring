/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
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
    if(process.env.NODE_ENV === 'development' && !process.env.LOCALDEV){
      return [
        {
          source: '/images/:path*',
          destination: 'https://monitoring.localzero.net/images/:path*',
        }
      ]
    } else {
      return [
        {
          source: '/images/:path*',
          destination: 'http://localhost:8000/images/:path*',
        }
      ]
    }
  },
};

export default nextConfig;
