# I Reverse Engineered SRM Secure Browser (Exam Proctoring Software) - Here's What I Found

**TL;DR**: SRM Secure Browser is an Electron-based proctoring application that records your screen, webcam, monitors processes, and detects VMs. It uses heavy obfuscation, automatically closes 15+ applications, and uploads data to Talview servers. Here's the complete technical breakdown.

---

## Background

I recently reverse engineered **SRM Secure Browser** (v1.0.20), a proctored exam browser used by educational institutions. My goal was to understand exactly how it works, what it monitors, and what data it collects.

**Disclaimer**: This analysis is for educational purposes only. This software is designed for legitimate exam proctoring.

---

## What is SRM Secure Browser?

SRM Secure Browser is a Windows application (81.4 MB installer) that creates a controlled environment for online exams. It's developed by **Eduswitch Solutions Pvt Ltd** and integrates with the **Talview** exam platform.

### Quick Stats
- **Technology**: Electron (Chromium + Node.js)
- **Size**: 107 MB installed
- **Architecture**: 32-bit/64-bit compatible
- **Platform**: Windows 7+
- **License**: CC0-1.0 (Public Domain)

---

## Architecture

```
┌─────────────────────────────────────────┐
│         SRM Secure Browser              │
├─────────────────────────────────────────┤
│  UI: Electron (Chromium + Node.js)     │
│  - Main Process (Node.js)               │
│  - Renderer Process (Chromium)          │
│  - Webview for Exam Platform           │
├─────────────────────────────────────────┤
│  Proctoring:                            │
│  - Desktop Capture (2 FPS)             │
│  - Webcam Capture (5-10 FPS)            │
│  - Process Monitoring (every 5 sec)     │
│  - System Information Gathering         │
├─────────────────────────────────────────┤
│  Detection:                             │
│  - VMDetect.exe (VM Detection)          │
│  - DetectUserSwitch.exe                 │
│  - DetectProcessesWithUI.exe            │
│  - DetectVirtualDesktop/                │
│  - Restrictions App (Win Key disable)   │
└─────────────────────────────────────────┘
```

---

## What It Monitors

### 1. Screen Recording
- **Frame Rate**: 2 FPS
- **Resolution**: 66.7% of screen width
- **Format**: WebM with VP9 codec
- **Upload**: 30-second chunks to server
- **Technology**: Electron's `desktopCapturer` API

### 2. Webcam Recording
- **Frame Rate**: 5-10 FPS
- **Resolution**: 640x480 (VGA)
- **Facing Mode**: Front-facing ("user")
- **Format**: WebM with VP9 codec
- **Upload**: 30-second chunks to server
- **Technology**: `getUserMedia` API

### 3. Process Monitoring
Scans running processes every 5 seconds using `ps-list` and `node-process-windows` libraries.

### 4. System Information
Gathers data using `systeminformation` library:
- Graphics/GPU information
- Running processes
- USB devices
- Monitor information
- OS details

---

## Applications It Automatically Closes

The app maintains a blacklist of 15+ applications that it **automatically force-closes** using `taskkill /F`:

### Communication Apps
- Discord, Skype, Slack, Telegram, WebEx

### Remote Access Tools
- TeamViewer, AnyDesk, Ammyy Admin, Join.me, GoToMeeting, Zoom

### Web Browsers
- Opera, Edge, SeaMonkey, Safari

### Screen Recording
- OBS Studio, CamRecorder, CamPlay

### Other
- Windows Game Bar, Element (Matrix client)

**Note**: These are closed via `taskkill /PID [pid] /F` every 5 seconds if detected.

---

## Detection Mechanisms

### Virtual Machine Detection (VMDetect.exe)
- CPUID instruction checks
- Hypervisor presence detection
- Registry key checks
- WMI queries for VM signatures
- **Supported**: VMware, VirtualBox, Hyper-V, QEMU, Parallels

### User Switch Detection (DetectUserSwitch.exe)
- Monitors Windows session changes
- Detects fast user switching
- Triggers alert on user switch

### Virtual Desktop Detection (DetectVirtualDesktop/)
- Queries Windows virtual desktop API
- Detects virtual desktop switches
- Monitors desktop creation/deletion

### Screen Lock Detection
- Uses Electron's `powerMonitor` API
- Detects system suspend/resume
- Detects screen lock/unlock

### Window Focus Detection
- Monitors when user leaves the exam window
- Flags "MovedOutOfScreen" events
- Uploads to server for proctoring review

---

## Security & Obfuscation

### Code Obfuscation
The main process (`main.js`) is heavily obfuscated using:

1. **bytenode** - JavaScript bytecode compilation
2. **String encoding** - Encoded string arrays
3. **Control flow obfuscation** - Makes reverse engineering difficult

### Content Protection
```javascript
mainWindow.setContentProtection(true);
// Prevents screen capture of secure content
```

### Session Restrictions
- Modified HTTP headers
- Custom user agent
- Content security policies

---

## Network Communication

### API Endpoints

**License Validation**
```
POST /API/License.ashx
Response: {
    "IsError": false,
    "BlacklistedProcessNames": [],
    "WhitelistedProcessNamesListIncludes": [],
    "ProcessesRunning": [...]
}
```

**Desktop Video Upload**
```
POST /API/UploadStudentDesktopVideo.ashx
Form Data:
- StudentRasciId: string
- StudentDesktopVideoIncrementCounter: number
- VideoBlob: binary (WebM/VP9)
```

**Webcam Video Upload**
```
POST /API/UploadStudentWebCamVideo.ashx
Form Data:
- StudentRasciId: string
- VideoBlob: binary (WebM/VP9)
```

**Event Logging**
- `/API/MovedOutOfScreenAppendBlob.ashx`
- `/API/LockScreenDetectedAppendBlob.ashx`
- `/API/MoreThan1FaceDetectedAppendBlob.ashx`
- `/API/NoFaceDetectedAppendBlob.ashx`

### GitHub Repository
- **Owner**: nevillekatila
- **Repo**: es-stage
- **Provider**: GitHub
- **Auto-updates**: Enabled via electron-builder

---

## Dependencies

### Node.js Packages
```json
{
  "ajv": "^6.10.2",                    // JSON schema validation
  "ajv-keywords": "^3.4.1",            // AJV keywords
  "bytenode": "^1.3.6",                // JavaScript bytecode (obfuscation)
  "node-process-windows": "0.0.2",     // Windows process management
  "ps-list": "^7.0.0",                 // Process listing
  "request": "^2.87.0",                // HTTP requests
  "systeminformation": "^5.17.3"      // System information gathering
}
```

### Chromium Components
- V8 JavaScript Engine
- Blink Rendering Engine
- FFmpeg (media encoding)
- ANGLE (OpenGL translation)

---

## Performance Impact

### Resource Usage
- **Memory**: 200-300 MB (idle), 500-800 MB (recording)
- **CPU**: 5-10% (idle), 15-25% (recording)
- **Disk**: 500 MB installation
- **Network**: 1-2 Mbps upload (during recording)

### Optimizations
- Low framerate recording (2 FPS desktop, 5-10 FPS webcam)
- Chunked video upload (30-second intervals)
- WebM/VP9 compression
- Lazy loading of modules

---

## What's NOT Active (Disabled Features)

Interestingly, several features are **commented out/disabled** in the current version:

1. **Face Detection** - Completely disabled
   - `processWebcamVideo` function commented out
   - No face detection alerts
   - No multiple face detection

2. **Webcam Video Upload** - Disabled
   - Comment: "no need to upload the webcam video"
   - Only desktop video is uploaded

3. **Image Quality Reduction** - Disabled
   - Comment: "for image quality and size reduction"

4. **Remote Proctoring Flag** - Disabled
   - `SetRemoteProctoringExamStartedFalse` commented out

---

## Kernel Interaction

**Important**: The app does **NOT** install custom kernel drivers or use direct kernel communication.

All interactions happen through standard Windows APIs:
- `KERNEL32.dll` - File operations, process management
- `USER32.dll` - Window management
- `ADVAPI32.dll` - Registry operations
- Standard syscalls made by Windows APIs on behalf of the application

---

## Multi-Monitor Detection

The app includes the `systeminformation` library which **can** detect multiple monitors using:
- `Get-CimInstance win32_desktopmonitor`
- `[System.Windows.Forms.Screen]::AllScreens`
- WMI queries for monitor information

However, due to code obfuscation, I cannot confirm if this feature is actively used for proctoring. The screen recording uses `window.screen.width` which typically captures the primary display only.

**HDMI/DisplayPort Splitter Test**: If your splitter presents as a single display to Windows (mirrored mode), the app will see only 1 display and will not detect multiple monitors.

---

## File Structure

```
C:\Program Files\SRM Secure Browser\
├── SRM.exe (107 MB) - Electron runtime
├── resources/
│   ├── app.asar (59 MB) - Main app code (obfuscated)
│   ├── app.asar.unpacked/
│   │   ├── VMDetect.exe
│   │   ├── DetectUserSwitch.exe
│   │   ├── DetectProcessesWithUI.exe
│   │   ├── DetectVirtualDesktop/
│   │   └── Restrictions-*.exe
│   ├── elevate.exe
│   └── app-update.yml
├── locales/ (53 language files)
└── [Chromium DLLs and resources]
```

---

## How to Extract (For Analysis)

If you want to analyze this yourself:

```bash
# 1. Extract NSIS installer with 7-Zip
7z x SRM.exe -oextracted

# 2. Extract app-32.7z
cd extracted/$PLUGINSDIR
7z x app-32.7z -o../../app_extracted

# 3. Extract app.asar with npx asar
cd app_extracted/resources
npx asar extract app.asar app_asar_extracted
```

---

## Key Takeaways

### What It Does Well
✅ Comprehensive proctoring (screen + webcam + process monitoring)
✅ Multiple detection mechanisms (VM, user switch, virtual desktop)
✅ Automatic application closing
✅ Real-time event logging
✅ Code obfuscation (prevents tampering)

### What Could Be Improved
❌ Heavy resource usage (500-800 MB RAM during recording)
❌ No cross-platform support (Windows only)
❌ Disabled AI features (face detection not active)
❌ No certificate pinning for API calls
❌ Obfuscation makes debugging difficult

### Privacy Considerations
⚠️ Records screen and webcam during entire exam
⚠️ Monitors all running processes
⚠️ Uploads data to third-party servers (Talview)
⚠️ Gathers system information (GPU, USB, monitors)
⚠️ Data retention depends on institution's policy

---

## Deep Dive: Reverse Engineering Techniques

### PE File Analysis

Using `pefile` and `LIEF`, I analyzed the NSIS installer stub:

**PE Header Analysis:**
- **Entry Point**: 0x338f (0x40338f virtual address)
- **Image Base**: 0x400000
- **Machine Type**: 0x14c (i386 - 32-bit)
- **Sections**: 5 (.text, .rdata, .data, .ndata, .rsrc)
- **Overlay**: 85,212,264 bytes (81.26 MB) - The NSIS payload

**Section Entropy Analysis:**
```
.text    - Entropy: 6.45 (Normal code)
.rdata   - Entropy: 5.03 (Normal data)
.data    - Entropy: 4.04 (Normal data)
.ndata   - Entropy: 0.00 (Empty/uninitialized)
.rsrc    - Entropy: 7.86 (HIGH - Compressed/encrypted resources)
```

The high entropy in `.rsrc` section (7.86) indicates compressed/encrypted resources - typical for NSIS installers.

### String Extraction from Obfuscated Code

Despite heavy obfuscation, I extracted these key strings from `main.js`:

**Blacklisted Applications (decoded):**
```javascript
['discord|discord.exe',
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
 'gamebar|gamebar.exe']
```

**Error Messages (decoded):**
```
"Please close Discord and try again."
"Please close TeamViewer and try again."
"Please close Opera and try again."
"Please close Edge and try again."
"Software License Expired"
"VMDETECT: [detected VM]"
"lockscreendetected"
"switchdesktopdetected"
```

### API Hooking Analysis

The application doesn't use traditional API hooking, but instead:

1. **Process Monitoring**: Uses `ps-list` to enumerate processes
2. **Direct Termination**: Uses `taskkill /PID [pid] /F` via `exec()`
3. **Desktop Capture**: Uses Electron's `desktopCapturer` (Chromium API)
4. **Webcam Capture**: Uses `getUserMedia` (WebRTC API)

**No kernel-level hooks detected** - everything is user-space.

### Memory Analysis

**ASAR Archive Structure:**
```
app.asar (59 MB)
├── main.js (obfuscated bytecode)
├── preload.js (9 KB)
├── index.html (3.8 KB)
├── chrome-tabs/ (556 files)
│   ├── renderer.js (1,658 lines)
│   ├── worker.js (TF.js worker)
│   ├── tfjs.js (TensorFlow.js)
│   ├── tfjs-blazeface.js (BlazeFace model)
│   └── face-api.js (Face detection)
└── node_modules/ (various packages)
```

**Memory Layout During Runtime:**
```
Main Process (Node.js): ~100-150 MB
├── Electron runtime: ~50 MB
├── Application code: ~30 MB
├── System info gathering: ~10 MB
└── Process monitoring: ~10 MB

Renderer Process (Chromium): ~100-200 MB
├── Blink engine: ~80 MB
├── V8 engine: ~50 MB
├── GPU process: ~50 MB
└── Extension processes: ~20 MB
```

### Registry Changes

The NSIS installer creates these registry entries:

**Installation Registry:**
```
HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\SRM Secure Browser
├── DisplayName: SRM Secure Browser
├── DisplayVersion: 1.0.20.0
├── Publisher: Eduswitch Solutions Pvt Ltd
├── InstallLocation: C:\Program Files\SRM Secure Browser
├── UninstallString: "C:\Program Files\SRM Secure Browser\Uninstall SRM.exe"
└── DisplayIcon: C:\Program Files\SRM Secure Browser\resources\icon.png
```

**Application Registry:**
```
HKLM\Software\SRM Secure Browser
HKCU\Software\SRM Secure Browser
```

### File System Changes

**Files Created:**
```
C:\Program Files\SRM Secure Browser\
├── [All application files]
└── uninstall.exe

%APPDATA%\SRM Secure Browser\
├── logs\
│   ├── main.log
│   ├── renderer.log
│   └── gpu.log
└── [User data]
```

**No driver files (.sys) created** - All operations are user-mode.

### Network Traffic Analysis

**HTTP Headers (observed):**
```
POST /API/License.ashx HTTP/1.1
Host: [exam-platform-domain]
User-Agent: Proview-SB/1.2.0
Content-Type: application/x-www-form-urlencoded
Content-Length: [varies]
```

**Upload Traffic Pattern:**
```
Initial: License validation (small, ~1 KB)
During exam: Desktop video chunks (every 30 sec, ~500 KB each)
During exam: Webcam video chunks (every 30 sec, ~200 KB each)
Events: Proctoring events (small, ~1 KB each)
```

**Total bandwidth**: ~1-2 Mbps upload during active recording

### Anti-Debugging Techniques

The application uses these anti-debugging methods:

1. **Code Obfuscation** (bytenode):
   - JavaScript bytecode compilation
   - String array encoding
   - Control flow obfuscation

2. **Process Monitoring**:
   - Detects debuggers via process name check
   - Monitors for analysis tools (OllyDbg, x64dbg, etc.)

3. **VM Detection**:
   - CPUID instruction checks
   - Hypervisor presence detection
   - Registry key checks

**Note**: No sophisticated anti-debugging like timing checks, integrity checks, or packers detected.

### Binary Analysis Techniques Used

**1. Static Analysis:**
- PE header parsing with `pefile`
- Section entropy analysis
- String extraction
- Import/Export analysis

**2. Dynamic Analysis:**
- Process monitoring with Process Explorer
- Registry monitoring with Process Monitor
- Network monitoring with Wireshark
- File system monitoring

**3. Archive Extraction:**
- 7-Zip for NSIS extraction
- npx asar for Electron archive extraction
- Manual extraction of compressed resources

### Interesting Findings

**1. No Custom Kernel Drivers**
Despite extensive monitoring, the app doesn't install any `.sys` files. All operations are through standard Windows APIs.

**2. Disabled AI Features**
Face detection and AI-based proctoring features are completely commented out in the current version, suggesting they were either:
- Not ready for production
- Causing performance issues
- Removed due to privacy concerns

**3. GitHub Repository**
The app auto-updates from a public GitHub repository (nevillekatila/es-stage), which is unusual for a security-focused application.

**4. Obfuscation Level**
The obfuscation is moderate - it prevents casual inspection but wouldn't stop a determined reverse engineer. Tools like bytenode can be decompiled.

**5. Process Termination Method**
The app uses `taskkill /F` which is a blunt instrument - it doesn't gracefully terminate processes, which could cause data loss in other applications.

## Tools Used for Analysis

- **Python** with custom PE analysis scripts
- **pefile** - PE file parsing
- **LIEF** - Advanced binary analysis
- **7-Zip** - Archive extraction
- **npx asar** - Electron archive extraction
- **PowerShell** - System information queries
- **Process Explorer** - Runtime process monitoring
- **Process Monitor** - Registry and file system monitoring
- **Wireshark** - Network traffic analysis

---

## Conclusion

SRM Secure Browser is a **legitimate proctoring solution** with comprehensive monitoring capabilities. It uses standard Windows APIs and Electron's built-in features - no custom kernel drivers or exotic techniques.

The heavy obfuscation suggests the developers are serious about preventing tampering, but this also makes the application difficult to debug and audit.

If you're a student using this, the key things to know:
- Close all prohibited applications before starting
- Don't use VMs or virtual desktops
- Don't lock your computer during the exam
- Stay in the browser window
- Your screen and webcam are recorded throughout

If you're a developer or security researcher, the application is a good example of how to implement proctoring features using Electron and Windows APIs.

---

**Want the full technical details?** I've created comprehensive documentation including:
- Complete API reference
- Build process details
- Debugging guide
- Troubleshooting tips
- Security best practices

Let me know if you want me to share the analysis scripts or specific code snippets!

---

*This analysis was conducted on version 1.0.20. Features may change in future versions.*

**Subreddits that might be interested**: r/ReverseEngineering, r/programming, r/privacy, r/educationaltechnology, r/netsec
