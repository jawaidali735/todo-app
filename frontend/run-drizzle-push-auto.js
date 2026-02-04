// Script to run drizzle-kit push with automatic response to prompts
require('dotenv').config({ path: './.env.local' });

const { spawn } = require('child_process');

// Spawn the drizzle-kit push command
const child = spawn('npx', ['drizzle-kit', 'push'], {
  stdio: ['pipe', 'inherit', 'inherit'],
  env: process.env,
  cwd: process.cwd()
});

// Send 'Enter' to accept the first option ('+ users create table')
setTimeout(() => {
  child.stdin.write('\n'); // Press Enter to select the first option
}, 5000); // Wait 5 seconds for the prompt to appear

// Handle process events
child.on('close', (code) => {
  console.log(`Child process exited with code ${code}`);
  process.exit(code);
});

child.on('error', (err) => {
  console.error('Error running drizzle-kit push:', err.message);
  process.exit(1);
});