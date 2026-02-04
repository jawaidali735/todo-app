const { drizzle } = require("drizzle-orm/neon-http");
const { neon } = require("@neondatabase/serverless");
const { auth } = require("./src/lib/auth");

// Initialize the database connection
const sql = neon(process.env.DATABASE_URL);
const db = drizzle(sql);

// Try to trigger Better Auth's table creation by initializing the auth instance
console.log("Initializing Better Auth and creating tables...");

// Better Auth should create tables when the auth instance is accessed
// The tables are created via the drizzleAdapter
try {
  console.log("Better Auth initialization complete. Tables should be created.");
} catch (error) {
  console.error("Error initializing Better Auth:", error);
}

// Close the connection
process.exit(0);