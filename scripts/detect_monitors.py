import subprocess
import json
import re

def get_monitor_info_powershell():
    """Get monitor information using PowerShell (same method as SRM.exe)"""
    print("=" * 80)
    print("MONITOR DETECTION USING POWERSHELL (Same method as SRM.exe)")
    print("=" * 80)
    
    results = {}
    
    # Method 1: Get-CimInstance win32_desktopmonitor
    print("\n[1] Desktop Monitor Information:")
    print("-" * 80)
    try:
        ps_command = "Get-CimInstance win32_desktopmonitor | Select-Object DeviceName, ScreenHeight, ScreenWidth, MonitorType, DisplayName | ConvertTo-Json"
        output = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True)
        
        if output.stdout:
            try:
                monitors = json.loads(output.stdout)
                if isinstance(monitors, dict):
                    monitors = [monitors]
                
                print(f"  Total monitors detected: {len(monitors)}")
                for i, monitor in enumerate(monitors, 1):
                    print(f"\n  Monitor {i}:")
                    print(f"    Device Name: {monitor.get('DeviceName', 'N/A')}")
                    print(f"    Screen Height: {monitor.get('ScreenHeight', 'N/A')}")
                    print(f"    Screen Width: {monitor.get('ScreenWidth', 'N/A')}")
                    print(f"    Monitor Type: {monitor.get('MonitorType', 'N/A')}")
                    print(f"    Display Name: {monitor.get('DisplayName', 'N/A')}")
                
                results['desktop_monitors'] = monitors
            except json.JSONDecodeError:
                print("  Could not parse JSON output")
                print(f"  Raw output: {output.stdout[:500]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Method 2: Get-CimInstance WmiMonitorBasicDisplayParams
    print("\n[2] WMI Monitor Basic Display Parameters:")
    print("-" * 80)
    try:
        ps_command = "Get-CimInstance -Namespace root\\wmi -ClassName WmiMonitorBasicDisplayParams | Select-Object InstanceName, Active, MaxHorizontalImageSize, MaxVerticalImageSize, DisplayTransferCharacteristic | ConvertTo-Json"
        output = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True)
        
        if output.stdout:
            try:
                monitor_params = json.loads(output.stdout)
                if isinstance(monitor_params, dict):
                    monitor_params = [monitor_params]
                
                print(f"  Total monitor parameters: {len(monitor_params)}")
                for i, params in enumerate(monitor_params, 1):
                    print(f"\n  Monitor {i}:")
                    print(f"    Instance Name: {params.get('InstanceName', 'N/A')}")
                    print(f"    Active: {params.get('Active', 'N/A')}")
                    print(f"    Max Horizontal Image Size: {params.get('MaxHorizontalImageSize', 'N/A')}")
                    print(f"    Max Vertical Image Size: {params.get('MaxVerticalImageSize', 'N/A')}")
                    print(f"    Display Transfer Characteristic: {params.get('DisplayTransferCharacteristic', 'N/A')}")
                
                results['wmi_display_params'] = monitor_params
            except json.JSONDecodeError:
                print("  Could not parse JSON output")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Method 3: Get-CimInstance WmiMonitorConnectionParams
    print("\n[3] WMI Monitor Connection Parameters:")
    print("-" * 80)
    try:
        ps_command = "Get-CimInstance -Namespace root\\wmi -ClassName WmiMonitorConnectionParams | Select-Object InstanceName, VideoInputTechnology, TechnologyType, OutputTechnology | ConvertTo-Json"
        output = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True)
        
        if output.stdout:
            try:
                connection_params = json.loads(output.stdout)
                if isinstance(connection_params, dict):
                    connection_params = [connection_params]
                
                print(f"  Total connection parameters: {len(connection_params)}")
                for i, params in enumerate(connection_params, 1):
                    print(f"\n  Monitor {i}:")
                    print(f"    Instance Name: {params.get('InstanceName', 'N/A')}")
                    print(f"    Video Input Technology: {params.get('VideoInputTechnology', 'N/A')}")
                    print(f"    Technology Type: {params.get('TechnologyType', 'N/A')}")
                    print(f"    Output Technology: {params.get('OutputTechnology', 'N/A')}")
                
                results['wmi_connection_params'] = connection_params
            except json.JSONDecodeError:
                print("  Could not parse JSON output")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Method 4: WmiMonitorID (Manufacturer, Product Code, Serial Number)
    print("\n[4] WMI Monitor ID (Manufacturer, Product, Serial):")
    print("-" * 80)
    try:
        ps_command = """
        $monitors = gwmi WmiMonitorID -Namespace root\\wmi
        $monitors | ForEach-Object {
            [PSCustomObject]@{
                ManufacturerName = if ($_.ManufacturerName) { ($_.ManufacturerName -notmatch 0 | foreach {[char]$_}) -join "" } else { "N/A" }
                ProductCodeID = if ($_.ProductCodeID) { ($_.ProductCodeID -notmatch 0 | foreach {[char]$_}) -join "" } else { "N/A" }
                UserFriendlyName = if ($_.UserFriendlyName) { ($_.UserFriendlyName -notmatch 0 | foreach {[char]$_}) -join "" } else { "N/A" }
                SerialNumberID = if ($_.SerialNumberID) { ($_.SerialNumberID -notmatch 0 | foreach {[char]$_}) -join "" } else { "N/A" }
                InstanceName = $_.InstanceName
            }
        } | ConvertTo-Json
        """
        output = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True)
        
        if output.stdout:
            try:
                monitor_ids = json.loads(output.stdout)
                if isinstance(monitor_ids, dict):
                    monitor_ids = [monitor_ids]
                
                print(f"  Total monitor IDs: {len(monitor_ids)}")
                for i, monitor_id in enumerate(monitor_ids, 1):
                    print(f"\n  Monitor {i}:")
                    print(f"    Manufacturer: {monitor_id.get('ManufacturerName', 'N/A')}")
                    print(f"    Product Code: {monitor_id.get('ProductCodeID', 'N/A')}")
                    print(f"    User Friendly Name: {monitor_id.get('UserFriendlyName', 'N/A')}")
                    print(f"    Serial Number: {monitor_id.get('SerialNumberID', 'N/A')}")
                    print(f"    Instance Name: {monitor_id.get('InstanceName', 'N/A')}")
                
                results['wmi_monitor_ids'] = monitor_ids
            except json.JSONDecodeError:
                print("  Could not parse JSON output")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Method 5: System.Windows.Forms.Screen.AllScreens
    print("\n[5] All Screens (System.Windows.Forms):")
    print("-" * 80)
    try:
        ps_command = """
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
            [PSCustomObject]@{
                DeviceName = $_.DeviceName
                Bounds = $_.Bounds.ToString()
                WorkingArea = $_.WorkingArea.ToString()
                Primary = $_.Primary
                BitsPerPixel = $_.BitsPerPixel
            }
        } | ConvertTo-Json
        """
        output = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True)
        
        if output.stdout:
            try:
                screens = json.loads(output.stdout)
                if isinstance(screens, dict):
                    screens = [screens]
                
                print(f"  Total screens detected: {len(screens)}")
                for i, screen in enumerate(screens, 1):
                    print(f"\n  Screen {i}:")
                    print(f"    Device Name: {screen.get('DeviceName', 'N/A')}")
                    print(f"    Bounds: {screen.get('Bounds', 'N/A')}")
                    print(f"    Working Area: {screen.get('WorkingArea', 'N/A')}")
                    print(f"    Primary Display: {screen.get('Primary', 'N/A')}")
                    print(f"    Bits Per Pixel: {screen.get('BitsPerPixel', 'N/A')}")
                
                results['all_screens'] = screens
            except json.JSONDecodeError:
                print("  Could not parse JSON output")
    except Exception as e:
        print(f"  Error: {e}")
    
    return results

def get_display_config():
    """Get display configuration using wmic"""
    print("\n" + "=" * 80)
    print("DISPLAY CONFIGURATION USING WMIC")
    print("=" * 80)
    
    try:
        ps_command = "wmic desktopmonitor get Name, MonitorType, ScreenHeight, ScreenWidth /format:list"
        output = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True)
        
        print("\nDesktop Monitor Configuration:")
        print("-" * 80)
        for line in output.stdout.split('\n'):
            if line.strip():
                print(f"  {line}")
    except Exception as e:
        print(f"  Error: {e}")

def get_graphics_info():
    """Get graphics adapter information"""
    print("\n" + "=" * 80)
    print("GRAPHICS ADAPTER INFORMATION")
    print("=" * 80)
    
    try:
        ps_command = "Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion, AdapterRAM, CurrentHorizontalResolution, CurrentVerticalResolution | ConvertTo-Json"
        output = subprocess.run(["powershell", "-Command", ps_command], 
                              capture_output=True, text=True)
        
        if output.stdout:
            try:
                graphics = json.loads(output.stdout)
                if isinstance(graphics, dict):
                    graphics = [graphics]
                
                print(f"  Total graphics adapters: {len(graphics)}")
                for i, gpu in enumerate(graphics, 1):
                    print(f"\n  Graphics Adapter {i}:")
                    print(f"    Name: {gpu.get('Name', 'N/A')}")
                    print(f"    Driver Version: {gpu.get('DriverVersion', 'N/A')}")
                    print(f"    Adapter RAM: {gpu.get('AdapterRAM', 'N/A')} bytes")
                    print(f"    Current Resolution: {gpu.get('CurrentHorizontalResolution', 'N/A')}x{gpu.get('CurrentVerticalResolution', 'N/A')}")
            except json.JSONDecodeError:
                print("  Could not parse JSON output")
    except Exception as e:
        print(f"  Error: {e}")

def summary(results):
    """Print summary of findings"""
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total_monitors = 0
    
    if 'desktop_monitors' in results:
        total_monitors = max(total_monitors, len(results['desktop_monitors']))
    
    if 'all_screens' in results:
        total_monitors = max(total_monitors, len(results['all_screens']))
    
    if 'wmi_display_params' in results:
        total_monitors = max(total_monitors, len(results['wmi_display_params']))
    
    print(f"\nTotal Displays Detected: {total_monitors}")
    
    if total_monitors > 1:
        print("\n⚠️  MULTIPLE DISPLAYS DETECTED")
        print("   SRM.exe may detect this if it uses monitor detection features")
    else:
        print("\n✓ Single display detected")

if __name__ == '__main__':
    results = get_monitor_info_powershell()
    get_display_config()
    get_graphics_info()
    summary(results)
