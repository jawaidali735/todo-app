# Frontend Authentication Setup

This project implements a modern web application frontend using Next.js 16+ with Better Auth for authentication and Drizzle ORM for database interactions. The system provides secure user signup/login functionality, protected dashboard access, and JWT-based communication with backend services.

## Features

- User authentication with email/password
- Protected dashboard with user-specific content
- Task management system
- JWT-based secure communication with backend
- Responsive UI with Tailwind CSS

## Tech Stack

- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (with JWT plugin)
- Drizzle ORM
- Neon PostgreSQL
- Lucide React icons

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy the environment variables:
```bash
cp .env.example .env.local
```

3. Update the `.env.local` file with your configuration:
```env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname"
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-secret-key-here
```

4. Run the development server:
```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to view the application.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── layout.tsx
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── dashboard/
│   │   ├── api/
│   │   │   └── auth/
│   │   └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   └── dashboard/
│   ├── db/
│   ├── lib/
│   └── services/
├── middleware.ts
├── drizzle.config.ts
└── ...
```

## Authentication Flow

1. Users can sign up with email and password
2. Authentication is handled by Better Auth
3. JWT tokens are used for secure communication with the backend
4. Protected routes check for valid sessions before granting access

## Database Schema

The application uses Drizzle ORM with the following key tables:
- Users (managed by Better Auth)
- Tasks (user-specific tasks)

## API Communication

The frontend communicates with the backend using authenticated requests with JWT tokens in the Authorization header:

```
Authorization: Bearer <token>
```

## Environment Variables

- `DATABASE_URL`: Neon PostgreSQL connection string
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Base URL for Better Auth
- `NEXT_PUBLIC_BETTER_AUTH_SECRET`: Secret key for JWT signing

## Migrations

To manage database schema changes:

```bash
npx drizzle-kit push
```

## Learn More

To learn more about the technologies used in this project, check out the following resources:

- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com/docs)
- [Drizzle ORM Documentation](https://orm.drizzle.team/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)