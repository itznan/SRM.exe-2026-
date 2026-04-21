# SRM Secure Browser - User Guide

## What is SRM Secure Browser?

SRM Secure Browser is a proctored exam browser designed to ensure fair and secure online testing. It creates a controlled environment that prevents cheating during exams by monitoring your computer and restricting access to certain applications.

## Features

### ✅ What It Does
- **Secure Exam Environment**: Locks your browser to the exam platform
- **Screen Recording**: Records your screen during the exam for proctoring
- **Webcam Recording**: Records your webcam to monitor test-taker identity
- **Process Monitoring**: Detects and closes applications that could be used for cheating
- **VM Detection**: Prevents running in virtual machine environments
- **User Switch Detection**: Detects if you switch user accounts during the exam
- **System Restrictions**: Disables certain keyboard shortcuts and system features

### 🔒 Security Features
- Monitors running processes every 5 seconds
- Automatically closes prohibited applications
- Detects virtual desktop usage
- Detects screen lock/unlock events
- Records desktop and webcam video
- Uploads proctoring data to secure servers

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 7 or later (32-bit or 64-bit)
- **Processor**: Intel Core i3 or equivalent
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 500 MB free disk space
- **Internet**: Stable broadband connection
- **Webcam**: Required for identity verification
- **Microphone**: Required (if exam requires audio monitoring)

### Supported Browsers
- SRM Secure Browser uses its own built-in Chromium-based browser
- No external browser installation required

## Installation

### Step 1: Download
Download the SRM Secure Browser installer (SRM.exe) from your institution's exam portal or the provided link.

### Step 2: Run Installer
1. Double-click `SRM.exe`
2. Follow the on-screen installation wizard
3. Choose your preferred installation location (default: `C:\Program Files\SRM Secure Browser`)
4. Wait for installation to complete
5. Desktop shortcut will be created automatically

### Step 3: Launch
Double-click the SRM Secure Browser icon on your desktop to launch the application.

## Using SRM Secure Browser

### Before the Exam

1. **Close All Applications**
   - Close all browsers (Chrome, Firefox, Edge, etc.)
   - Close communication apps (Discord, Skype, Slack, Telegram)
   - Close remote access tools (TeamViewer, AnyDesk, Zoom)
   - Close screen recording software (OBS, CamRecorder)
   - Close any other unnecessary applications

2. **Check Your Setup**
   - Ensure webcam is working
   - Ensure microphone is working (if required)
   - Check internet connection stability
   - Close any VPN or proxy software
   - Disable Windows notifications

3. **Test Your Equipment**
   - Test webcam in Windows Camera app
   - Test microphone in Windows Sound settings
   - Ensure you have a stable power source

### During the Exam

1. **Launch the Browser**
   - Open SRM Secure Browser
   - Enter your exam credentials when prompted
   - Wait for the exam platform to load

2. **Proctoring Activation**
   - Allow webcam access when prompted
   - Allow microphone access when prompted
   - Allow screen recording when prompted
   - Wait for proctoring system to initialize

3. **Taking the Exam**
   - Take your exam in the secure browser window
   - Do not switch to other applications
   - Do not lock your computer
   - Do not switch user accounts
   - Do not use virtual desktops
   - Stay in front of your webcam

4. **What's Monitored**
   - Your screen is recorded at 2 FPS
   - Your webcam is recorded at 5-10 FPS
   - Running processes are monitored every 5 seconds
   - Screen focus is tracked
   - User activity is logged

### After the Exam

1. **Submit Your Exam**
   - Complete all questions
   - Submit your exam through the platform
   - Wait for confirmation

2. **Close the Browser**
   - The browser will close automatically after submission
   - Proctoring data will be uploaded automatically
   - You can close the application manually if needed

3. **Normal Operation**
   - After closing, your computer returns to normal operation
   - All restrictions are lifted
   - You can use other applications normally

## Prohibited Applications

The following applications will be **automatically closed** when SRM Secure Browser runs:

### Communication Apps
- Discord, Skype, Slack, Telegram, WebEx

### Remote Access Tools
- TeamViewer, AnyDesk, Ammyy Admin, Join.me, GoToMeeting, Zoom

### Web Browsers
- Chrome, Firefox, Opera, Edge, Safari, SeaMonkey

### Screen Recording
- OBS Studio, CamRecorder, CamPlay

### Other
- Windows Game Bar, Element (Matrix client)

**Note**: If any of these applications are running, SRM Secure Browser will automatically close them. Please close them manually before starting the exam.

## Troubleshooting

### Installation Issues

**Problem**: Installer won't run
- **Solution**: Right-click SRM.exe and select "Run as Administrator"
- **Solution**: Disable antivirus temporarily during installation
- **Solution**: Ensure you have sufficient disk space

**Problem**: Installation fails
- **Solution**: Check Windows Event Viewer for error details
- **Solution**: Ensure .NET Framework 4.5+ is installed
- **Solution**: Restart your computer and try again

### Launch Issues

**Problem**: Browser won't open
- **Solution**: Check internet connection
- **Solution**: Restart the application
- **Solution**: Check if Windows Firewall is blocking it
- **Solution**: Run as Administrator

**Problem**: Exam platform won't load
- **Solution**: Check your internet connection
- **Solution**: Clear browser cache (if applicable)
- **Solution**: Contact your institution's IT support
- **Solution**: Check if exam portal is accessible in regular browser

### Webcam/Microphone Issues

**Problem**: Webcam not detected
- **Solution**: Check if webcam is connected properly
- **Solution**: Ensure webcam drivers are installed
- **Solution**: Test webcam in Windows Camera app
- **Solution**: Check Windows privacy settings (Settings > Privacy > Camera)

**Problem**: Microphone not detected
- **Solution**: Check if microphone is connected properly
- **Solution**: Ensure microphone drivers are installed
- **Solution**: Test microphone in Windows Sound settings
- **Solution**: Check Windows privacy settings (Settings > Privacy > Microphone)

### Proctoring Issues

**Problem**: "Prohibited application detected" error
- **Solution**: Close all prohibited applications listed above
- **Solution**: Check Task Manager for running processes
- **Solution**: Restart your computer to clear stuck processes

**Problem**: "Virtual machine detected" error
- **Solution**: SRM Secure Browser cannot run in virtual machines
- **Solution**: Use a physical computer instead
- **Solution**: Contact your institution if you only have a VM available

**Problem**: Screen recording not working
- **Solution**: Ensure you granted screen recording permission
- **Solution**: Check if Windows Game Bar is disabled
- **Solution**: Restart the application

### Performance Issues

**Problem**: Browser is slow
- **Solution**: Close other applications to free up RAM
- **Solution**: Check internet connection speed
- **Solution**: Restart your computer
- **Solution**: Ensure you meet minimum system requirements

**Problem**: Computer freezes during exam
- **Solution**: This may be due to resource-intensive proctoring
- **Solution**: Close all other applications
- **Solution**: Ensure your computer meets recommended specs

## Tips for a Smooth Exam Experience

### Before the Exam
1. **Test your equipment** 30 minutes before the exam
2. **Close all applications** before launching SRM Secure Browser
3. **Use a stable internet connection** (wired preferred over WiFi)
4. **Ensure your computer is plugged in** to prevent battery issues
5. **Find a quiet, well-lit room** for the exam
6. **Have your ID ready** for verification if required

### During the Exam
1. **Stay in the secure browser window** - don't switch applications
2. **Keep your face visible** to the webcam
3. **Don't lock your computer** during the exam
4. **Don't use virtual desktops** or multiple monitors
5. **Don't use external devices** (phones, tablets) during the exam
6. **Stay focused** on the exam to avoid time running out

### After the Exam
1. **Wait for confirmation** that your exam was submitted
2. **Don't close the browser** until submission is complete
3. **Keep the browser open** until proctoring data uploads
4. **Contact support** if you encounter any issues

## Privacy and Data

### What is Recorded
- Screen video (2 FPS)
- Webcam video (5-10 FPS)
- Running processes
- System information
- Exam responses

### Data Storage
- Proctoring data is uploaded to secure servers
- Data is encrypted during transmission
- Data is stored according to your institution's privacy policy
- Data is typically retained for a specified period after the exam

### Your Rights
- You have the right to know what data is collected
- You have the right to access your data
- You have the right to request data deletion (where applicable)
- Contact your institution for privacy-related questions

## Uninstallation

### To Remove SRM Secure Browser

1. **Open Control Panel**
   - Press `Win + R`
   - Type `control`
   - Press Enter

2. **Uninstall the Application**
   - Go to "Programs and Features"
   - Find "SRM Secure Browser"
   - Click "Uninstall"
   - Follow the uninstallation wizard

3. **Clean Up**
   - Delete the installation folder if it remains
   - Delete desktop shortcut if desired
   - Restart your computer

## Support

### Getting Help

If you encounter issues during the exam:

1. **Contact Your Institution**
   - Use the provided support contact
   - Include error messages and screenshots
   - Describe what you were doing when the error occurred

2. **Technical Requirements**
   - Ensure you meet all system requirements
   - Check that your equipment is working properly
   - Test your setup before the exam

3. **Emergency Contacts**
   - Keep your institution's IT support number handy
   - Have a backup device ready if possible
   - Know the exam rescheduling policy

## FAQ

**Q: Can I use multiple monitors?**
A: While the app may detect multiple monitors, it's recommended to use a single monitor during exams to avoid issues.

**Q: Can I use a VPN?**
A: No, VPNs and proxies should be disabled before starting the exam.

**Q: What if my internet disconnects during the exam?**
A: The exam may pause or you may lose time. Reconnect as quickly as possible and contact support if needed.

**Q: Can I use keyboard shortcuts?**
A: Most keyboard shortcuts are disabled during the exam, including the Windows key, Ctrl+C, and others.

**Q: Will the app work on Mac or Linux?**
A: Currently, SRM Secure Browser is only available for Windows.

**Q: How long does proctoring data take to upload?**
A: Upload time depends on your internet speed, but typically completes within a few minutes after the exam.

**Q: Can I pause the exam and resume later?**
A: This depends on your institution's exam policy. Check with your exam administrator.

**Q: What happens if I accidentally close the browser?**
A: You may be able to reconnect to the exam, but this depends on your institution's policy. Contact support immediately.

**Q: Is my webcam recording stored?**
A: Yes, webcam recordings are stored on secure servers for proctoring purposes and are handled according to your institution's privacy policy.

## Version Information

- **Current Version**: 1.0.20
- **Developer**: Eduswitch Solutions Pvt Ltd
- **Platform**: Windows 7+
- **Architecture**: 32-bit/64-bit compatible

## Legal Information

SRM Secure Browser is designed for legitimate exam proctoring purposes. By using this software, you agree to:
- Use it only for authorized exam purposes
- Not attempt to bypass security features
- Not attempt to reverse engineer the application
- Comply with your institution's academic integrity policies

Unauthorized use or attempts to bypass security features may result in exam disqualification and academic penalties.

---

**For technical support, please contact your institution's IT helpdesk or exam administrator.**
