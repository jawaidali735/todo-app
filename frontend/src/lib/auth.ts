import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db/drizzle";
import * as schema from "@/db/schema"

let authConfig: any = {
  emailAndPassword: {
    enabled: true,
  },
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-build", // Shared secret - also used by backend to verify JWT
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  trustHost: true,
  // No JWT plugin needed - we create our own JWT tokens with HS256 in get-jwt.ts
};

// Only add database config if we're not in build mode
if (process.env.NODE_ENV !== 'production' || process.env.DATABASE_URL) {
  try {
    if (process.env.DATABASE_URL) {
      authConfig.database = drizzleAdapter(db, {
        provider: "pg",
        schema: {
          ...schema,
        },
      });
    }
  } catch (e) {
    console.warn('Database adapter not initialized:', e);
  }
}

export const auth = betterAuth(authConfig);
