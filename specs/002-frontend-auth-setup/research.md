# Research: Frontend & Authentication Setup (Next.js 16+)

**Feature**: 002-frontend-auth-setup
**Date**: 2026-01-19
**Research Phase**: Phase 0 of Implementation Plan

## Objective
Research and validate implementation approaches for Next.js 16+ frontend with Better Auth and Drizzle ORM integration.

## Better Auth Integration with Next.js 16+

### Key Findings:
- Better Auth supports Next.js 13+ with App Router
- JWT Plugin enables stateless authentication for backend communication
- Client-side hooks available for session management
- Server-side components can access auth state using middleware

### Implementation Pattern:
```typescript
// Example auth configuration
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  // auth configuration
  plugins: [jwt()]
});
```

## Drizzle ORM with Neon PostgreSQL

### Key Findings:
- Drizzle ORM supports Neon Serverless driver (@neondatabase/serverless)
- Schema definition uses TypeScript for type safety
- Migration system handles database schema updates
- Works well with Next.js App Router patterns

### Schema Example:
```typescript
import { pgTable, serial, text, timestamp, boolean } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: text("email").notNull().unique(),
  password: text("password").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const tasks = pgTable("tasks", {
  id: serial("id").primaryKey(),
  userId: integer("user_id").references(() => users.id),
  title: text("title").notNull(),
  completed: boolean("completed").default(false),
  createdAt: timestamp("created_at").defaultNow(),
});
```

## JWT Token Handling

### Key Findings:
- Better Auth JWT plugin generates tokens accessible on frontend
- Tokens can be retrieved client-side for backend API communication
- Secure token transmission via Authorization header
- Token validation on backend ensures security

### Token Retrieval Pattern:
```typescript
// Getting JWT token for API calls
const { data: session } = useSession();
const token = session?.accessToken;
```

## Next.js App Router Patterns

### Key Findings:
- Layouts and route groups for protected routes
- Server Components can access auth state
- Client Components use hooks for auth state
- Middleware for universal auth protection

### Protected Route Pattern:
```typescript
// app/dashboard/page.tsx
import { auth } from "@/lib/auth";

export default async function DashboardPage() {
  const session = await auth();
  if (!session) {
    redirect("/login");
  }

  return <DashboardContent />;
}
```

## Neon PostgreSQL Connection

### Key Findings:
- Neon provides serverless PostgreSQL with instant branching
- Connection string format compatible with Drizzle
- Environment variable configuration for security
- Connection pooling handled automatically

### Connection String Format:
```
postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
```

## Tailwind CSS Integration

### Key Findings:
- Next.js 16+ supports Tailwind CSS v4+
- Configuration file setup with presets
- Component-based styling approach
- Responsive design utilities built-in

## Research Validation

### Confirmed Feasibility:
- ✅ Better Auth works with Next.js 16+ App Router
- ✅ Drizzle ORM connects to Neon PostgreSQL
- ✅ JWT tokens accessible for backend communication
- ✅ Protected routes achievable with Next.js patterns
- ✅ Tailwind CSS integrates with Next.js

### Potential Challenges:
- Token synchronization between frontend and backend
- Ensuring consistent user data isolation
- Managing environment variables securely across environments