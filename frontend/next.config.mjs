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
    console.log(process.env.LOCALDEV)
    if(process.env.NODE_ENV === 'development' && !process.env.LOCALDEV){
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
