import struct
import re

def analyze_nsis_structure(filepath):
    """Analyze NSIS installer structure"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print("=" * 80)
    print("NSIS INSTALLER ANALYSIS")
    print("=" * 80)
    
    # NSIS signature search
    print("\n[1] NSIS Signature Detection:")
    print("-" * 80)
    
    nsis_signatures = [
        b'Nullsoft',
        b'NSIS',
        b'~NSIS',
    ]
    
    for sig in nsis_signatures:
        pos = data.find(sig)
        if pos != -1:
            print(f"  Found '{sig.decode('ascii')}' at offset 0x{pos:x}")
            
            # Show context around the signature
            context_start = max(0, pos - 32)
            context_end = min(len(data), pos + 64)
            context = data[context_start:context_end]
            print(f"  Context: {context[:100]}")
    
    # Look for NSIS header structure
    # NSIS typically has a specific header structure after the PE section
    print(f"\n[2] Searching for NSIS Data Header:")
    print("-" * 80)
    
    # NSIS 2.x/3.x header typically starts with specific markers
    # Look for the data section which contains compressed install data
    
    # Search for common NSIS markers
    markers = [
        b'\xEB\x03\x90',  # Common jump instruction at start of NSIS data
        b'nsis',  # Lowercase nsis
    ]
    
    for marker in markers:
        positions = []
        start = 0
        while True:
            pos = data.find(marker, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        if positions:
            print(f"  Found marker {marker.hex()} at {len(positions)} positions")
            for p in positions[:5]:
                print(f"    Offset 0x{p:x}")
    
    # Extract strings that might reveal what this installs
    print(f"\n[3] Extracting Installation-Related Strings:")
    print("-" * 80)
    
    # Look for file extensions, paths, and installation-related strings
    interesting_patterns = [
        rb'[\w\-]+\.(exe|dll|bat|cmd|msi|zip|rar|7z|dat|bin|cfg|ini|xml|json)',
        rb'[A-Za-z]:\\[^\x00]{1,100}',  # Windows paths
        rb'Program Files[^\x00]{1,50}',
        rb'\\Install[^\x00]{1,50}',
        rb'\\Temp[^\x00]{1,30}',
        rb'Registry[^\x00]{1,30}',
        rb'Start Menu[^\x00]{1,30}',
        rb'Desktop[^\x00]{1,30}',
    ]
    
    all_strings = []
    for pattern in interesting_patterns:
        matches = re.finditer(pattern, data, re.IGNORECASE)
        for match in matches:
            try:
                s = match.group().decode('ascii', errors='ignore')
                if s not in all_strings and len(s) > 3:
                    all_strings.append(s)
            except:
                pass
    
    # Display unique strings
    seen = set()
    for s in all_strings[:100]:
        if s not in seen:
            print(f"  {s}")
            seen.add(s)
    
    # Look for specific NSIS script commands
    print(f"\n[4] NSIS Script Commands Detection:")
    print("-" * 80)
    
    nsis_commands = [
        b'File ',
        b'Exec ',
        b'ExecWait ',
        b'CreateDirectory ',
        b'Delete ',
        b'CopyFiles ',
        b'Rename ',
        b'WriteRegStr ',
        b'ReadRegStr ',
        b'SetOutPath ',
        b'InstallDir ',
        b'InstallDirRegKey ',
        b'Section ',
        b'Function ',
        b'Page ',
        b'Component ',
    ]
    
    found_commands = []
    for cmd in nsis_commands:
        if cmd in data:
            count = data.count(cmd)
            found_commands.append((cmd.decode('ascii').strip(), count))
    
    if found_commands:
        print("  Found NSIS script commands:")
        for cmd, count in found_commands:
            print(f"    {cmd}: {count} occurrences")
    
    # Analyze the overlay data more carefully
    print(f"\n[5] Overlay Data Analysis:")
    print("-" * 80)
    
    # The overlay starts after the PE structure
    # From previous analysis, overlay starts around 0x21a00
    
    overlay_start = 0x21a00
    overlay_data = data[overlay_start:]
    
    print(f"  Overlay size: {len(overlay_data):,} bytes ({len(overlay_data)/1024/1024:.2f} MB)")
    print(f"  Overlay start offset: 0x{overlay_start:x}")
    
    # Check overlay entropy
    import math
    def calc_entropy(chunk):
        if len(chunk) == 0:
            return 0
        entropy = 0
        for byte in range(256):
            p = chunk.count(byte) / len(chunk)
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    sample_size = min(1048576, len(overlay_data))
    overlay_entropy = calc_entropy(overlay_data[:sample_size])
    print(f"  Overlay entropy (first 1MB): {overlay_entropy:.4f}")
    
    # Look for headers in the overlay that might indicate file structure
    print(f"\n[6] File Headers in Overlay:")
    print("-" * 80)
    
    file_signatures = {
        b'PK\x03\x04': 'ZIP',
        b'PK\x05\x06': 'ZIP end',
        b'7z\xbc\xaf\x27\x1c': '7-Zip',
        b'\x1f\x8b': 'GZIP',
        b'BZh': 'BZIP2',
        b'MZ': 'PE/EXE',
        b'PE\x00\x00': 'PE header',
        b'RIFF': 'RIFF',
        b'\x89PNG': 'PNG',
        b'BM': 'BMP',
        b'GIF8': 'GIF',
    }
    
    for sig, name in file_signatures.items():
        # Search in overlay
        pos = overlay_data.find(sig)
        if pos != -1:
            abs_pos = overlay_start + pos
            print(f"  {name} header at overlay offset 0x{pos:x} (absolute 0x{abs_pos:x})")
    
    # Try to find NSIS-specific data structures
    # NSIS uses a specific format for storing files
    print(f"\n[7] NSIS File Entry Search:")
    print("-" * 80)
    
    # NSIS file entries often have specific patterns
    # Look for sequences that might be file sizes or offsets
    # Search for potential file entry headers
    
    # NSIS 2.x uses 4-byte offsets and sizes
    # Let's look for patterns that might indicate file entries
    
    # Look for registry keys
    print(f"\n[8] Registry Key Patterns:")
    print("-" * 80)
    
    registry_patterns = [
        b'SOFTWARE\\',
        b'HKEY_LOCAL_MACHINE',
        b'HKEY_CURRENT_USER',
        b'HKLM\\',
        b'HKCU\\',
    ]
    
    for pattern in registry_patterns:
        positions = []
        start = 0
        while True:
            pos = overlay_data.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
            if len(positions) > 20:
                break
        
        if positions:
            print(f"  {pattern.decode('ascii')}: {len(positions)} occurrences")
            for p in positions[:5]:
                # Extract context
                ctx_start = max(0, p - 10)
                ctx_end = min(len(overlay_data), p + 50)
                try:
                    ctx = overlay_data[ctx_start:ctx_end].decode('ascii', errors='ignore')
                    print(f"    0x{overlay_start + p:x}: {ctx[:80]}")
                except:
                    pass

if __name__ == '__main__':
    exe_path = r'c:\Nan\AI\sacy\SRM.exe'
    analyze_nsis_structure(exe_path)
