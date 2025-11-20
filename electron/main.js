const { app, BrowserWindow, ipcMain, Notification, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const io = require('socket.io-client');

let mainWindow;
let pythonProcess;
let socket;

// Start Python backend
function startBackend() {
  const pythonScript = path.join(__dirname, '..', 'backend', 'app.py');
  
  pythonProcess = spawn('python', [pythonScript], {
    cwd: path.join(__dirname, '..'),
  });
  
  pythonProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });
  
  pythonProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });
  
  pythonProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });
  
  // Wait for backend to start, then connect
  setTimeout(() => {
    connectToBackend();
  }, 3000);
}

// Connect to backend via Socket.IO
function connectToBackend() {
  console.log('Attempting to connect to backend at http://127.0.0.1:5000');
  
  socket = io('http://127.0.0.1:5000', {
    transports: ['polling', 'websocket'],
    upgrade: true,
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 10,
    timeout: 10000
  });
  
  socket.on('connect', () => {
    console.log('✓ Connected to backend successfully!');
    if (mainWindow) {
      mainWindow.webContents.send('backend-status', { connected: true });
    }
  });
  
  socket.on('connect_error', (error) => {
    console.error('Connection error:', error.message);
  });
  
  socket.on('disconnect', () => {
    console.log('Disconnected from backend');
    if (mainWindow) {
      mainWindow.webContents.send('backend-status', { connected: false });
    }
  });
  
  socket.on('recording_started', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('recording-started', data);
    }
    showNotification('Recording Started', `Meeting "${data.title}" is now being recorded`);
  });
  
  socket.on('processing_status', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('processing-status', data);
    }
    // Notify on major processing milestones
    if (data.status === 'transcribing') {
      showNotification('Transcribing Audio', 'Converting speech to text...');
    } else if (data.status === 'summarizing') {
      showNotification('Generating Summary', 'AI is analyzing the meeting...');
    } else if (data.status === 'extracting_actions') {
      showNotification('Extracting Actions', 'Identifying action items...');
    }
  });
  
  socket.on('meeting_processed', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('meeting-processed', data);
    }
    showNotification('Meeting Processed', 'Summary and action items are ready!');
  });
  
  socket.on('audio_status', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('audio-status', data);
    }
  });
  
  socket.on('live_transcript_update', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('live-transcript-update', data);
    }
  });
  
  socket.on('error', (data) => {
    if (mainWindow) {
      mainWindow.webContents.send('error', data);
    }
    showNotification('Error', data.message || 'An error occurred');
  });
}

// Create main window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    icon: path.join(__dirname, 'assets', 'icon.png')
  });
  
  mainWindow.loadFile(path.join(__dirname, '..', 'frontend', 'index.html'));
  
  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
  
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
  
  // Create menu
  createMenu();
}

// Create application menu
function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New Meeting',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('new-meeting');
          }
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: 'CmdOrCtrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Meeting',
      submenu: [
        {
          label: 'Start Recording',
          accelerator: 'CmdOrCtrl+R',
          click: () => {
            mainWindow.webContents.send('start-recording');
          }
        },
        {
          label: 'Stop Recording',
          accelerator: 'CmdOrCtrl+S',
          click: () => {
            mainWindow.webContents.send('stop-recording');
          }
        }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Documentation',
          click: () => {
            require('electron').shell.openExternal('https://github.com/yourusername/ai-meeting-summarizer');
          }
        },
        {
          label: 'About',
          click: () => {
            mainWindow.webContents.send('show-about');
          }
        }
      ]
    }
  ];
  
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Show desktop notification
function showNotification(title, body) {
  if (Notification.isSupported()) {
    // Check if notifications are enabled (default: true)
    const Store = require('electron-store');
    const store = new Store();
    const notificationsEnabled = store.get('enableNotifications', true);
    
    if (notificationsEnabled) {
      const notification = new Notification({
        title: title,
        body: body,
        icon: path.join(__dirname, 'assets', 'icon.png'),
        silent: false,
        timeoutType: 'default'
      });
      notification.show();
      
      // Auto-close after 5 seconds
      setTimeout(() => {
        notification.close();
      }, 5000);
    }
  }
}

// IPC handlers
ipcMain.on('start-recording', (event, data) => {
  console.log('[ELECTRON] Received start-recording IPC event:', data);
  console.log('[ELECTRON] Socket connected:', socket && socket.connected);
  if (socket && socket.connected) {
    console.log('[ELECTRON] Emitting start_recording to backend');
    socket.emit('start_recording', data);
  } else {
    console.error('[ELECTRON] Socket not connected! Cannot start recording.');
  }
});

ipcMain.on('stop-recording', (event, data) => {
  console.log('[ELECTRON] Received stop-recording IPC event:', data);
  console.log('[ELECTRON] Socket connected:', socket && socket.connected);
  if (socket && socket.connected) {
    console.log('[ELECTRON] Emitting stop_recording to backend');
    socket.emit('stop_recording', data);
  } else {
    console.error('[ELECTRON] Socket not connected! Cannot stop recording.');
  }
});

ipcMain.on('sync-tasks', (event, data) => {
  if (socket && socket.connected) {
    socket.emit('sync_action_items', data);
  }
});

ipcMain.on('show-notification', (event, data) => {
  showNotification(data.title, data.body);
});

// App lifecycle
app.on('ready', () => {
  createWindow();
  
  // Wait for backend to fully start, then connect
  setTimeout(() => {
    connectToBackend();
  }, 5000);  // Increased wait time
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('before-quit', () => {
  // Don't kill backend - npm will handle it
  
  // Disconnect socket
  if (socket) {
    socket.disconnect();
  }
});

