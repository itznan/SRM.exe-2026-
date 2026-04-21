# SRM Secure Browser - Technical Documentation

## Architecture Overview

SRM Secure Browser is built on the Electron framework, combining Chromium and Node.js to create a cross-platform desktop application with enhanced security and proctoring capabilities.

### Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                   SRM Secure Browser                    │
├─────────────────────────────────────────────────────────┤
│  UI Layer: Electron (Chromium + Node.js)                │
│  - Main Process (Node.js)                               │
│  - Renderer Process (Chromium)                          │
│  - Webview for Exam Platform                            │
├─────────────────────────────────────────────────────────┤
│  Proctoring Layer:                                       │
│  - Desktop Capture (desktopCapturer API)                │
│  - Webcam Capture (getUserMedia API)                    │
│  - Process Monitoring (ps-list, node-process-windows)    │
│  - System Information (systeminformation)                │
├─────────────────────────────────────────────────────────┤
│  Detection Layer:                                        │
│  - VMDetect.exe (Virtual Machine Detection)              │
│  - DetectUserSwitch.exe (User Account Switching)        │
│  - DetectProcessesWithUI.exe (Process Monitoring UI)     │
│  - DetectVirtualDesktop/ (Virtual Desktop Detection)    │
│  - Restrictions-DiableWinKey-WinFormsApp.exe (Win Key)  │
├─────────────────────────────────────────────────────────┤
│  Communication Layer:                                    │
│  - HTTP Requests (request library)                      │
│  - WebSocket (for real-time updates)                    │
│  - AJAX (for data upload)                               │
└─────────────────────────────────────────────────────────┘
```

## File Structure

### Installation Structure
```
C:\Program Files\SRM Secure Browser\
├── SRM.exe                    # Electron runtime (107 MB)
├── resources/
│   ├── app.asar               # Main application code (59 MB)
│   ├── app.asar.unpacked/    # Unpacked executables
│   │   ├── VMDetect.exe
│   │   ├── DetectUserSwitch.exe
│   │   ├── DetectProcessesWithUI.exe
│   │   ├── DetectVirtualDesktop/
│   │   ├── Restrictions-DiableWinKey-WinFormsApp.exe
│   │   └── DiableWinKey-WinFormsApp-DisableRestrictions.exe
│   ├── elevate.exe            # UAC elevation helper
│   └── app-update.yml         # Update configuration
├── locales/                   # 53 language files
├── chrome_100_percent.pak     # Chrome resources
├── chrome_200_percent.pak
├── resources.pak
├── icudtl.dat                 # ICU data
├── v8_context_snapshot.bin    # V8 snapshot
└── [DLLs]                     # Chromium DLLs
    ├── d3dcompiler_47.dll
    ├── ffmpeg.dll
    ├── libEGL.dll
    ├── libGLESv2.dll
    └── ...
```

### ASAR Structure
```
app.asar/
├── main.js                    # Main process (obfuscated)
├── preload.js                 # Preload script
├── index.html                 # UI entry point
├── package.json               # Dependencies
├── chrome-tabs/               # Tab management
├── node_modules/              # Node.js dependencies
├── public/                    # Public assets
├── private/                   # Private modules
├── Main/                      # Main module helpers
└── includes/                  # Included libraries
```

## Dependencies

### Node.js Dependencies (package.json)
```json
{
  "ajv": "^6.10.2",                    // JSON schema validation
  "ajv-keywords": "^3.4.1",            // AJV keywords
  "bytenode": "^1.3.6",                // JavaScript bytecode compiler
  "node-process-windows": "0.0.2",     // Windows process management
  "ps-list": "^7.0.0",                 // Process listing
  "request": "^2.87.0",                // HTTP requests
  "systeminformation": "^5.17.3"      // System information gathering
}
```

### Chromium Components
- **V8 JavaScript Engine**: JavaScript execution
- **Blink Rendering Engine**: HTML/CSS rendering
- **ICU**: Internationalization support
- **FFmpeg**: Media encoding/decoding
- **ANGLE**: OpenGL translation layer

## Main Process (main.js)

### Architecture
The main process is heavily obfuscated using bytenode (JavaScript bytecode compilation). Key components include:

### IPC Communication
```javascript
const { ipcMain, BrowserWindow, globalShortcut, dialog } = require('electron');
```

### Key Functions

#### 1. Process Monitoring
```javascript
// Monitors running processes every 5 seconds
setInterval(() => {
    KillBlacklistedSoftwares();
}, 5000);
```

#### 2. Application Blacklist
```javascript
const blacklistedApps = [
    'discord|discord.exe',
    'teamviewer|teamviewer.exe',
    'skype|skype.exe',
    'webex|webex.exe',
    'opera|opera.exe',
    'edge|edge.exe',
    'zoom|zoom.exe',
    'anydesk|anydesk.exe',
    'ammyy|ammyy.exe',
    'gotomeeting|gotomeeting.exe',
    'join.me|join.me',
    'telegram|telegram.exe',
    'slack|slack.exe',
    'obs|obs.exe',
    'camrecorder|camrecorder.exe',
    'camplay|camplay.exe',
    'gamebar|gamebar.exe'
];
```

#### 3. Process Termination
```javascript
exec('taskkill /PID ' + pid + ' /F', (error, stdout, stderr) => {
    // Force kill process
});
```

#### 4. Virtual Desktop Detection
```javascript
// Windows 10/11
exec('Virtualdesktop10.exe /GetCurrentDesktop');

// Windows 11
exec('Virtualdesktop11.exe /GetCurrentDesktop');

// macOS
exec('VirtualdesktopMac /GetCurrentDesktop');
```

#### 5. Power Monitoring
```javascript
const { powerMonitor } = require('electron');

powerMonitor.on('suspend', () => {
    // System suspend detected
    mainWindow.webContents.send('lockscreendetected', {data: 'SUSPENDED'});
});

powerMonitor.on('unlock-screen', () => {
    // Screen unlock detected
    mainWindow.webContents.send('lockscreendetected', {data: 'UNLOCKED'});
});
```

## Renderer Process (renderer.js)

### Screen Recording

#### Desktop Capture
```javascript
desktopCapturer.getSources({ types: ['screen'] }).then(async sources => {
    for (const source of sources) {
        if (source.name === 'Entire Screen' || source.name === 'Entire screen' || source.name === 'Screen 1') {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: false,
                video: {
                    mandatory: {
                        chromeMediaSource: 'desktop',
                        chromeMediaSourceId: source.id,
                        maxWidth: window.screen.width / 1.5,
                        maxFrameRate: 2
                    }
                }
            });
            handleStream(stream);
        }
    }
});
```

#### Recording Parameters
- **Frame Rate**: 2 FPS
- **Resolution**: 66.7% of screen width
- **Format**: WebM with VP9 codec
- **Chunk Size**: 30 seconds

### Webcam Recording

#### Camera Capture
```javascript
navigator.mediaDevices.getUserMedia({
    video: { 
        frameRate: { ideal: 5, max: 10 }, 
        facingMode: { ideal: "user" }, 
        width: { ideal: 640 }, 
        height: { ideal: 480 } 
    },
    audio: true
});
```

#### Recording Parameters
- **Frame Rate**: 5-10 FPS
- **Resolution**: 640x480 (VGA)
- **Facing Mode**: "user" (front-facing)
- **Format**: WebM with VP9 codec
- **Chunk Size**: 30 seconds

### Proctoring Events

#### Window Focus Detection
```javascript
function FlagMovedOutOfScreen() {
    noOfMovedOutOfScreenFlags++;
    // Upload to server
}
```

#### Screen Lock Detection
```javascript
function FlagScreenLock() {
    noOfScreenLockDetectedFlags++;
    // Upload to server
}
```

## Detection Executables

### VMDetect.exe
**Purpose**: Detect virtual machine environments

**Detection Methods**:
- CPUID instruction checks
- Hypervisor presence detection
- Registry key checks
- WMI queries for VM signatures

**Supported VMs**:
- VMware
- VirtualBox
- Hyper-V
- QEMU
- Parallels

### DetectUserSwitch.exe
**Purpose**: Detect user account switching

**Detection Method**:
- Monitors Windows session changes
- Detects fast user switching
- Triggers alert on user switch

### DetectProcessesWithUI.exe
**Purpose**: Show UI for process detection

**Features**:
- Displays detected processes to user
- Shows prohibited applications
- Provides user-friendly alerts

### DetectVirtualDesktop/
**Purpose**: Detect virtual desktop usage

**Detection Method**:
- Queries Windows virtual desktop API
- Detects virtual desktop switches
- Monitors desktop creation/deletion

### Restrictions-DiableWinKey-WinFormsApp.exe
**Purpose**: Disable Windows key and system restrictions

**Features**:
- Disables Windows key
- Blocks Alt+Tab
- Blocks Ctrl+Alt+Delete
- Blocks other system shortcuts

## Network Communication

### API Endpoints

#### License Validation
```
POST /API/License.ashx
Content-Type: application/x-www-form-urlencoded

Response:
{
    "IsError": false,
    "BlacklistedProcessNames": [],
    "WhitelistedProcessNamesListIncludes": [],
    "ProcessesRunning": [...]
}
```

#### Desktop Video Upload
```
POST /API/UploadStudentDesktopVideo.ashx
Content-Type: multipart/form-data

Form Data:
- StudentRasciId: string
- StudentDesktopVideoIncrementCounter: number
- VideoBlob: binary
```

#### Webcam Video Upload
```
POST /API/UploadStudentWebCamVideo.ashx
Content-Type: multipart/form-data

Form Data:
- StudentRasciId: string
- VideoBlob: binary
```

#### Event Logging
```
POST /API/MovedOutOfScreenAppendBlob.ashx
POST /API/LockScreenDetectedAppendBlob.ashx
POST /API/MoreThan1FaceDetectedAppendBlob.ashx
POST /API/NoFaceDetectedAppendBlob.ashx
```

### WebSocket Events

#### Proctoring Events
```javascript
ipcRenderer.sendToHost('start-proctoring', StudentInfoJSON);
ipcRenderer.sendToHost('stop-proctoring');
ipcRenderer.sendToHost('remove-loader', {});
```

#### Main Process Events
```javascript
mainWindow.webContents.send('lockscreendetected', {data: 'UNLOCKED'});
mainWindow.webContents.send('switchdesktopdetected', desktopName);
mainWindow.webContents.send('data.IsError is true', error);
```

## System Information Gathering

### Using systeminformation Library

#### Graphics Information
```javascript
si.graphics()
  .then(data => {
    // GPU information
    // Display information
    // Driver information
  });
```

#### Process Information
```javascript
si.processes()
  .then(data => {
    // Running processes
    // CPU usage
    // Memory usage
  });
```

#### USB Information
```javascript
si.usb()
  .then(data => {
    // Connected USB devices
    // Device names
    // Vendor IDs
  });
```

## Security Mechanisms

### Code Obfuscation

#### bytenode
```javascript
// Original code
function hello() {
    console.log('Hello World');
}

// Compiled to bytecode
// Cannot be easily reverse engineered
```

#### String Encoding
```javascript
// Obfuscated strings
var _0x4355ea = _0x5982;
// String array with encoded values
```

### Content Protection

#### setContentProtection
```javascript
mainWindow.setContentProtection(true);
// Prevents screen capture of secure content
```

#### Session Restrictions
```javascript
session.defaultSession.webRequest.onBeforeSendHeaders((details, callback) => {
    // Modify headers
    // Add custom user agent
    callback({ cancel: false, requestHeaders: details.requestHeaders });
});
```

## Update Mechanism

### electron-builder Configuration

```yaml
# app-update.yml
owner: nevillekatila
repo: es-stage
provider: github
releaseType: draft
updaterCacheDirName: srmug-secure-browser-updater
```

### Update Process
1. Check GitHub releases for new version
2. Download update package
3. Verify signature
4. Install update
5. Restart application

## Configuration

### Environment Variables
- `NODE_ENV`: Development/Production
- `ELECTRON_ENABLE_LOGGING`: Enable debug logging
- `ELECTRON_ENABLE_GPU`: Enable GPU acceleration

### Registry Keys
```
HKLM\Software\SRM Secure Browser
HKCU\Software\SRM Secure Browser
```

### Configuration Files
- `app-update.yml`: Update configuration
- `package.json`: Application metadata
- `resources.pak`: Chrome resources

## Performance Considerations

### Resource Usage
- **Memory**: ~200-300 MB (idle), ~500-800 MB (recording)
- **CPU**: ~5-10% (idle), ~15-25% (recording)
- **Disk**: ~500 MB installation
- **Network**: ~1-2 Mbps upload (during recording)

### Optimization Techniques
- Low framerate recording (2 FPS desktop, 5-10 FPS webcam)
- Chunked video upload (30-second intervals)
- WebM/VP9 compression
- Lazy loading of modules

## Error Handling

### Common Errors

#### License Validation Error
```javascript
if (data.IsError === true) {
    console.log('In catch of License.ashx call');
    // Show error to user
    // Retry mechanism
}
```

#### Process Kill Error
```javascript
exec('taskkill /PID ' + pid + ' /F', (error, stdout, stderr) => {
    if (error) {
        console.log('Error killing process: ' + error);
    }
});
```

#### Network Error
```javascript
request.post(url, { form: data }, (error, response, body) => {
    if (error) {
        // Retry logic
        // Error logging
    }
});
```

## Debugging

### Enable Debug Mode
```bash
# Windows
set ELECTRON_ENABLE_LOGGING=1
SRM.exe

# Or create debug shortcut
SRM.exe --enable-logging --log-level=verbose
```

### Log Locations
- **Windows**: `%APPDATA%\SRM Secure Browser\logs\`
- **Log Files**: `main.log`, `renderer.log`, `gpu.log`

### DevTools
```javascript
// In development
mainWindow.webContents.openDevTools();
```

## Build Process

### Build Tools
- **electron-builder**: Application packaging
- **electron-packager**: Cross-platform packaging
- **asar**: Archive creation

### Build Commands
```bash
# Build for Windows
npm run build:win

# Build with NSIS installer
npm run build:nsis

# Build for development
npm run build:dev
```

### NSIS Script
The NSIS installer script handles:
- File extraction
- Registry entries
- Uninstaller creation
- Desktop shortcut creation

## Security Best Practices

### Implemented
- Code obfuscation (bytenode)
- Content protection (setContentProtection)
- Process monitoring
- Virtual machine detection
- User switch detection
- Screen lock detection

### Recommendations
- Implement certificate pinning for API calls
- Add integrity checks for executable files
- Implement secure storage for sensitive data
- Add anti-debugging techniques
- Implement tamper detection

## Compliance

### Privacy
- GDPR compliance considerations
- Data encryption in transit
- Secure data storage
- User consent mechanisms

### Accessibility
- WCAG 2.1 compliance
- Keyboard navigation
- Screen reader support
- High contrast mode

## Version History

### Version 1.0.20 (Current)
- Electron-based architecture
- Advanced proctoring features
- Enhanced security mechanisms
- Improved performance

### Previous Versions
- Legacy NSIS-only versions
- Basic proctoring features
- Limited security

## Future Enhancements

### Planned Features
- AI-powered behavior analysis
- Advanced face recognition
- Biometric authentication
- Blockchain-based verification
- Mobile app integration

### Technical Improvements
- Reduced resource usage
- Faster upload speeds
- Better compression
- Cross-platform support (macOS, Linux)

## API Reference

### Main Process APIs

#### ipcMain Events
```javascript
ipcMain.on('start-proctoring', (event, data) => {
    // Start proctoring session
});

ipcMain.on('stop-proctoring', (event) => {
    // Stop proctoring session
});
```

#### BrowserWindow Methods
```javascript
mainWindow.setContentProtection(true);
mainWindow.setAlwaysOnTop(true);
mainWindow.setFullScreen(true);
```

### Renderer Process APIs

#### ipcRenderer Methods
```javascript
ipcRenderer.sendToHost('event-name', data);
ipcRenderer.send('event-name', data);
```

#### Electron APIs
```javascript
const { remote } = require('electron');
const { desktopCapturer } = require('electron');
```

## Troubleshooting Guide

### Technical Issues

#### Application Won't Launch
1. Check Windows Event Viewer
2. Verify .NET Framework 4.5+ is installed
3. Check antivirus logs
4. Run as Administrator

#### Proctoring Not Working
1. Check network connectivity
2. Verify API endpoints are accessible
3. Check firewall settings
4. Review log files

#### Recording Issues
1. Verify webcam/microphone permissions
2. Check Windows privacy settings
3. Test in Windows Camera app
4. Update graphics drivers

## License and Legal

### License
- CC0-1.0 (Public Domain)
- Proprietary components (Electron, Chromium)

### Third-Party Licenses
- Electron: MIT License
- Chromium: BSD License
- Node.js: MIT License
- Various npm packages: Various licenses

---

**For technical support or questions, contact the development team at Eduswitch Solutions Pvt Ltd.**
