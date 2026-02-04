#!/usr/bin/env node
// This script will run drizzle-kit push and automatically respond to prompts

const { spawn } = require('child_process');

// Set the environment variable
process.env.DATABASE_URL = 'postgresql://neondb_owner:npg_X9jxJwg6mSfM@ep-orange-night-ahjqz8d9-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require';

// Spawn the npx drizzle-kit push command
const drizzleProcess = spawn('npx', ['drizzle-kit', 'push'], {
  cwd: __dirname,
  env: process.env,
  stdio: ['pipe', 'pipe', 'pipe'] // stdin, stdout, stderr
});

// Listen to stdout
drizzleProcess.stdout.on('data', (data) => {
  const output = data.toString();
  console.log(output);

  // Look for the prompt and respond with Enter to select the first option
  if (output.includes('Is frontend_todos table created or renamed')) {
    setTimeout(() => {
      drizzleProcess.stdin.write('\n'); // Press Enter to select first option
      console.log('(Automatically selected: + frontend_todos create table)');
    }, 100);
  }
});

// Listen to stderr
drizzleProcess.stderr.on('data', (data) => {
  console.error(data.toString());
});

// Handle process close
drizzleProcess.on('close', (code) => {
  console.log(`drizzle-kit push exited with code ${code}`);
  process.exit(code);
});