import struct
import math

def calculate_entropy(data, block_size=4096):
    """Calculate Shannon entropy of data"""
    if len(data) == 0:
        return 0
    
    entropy = 0
    for byte in range(256):
        p = data.count(byte) / len(data)
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy

def analyze_file_structure(filepath):
    """Deep analysis of file structure"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print("=" * 80)
    print("DEEP FILE STRUCTURE ANALYSIS")
    print("=" * 80)
    
    # Hex dump of first 512 bytes
    print("\n[1] Hex dump of first 512 bytes:")
    print("-" * 80)
    for i in range(0, min(512, len(data)), 32):
        hex_part = ' '.join(f'{b:02x}' for b in data[i:i+32])
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+32])
        print(f"{i:04x}: {hex_part:<80} {ascii_part}")
    
    # Entropy analysis
    print(f"\n[2] Entropy Analysis:")
    print("-" * 80)
    block_size = 65536  # 64KB blocks
    num_blocks = min(50, len(data) // block_size)
    
    high_entropy_blocks = []
    for i in range(num_blocks):
        block = data[i*block_size:(i+1)*block_size]
        entropy = calculate_entropy(block)
        print(f"  Block {i} (offset 0x{i*block_size:x}): {entropy:.4f}")
        if entropy > 7.5:
            high_entropy_blocks.append((i, entropy))
    
    print(f"\n  High entropy blocks (>7.5): {len(high_entropy_blocks)}")
    for block_idx, ent in high_entropy_blocks[:10]:
        print(f"    Block {block_idx}: {ent:.4f}")
    
    # Overall entropy
    overall_entropy = calculate_entropy(data[:min(1048576, len(data))])
    print(f"  Overall entropy (first 1MB): {overall_entropy:.4f}")
    
    if overall_entropy > 7.5:
        print("  -> File appears to be PACKED or ENCRYPTED")
    
    # Search for embedded file signatures
    print(f"\n[3] Embedded File Signatures:")
    print("-" * 80)
    
    signatures = {
        b'PK\x03\x04': 'ZIP archive',
        b'PK\x05\x06': 'ZIP archive (end)',
        b'Rar!': 'RAR archive',
        b'7z\xbc\xaf\x27\x1c': '7-Zip archive',
        b'\x1f\x8b': 'GZIP archive',
        b'BZh': 'BZIP2 archive',
        b'MZ': 'PE/DOS executable',
        b'PE\x00\x00': 'PE header',
        b'\xca\xfe\xba\xbe': 'Mach-O binary (fat)',
        b'\xfe\xed\xfa\xce': 'Mach-O binary (32-bit)',
        b'\xfe\xed\xfa\xcf': 'Mach-O binary (64-bit)',
        b'\x7fELF': 'ELF executable',
        b'\x25PDF': 'PDF document',
        b'%PDF': 'PDF document',
        b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'OLE compound document',
        b'fLaC': 'FLAC audio',
        b'ID3': 'MP3 audio',
        b'\xff\xfb': 'MP3 audio',
        b'\xff\xfa': 'MP3 audio',
        b'\x49\x44\x33': 'MP3 audio',
        b'RIFF': 'RIFF container (WAV, AVI, etc)',
        b'\x00\x00\x01\x00': 'ICO icon',
        b'\x00\x00\x02\x00': 'CUR cursor',
        b'BM': 'BMP image',
        b'\x89PNG': 'PNG image',
        b'GIF8': 'GIF image',
        b'II*\x00': 'TIFF image (little-endian)',
        b'MM\x00*': 'TIFF image (big-endian)',
        b'JFIF': 'JPEG image',
        b'\xff\xd8\xff': 'JPEG image',
    }
    
    found_signatures = []
    for sig, desc in signatures.items():
        pos = data.find(sig)
        if pos != -1:
            found_signatures.append((pos, sig, desc))
            print(f"  Found '{desc}' at offset 0x{pos:x}")
    
    if not found_signatures:
        print("  No known file signatures found")
    
    # Search for PE headers at various offsets
    print(f"\n[4] Searching for PE headers:")
    print("-" * 80)
    pe_signatures = []
    for i in range(len(data) - 4):
        if data[i:i+4] == b'PE\x00\x00':
            pe_signatures.append(i)
    
    print(f"  Found {len(pe_signatures)} PE signatures")
    for idx, offset in enumerate(pe_signatures[:10]):
        print(f"    PE #{idx+1} at offset 0x{offset:x}")
    
    # Check if it's a self-extracting archive
    print(f"\n[5] Self-Extracting Archive Detection:")
    print("-" * 80)
    
    # Look for installer strings
    installer_strings = [
        b'NSIS', b'Nullsoft', b'Install', b'Setup', b'Wizard',
        b'Inno Setup', b'Wise Installation', b'InstallShield',
        b'WinZip Self-Extractor', b'7-Zip Self-Extracting',
        b'Microsoft Cabinet', b'MSI', b'Windows Installer'
    ]
    
    found_installer = []
    for s in installer_strings:
        if s.lower() in data.lower():
            found_installer.append(s.decode('ascii', errors='ignore'))
    
    if found_installer:
        print("  Installer signatures found:")
        for s in found_installer:
            print(f"    - {s}")
    else:
        print("  No common installer signatures found")
    
    # Resource section analysis
    print(f"\n[6] Resource-like patterns:")
    print("-" * 80)
    
    # Look for repeated patterns that might indicate resources
    # Search for common resource types
    resource_types = {
        1: 'RT_CURSOR',
        2: 'RT_BITMAP',
        3: 'RT_ICON',
        4: 'RT_MENU',
        5: 'RT_DIALOG',
        6: 'RT_STRING',
        7: 'RT_FONTDIR',
        8: 'RT_FONT',
        9: 'RT_ACCELERATOR',
        10: 'RT_RCDATA',
        11: 'RT_MESSAGETABLE',
        12: 'RT_GROUP_CURSOR',
        14: 'RT_GROUP_ICON',
        16: 'RT_VERSION',
        23: 'RT_MANIFEST',
        24: 'RT_DLGINCLUDE',
    }
    
    # Look for version info patterns
    version_pattern = b'VS_VERSION_INFO'
    pos = data.find(version_pattern)
    if pos != -1:
        print(f"  Found VS_VERSION_INFO at offset 0x{pos:x}")
    
    # Analyze the structure more carefully
    print(f"\n[7] Detailed Header Analysis:")
    print("-" * 80)
    
    # Check DOS stub
    if data[0:2] == b'MZ':
        print("  Valid MZ signature found")
        e_lfanew = struct.unpack('<I', data[60:64])[0]
        print(f"  PE header offset from DOS header: 0x{e_lfanew:x}")
        
        if e_lfanew < len(data) - 4:
            pe_sig = data[e_lfanew:e_lfanew+4]
            print(f"  Bytes at PE header offset: {pe_sig.hex()}")
            
            if pe_sig != b'PE\x00\x00':
                print("  -> Invalid PE signature - file may be packed or corrupted")
    
    # Check for overlay data
    print(f"\n[8] Overlay Analysis:")
    print("-" * 80)
    
    # Try to find the end of PE structure
    # Look for the last section's raw data end
    if pe_signatures:
        first_pe = pe_signatures[0]
        # Read COFF header
        if first_pe + 24 < len(data):
            num_sections = struct.unpack('<H', data[first_pe + 6:first_pe + 8])[0]
            optional_header_size = struct.unpack('<H', data[first_pe + 20:first_pe + 22])[0]
            
            section_header_offset = first_pe + 24 + optional_header_size
            print(f"  Section headers at offset: 0x{section_header_offset:x}")
            
            if section_header_offset + num_sections * 40 < len(data):
                last_section_end = 0
                for i in range(num_sections):
                    raw_ptr = struct.unpack('<I', data[section_header_offset + i*40 + 20:section_header_offset + i*40 + 24])[0]
                    raw_size = struct.unpack('<I', data[section_header_offset + i*40 + 16:section_header_offset + i*40 + 20])[0]
                    end = raw_ptr + raw_size
                    if end > last_section_end:
                        last_section_end = end
                
                print(f"  Last section ends at: 0x{last_section_end:x}")
                overlay_size = len(data) - last_section_end
                print(f"  Overlay size: {overlay_size:,} bytes ({overlay_size/1024/1024:.2f} MB)")
                
                if overlay_size > 0:
                    print("  -> File contains overlay data (likely embedded resources or packed data)")

if __name__ == '__main__':
    exe_path = r'c:\Nan\AI\sacy\SRM.exe'
    analyze_file_structure(exe_path)
