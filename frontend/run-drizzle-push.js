// Script to run drizzle-kit push with proper environment loading
require('dotenv').config({ path: './.env.local' });

const { execSync } = require('child_process');
const fs = require('fs');

// Verify that the config file exists
if (!fs.existsSync('./drizzle.config.ts')) {
  console.error('drizzle.config.ts does not exist!');
  process.exit(1);
}

console.log('DATABASE_URL exists:', !!process.env.DATABASE_URL);

try {
  // Run the drizzle-kit push command
  execSync('npx drizzle-kit push', {
    stdio: 'inherit',
    env: process.env
  });
} catch (error) {
  console.error('Error running drizzle-kit push:', error.message);
  process.exit(1);
}