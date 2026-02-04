import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    appDir: true,
  },
  // Specify the src directory as the base
  srcDir: 'src',
};

export default nextConfig;
