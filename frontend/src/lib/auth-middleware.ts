import { betterAuth } from "better-auth";

// Create auth instance without database adapter for middleware
export const authMiddleware = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-build",
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  trustHost: true,
});