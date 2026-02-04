import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db/drizzle";
import * as schema from "@/db/schema"

// Only initialize with database adapter in server components, not in edge runtime
const createAuthInstance = () => {
  let authConfig: any = {
    emailAndPassword: {
      enabled: true,
    },
    secret: process.env.BETTER_AUTH_SECRET!, // Shared secret - also used by backend to verify JWT
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
    trustHost: true,
    // No JWT plugin needed - we create our own JWT tokens with HS256 in get-jwt.ts
  };

  // Add database config only if not in edge runtime and DATABASE_URL is available
  if (typeof window === 'undefined' && process.env.DATABASE_URL) {
    try {
      authConfig.database = drizzleAdapter(db, {
        provider: "pg",
        schema: {
          ...schema,
        },
      });
    } catch (e) {
      console.warn('Database adapter not initialized:', e);
    }
  }

  return betterAuth(authConfig);
};

export const auth = typeof window !== 'undefined' ?
  betterAuth({
    secret: process.env.BETTER_AUTH_SECRET!,
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
    trustHost: true,
  }) : createAuthInstance();
