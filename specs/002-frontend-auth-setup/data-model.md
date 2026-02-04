# Data Model: Frontend & Authentication Setup

**Feature**: 002-frontend-auth-setup
**Date**: 2026-01-19
**Database**: Neon Serverless PostgreSQL with Drizzle ORM

## Overview
Defines the database schema for the frontend authentication system using Drizzle ORM with Neon PostgreSQL. The schema includes Better Auth required tables and application-specific task management tables.

## Better Auth Tables

### Users Table
```typescript
import { pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: text("id").primaryKey().notNull(),
  email: text("email").notNull().unique(),
  emailVerified: timestamp("email_verified"),
  firstName: text("first_name"),
  lastName: text("last_name"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
  password: text("password").notNull(), // hashed
  image: text("image"), // profile picture URL
  disabled: boolean("disabled").default(false),
  role: text("role").default("user"),
});
```

**Purpose**: Stores user account information for authentication system.

### Sessions Table
```typescript
export const sessions = pgTable("sessions", {
  id: text("id").primaryKey().notNull(),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  expiresAt: timestamp("expires_at", {
    mode: "date",
    withTimezone: true,
  }).notNull(),
  ipAddress: text("ip_address"), // for security tracking
  userAgent: text("user_agent"), // for security tracking
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

**Purpose**: Tracks active user sessions for authentication state.

### Accounts Table
```typescript
export const accounts = pgTable("accounts", {
  id: text("id").primaryKey().notNull(),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  providerId: text("provider_id").notNull(), // e.g., "credentials", "google"
  providerAccountId: text("provider_account_id").notNull(), // provider's user ID
  refreshToken: text("refresh_token"),
  accessToken: text("access_token"),
  idToken: text("id_token"),
  expiresAt: timestamp("expires_at"),
  password: text("password"), // for credentials provider
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});
```

**Purpose**: Stores account information for different authentication providers.

### Verification Tokens Table
```typescript
export const verificationTokens = pgTable(
  "verification_tokens",
  {
    id: text("id").primaryKey().notNull(),
    identifier: text("identifier").notNull(), // email or username
    value: text("value").notNull(), // the token
    expiresAt: timestamp("expires_at", {
      mode: "date",
      withTimezone: true,
    }).notNull(),
    type: text("type").notNull(), // "email_verification", "password_reset"
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (vt) => ({
    uniqueIdentifierValue: unique().on(vt.identifier, vt.value),
  })
);
```

**Purpose**: Handles email verification and password reset tokens.

## Application-Specific Tables

### Tasks Table
```typescript
export const tasks = pgTable("tasks", {
  id: text("id").primaryKey().notNull(),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }), // Links to user who owns the task
  title: text("title").notNull(),
  description: text("description"),
  completed: boolean("completed").default(false),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
  dueDate: timestamp("due_date"),
  priority: text("priority").default("medium"), // low, medium, high
});
```

**Purpose**: Stores user-specific tasks with completion status and metadata.

### Task Categories Table (Optional Extension)
```typescript
export const taskCategories = pgTable("task_categories", {
  id: text("id").primaryKey().notNull(),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }), // Owned by user
  name: text("name").notNull(),
  color: text("color").default("#3B82F6"), // Default blue color
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});
```

**Purpose**: Optional categorization system for tasks.

## Relationships

### User-Task Relationship
- **One-to-Many**: One user can have many tasks
- **Constraint**: Tasks are deleted when user is deleted (CASCADE)
- **Index**: userId in tasks table for efficient queries

### Foreign Key Constraints
1. `tasks.userId` → `users.id` (CASCADE delete)
2. `sessions.userId` → `users.id` (CASCADE delete)
3. `accounts.userId` → `users.id` (CASCADE delete)

## Indexes for Performance

### Primary Indexes
- `users.email` - Unique index for authentication lookup
- `tasks.userId` - Index for user-specific task queries
- `sessions.expiresAt` - Index for session cleanup

### Additional Indexes
- `tasks.completed` - For filtering completed/pending tasks
- `tasks.createdAt` - For chronological task ordering
- `verificationTokens.expiresAt` - For token expiration queries

## Security Considerations

### Data Isolation
- All user-specific data includes `userId` foreign key
- Queries must always filter by authenticated user's ID
- No cross-user data access is possible through proper JOINs

### Password Storage
- Passwords are stored as bcrypt hashes in the `accounts` table
- Never store plaintext passwords
- Use Better Auth's built-in password hashing

### Token Security
- Verification tokens have expiration times
- Session tokens have expiration times
- Regular cleanup of expired tokens required