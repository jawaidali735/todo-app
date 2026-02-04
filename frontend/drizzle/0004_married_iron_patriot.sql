ALTER TABLE "tasks" DISABLE ROW LEVEL SECURITY;--> statement-breakpoint
DROP TABLE "tasks" CASCADE;--> statement-breakpoint
ALTER TABLE "better_auth_account" DROP CONSTRAINT "better_auth_account_user_id_better_auth_user_id_fk";
--> statement-breakpoint
ALTER TABLE "better_auth_session" DROP CONSTRAINT "better_auth_session_user_id_better_auth_user_id_fk";
--> statement-breakpoint
ALTER TABLE "better_auth_account" ADD COLUMN "token_type" text;--> statement-breakpoint
ALTER TABLE "better_auth_account" ADD COLUMN "scope" text;--> statement-breakpoint
ALTER TABLE "better_auth_account" ADD COLUMN "password" text;--> statement-breakpoint
ALTER TABLE "better_auth_session" ADD COLUMN "idle_expires_at" timestamp NOT NULL;--> statement-breakpoint
ALTER TABLE "better_auth_user" ADD COLUMN "first_name" text;--> statement-breakpoint
ALTER TABLE "better_auth_user" ADD COLUMN "last_name" text;--> statement-breakpoint
ALTER TABLE "better_auth_user" ADD COLUMN "role" text DEFAULT 'user';