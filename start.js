#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

console.log('========================================');
console.log('AI Meeting Summarizer - Starting...');
console.log('========================================\n');

// Determine Python path based on OS
const isWindows = process.platform === 'win32';
const pythonPath = isWindows 
  ? path.join(__dirname, 'venv', 'Scripts', 'python.exe')
  : path.join(__dirname, 'venv', 'bin', 'python');
const backendPath = path.join(__dirname, 'backend', 'app.py');

console.log('Starting Flask Backend...');
console.log(`Python: ${pythonPath}`);
console.log(`Backend: ${backendPath}\n`);

// Start backend
const backend = spawn(pythonPath, [backendPath], {
  stdio: 'inherit',
  shell: false
});

backend.on('error', (err) => {
  console.error('❌ Failed to start backend:', err.message);
  console.error('\nTroubleshooting:');
  console.error('1. Make sure virtual environment is created: python -m venv venv');
  console.error('2. Make sure dependencies are installed: pip install -r requirements.txt');
  process.exit(1);
});

// Wait for backend to be ready
function checkBackend(retries = 30) {
  const options = {
    hostname: '127.0.0.1',
    port: 5000,
    path: '/api/meetings',
    method: 'GET',
    timeout: 1000
  };

  const req = http.request(options, (res) => {
    if (res.statusCode) {
      console.log('\n✅ Backend is ready!');
      console.log('Starting Electron Frontend...\n');
      
      // Start frontend
      const electronPath = isWindows ? 'npx.cmd' : 'npx';
      const electron = spawn(electronPath, ['electron', '.'], {
        stdio: 'inherit',
        shell: isWindows
      });

      electron.on('error', (err) => {
        console.error('❌ Failed to start frontend:', err.message);
        backend.kill();
        process.exit(1);
      });

      // Handle cleanup
      electron.on('exit', () => {
        console.log('\n👋 Shutting down...');
        backend.kill();
        process.exit(0);
      });
    }
  });

  req.on('error', () => {
    if (retries > 0) {
      if (retries % 10 === 0) {
        process.stdout.write(`Waiting for backend (${30 - retries + 1}/30)...\n`);
      }
      setTimeout(() => checkBackend(retries - 1), 1000);
    } else {
      console.error('\n❌ Backend failed to start after 30 seconds');
      console.error('\nCheck the terminal output above for errors.');
      backend.kill();
      process.exit(1);
    }
  });

  req.end();
}

// Wait 3 seconds then start checking
setTimeout(() => {
  console.log('Waiting for backend to initialize...');
  checkBackend();
}, 3000);

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
  console.log('\n\n👋 Shutting down gracefully...');
  backend.kill();
  setTimeout(() => process.exit(0), 500);
});

process.on('SIGTERM', () => {
  console.log('\n\n👋 Shutting down gracefully...');
  backend.kill();
  setTimeout(() => process.exit(0), 500);
});

