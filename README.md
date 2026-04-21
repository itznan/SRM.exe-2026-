# SRM.exe Reverse Engineering Analysis

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

## Overview

This repository contains a comprehensive reverse engineering analysis of **SRM.exe** (SRM Secure Browser v1.0.20), a proctored exam browser application developed by Eduswitch Solutions Pvt Ltd.

**Project Information:**
- **File Size**: 81.4 MB (85,349,992 bytes)
- **Format**: NSIS-3 Unicode installer
- **Product**: SRM Secure Browser
- **Version**: 1.0.20.0
- **Company**: Eduswitch Solutions Pvt Ltd
- **Technology**: Electron (Chromium + Node.js)

## Quick Start

### Running Analysis Scripts

```bash
# PE file structure analysis
python scripts/analyze_exe.py

# Deep entropy and embedded file analysis
python scripts/deep_analyze.py

# NSIS installer structure analysis
python scripts/analyze_nsis.py

# Advanced PE analysis with pefile and LIEF
python scripts/advanced_pe_analysis.py

# Monitor detection (same method as SRM.exe)
python scripts/detect_monitors.py
```

### Documentation

- **[README.md](README.md)** - This file (reverse engineering findings)
- **[docs/TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md)** - Complete technical documentation
- **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - User guide for end users
- **[docs/REDDIT_POST.md](docs/REDDIT_POST.md)** - Reddit-formatted analysis post

## Analysis Tools Used

- **Python** with custom PE analysis scripts
- **7-Zip** for archive extraction
- **npx asar** for Electron archive extraction
- **Entropy analysis** for packing detection

## Technical Architecture

### 1. Installer Layer (NSIS)

The executable is a Nullsoft Scriptable Install System (NSIS) installer with the following structure:

```
SRM.exe
├── NSIS Stub (~136 KB)
│   ├── Valid PE structure
│   ├── Entry point: 0x338f
│   └── Imports: KERNEL32.dll, USER32.dll, GDI32.dll, SHELL32.dll, ADVAPI32.dll
└── Payload Overlay (~81.26 MB)
    ├── Compressed installation data
    ├── High entropy (7.98-7.99)
    └── Contains embedded 7-Zip archives
```

### 2. Application Layer (Electron)

The actual application is built with the Electron framework:

```
SRM (Electron App)
├── SRM.exe (107 MB) - Electron runtime
├── app.asar (59 MB) - Main application code (obfuscated)
├── app.asar.unpacked/ - Unpacked executables
│   ├── VMDetect.exe - Virtual machine detection
│   ├── DetectUserSwitch.exe - User switch detection
│   ├── DetectProcessesWithUI.exe - Process monitoring
│   ├── DetectVirtualDesktop/ - Virtual desktop detection
│   ├── Restrictions-DiableWinKey-WinFormsApp.exe - System restrictions
│   └── DiableWinKey-WinFormsApp-DisableRestrictions.exe - Additional controls
├── resources/
│   ├── icon.png
│   └── elevate.exe
└── Chromium components
    ├── chrome_100_percent.pak
    ├── chrome_200_percent.pak
    ├── resources.pak
    ├── icudtl.dat
    ├── v8_context_snapshot.bin
    └── Various DLLs (ffmpeg, libEGL, libGLESv2, etc.)
```

## How It Works

### Installation Process

1. User executes SRM.exe
2. NSIS stub extracts the compressed payload
3. Application files are installed to the system
4. Registry entries are created
5. Uninstaller is registered

### Runtime Behavior

1. **Application Launch**
   - Electron runtime starts with main.js (obfuscated)
   - Creates a browser window
   - Loads a webview pointing to `https://talview.page.link/nco9`

2. **Proctoring System Activation**
   - Starts monitoring running processes
   - Activates VM detection
   - Enables user switch detection
   - Applies system restrictions

3. **Exam Session**
   - Student takes exam through the secure browser
   - Proctoring features monitor for violations
   - System restrictions prevent cheating

## Anti-Cheating Measures

### Blocked Applications
The application blocks the following processes:
- Discord
- TeamViewer
- Skype
- WebEx
- GoToMeeting
- Ammyy Admin
- Opera
- Microsoft Edge
- Zoom

### System Restrictions
- Disables Windows key
- Blocks keyboard shortcuts (Ctrl+Shift+Q+E, CmdOrCtrl+C)
- Prevents screen capture
- Detects and blocks virtual machine environments
- Detects virtual desktop usage
- Monitors for user account switching

### Detection Mechanisms

1. **VM Detection** (`VMDetect.exe`)
   - Detects virtual machine environments
   - Prevents sandboxing

2. **Process Monitoring** (`DetectProcessesWithUI.exe`)
   - Continuously monitors running processes
   - Alerts on prohibited applications

3. **User Switch Detection** (`DetectUserSwitch.exe`)
   - Detects when user switches accounts
   - May pause or terminate exam session

4. **Virtual Desktop Detection** (`DetectVirtualDesktop/`)
   - Detects virtual desktop usage
   - Prevents isolation techniques

## Network Communication

- **Primary URL**: `https://talview.page.link/nco9` (Talview exam platform)
- **License Validation**: HTTP requests to license server
- **Auto-Update**: GitHub releases (nevillekatila/es-stage)
- **Update Cache**: `srmug-secure-browser-updater`

## Dependencies

### Node.js Dependencies
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

## Security Analysis

### Legitimate Purpose
- Designed for online exam proctoring
- Used by educational institutions
- Integrates with Talview exam platform

### Privacy Considerations
- **Process Monitoring**: Continuously monitors running applications
- **System Information**: Gathers system details
- **Network Activity**: Communicates with exam servers

### What It Does NOT Do
- No evidence of data exfiltration
- No evidence of keylogging
- No evidence of unauthorized remote access
- Appears to be a legitimate proctoring solution

## Extraction Process

### Step 1: Extract NSIS Installer
```bash
7z x SRM.exe -oextracted
```

### Step 2: Extract Application Archive
```bash
cd extracted/$PLUGINSDIR
7z x app-32.7z -o../../app_extracted
```

### Step 3: Extract Electron ASAR
```bash
cd app_extracted/resources
npx asar extract app.asar app_asar_extracted
```

## File Structure After Extraction

```
c:/Nan/AI/sacy/
├── SRM.exe                          # Original installer
├── extracted/                        # NSIS extraction
│   ├── $PLUGINSDIR/
│   │   ├── app-32.7z
│   │   ├── StdUtils.dll
│   │   ├── System.dll
│   │   ├── UAC.dll
│   │   ├── WinShell.dll
│   │   ├── nsDialogs.dll
│   │   ├── nsExec.dll
│   │   └── nsis7z.dll
│   ├── $R0/
│   │   └── Uninstall SRM.exe
│   └── resources/
│       └── icon.png
└── app_extracted/                    # Application extraction
    ├── SRM.exe
    ├── LICENSE.electron.txt
    ├── LICENSES.chromium.html
    ├── resources/
    │   ├── app.asar
    │   ├── app.asar.unpacked/
    │   ├── app-update.yml
    │   └── elevate.exe
    ├── locales/                     # 53 language files
    └── [Chromium components]
```

## Key Findings

### Obfuscation
- **main.js** is heavily obfuscated using JavaScript bytecode (bytenode)
- String encoding used throughout the codebase
- Likely to prevent students from bypassing proctoring controls

### GitHub Repository
- **Owner**: nevillekatila
- **Repository**: es-stage
- **Provider**: GitHub
- **Release Type**: Draft

### Update Mechanism
- Uses electron-builder for auto-updates
- Checks GitHub releases for updates
- Caches updates in `srmug-secure-browser-updater` directory

## Conclusion

SRM.exe is a **legitimate secure browser application for online exam proctoring**. It creates a controlled browser environment that prevents cheating by:

1. Restricting access to other applications
2. Monitoring system state and processes
3. Detecting virtual environments
4. Enforcing browser and system restrictions

The application is developed by Eduswitch Solutions Pvt Ltd and integrates with the Talview exam platform. The obfuscation of the code is a security measure to prevent students from bypassing the proctoring controls.

## Analysis Scripts

The following Python scripts are located in the `scripts/` directory:

- **analyze_exe.py**: PE file structure analysis
- **deep_analyze.py**: Entropy analysis and embedded file detection
- **analyze_nsis.py**: NSIS installer structure analysis
- **advanced_pe_analysis.py**: Advanced PE analysis using pefile and LIEF
- **detect_monitors.py**: Monitor detection using PowerShell (same method as SRM.exe)

These scripts can be used to analyze similar NSIS installers or PE files.

## References

- [NSIS Documentation](https://nsis.sourceforge.io/)
- [Electron Documentation](https://www.electronjs.org/)
- [Talview Platform](https://www.talview.com/)
- [Eduswitch Solutions](https://www.eduswitch.com/)
