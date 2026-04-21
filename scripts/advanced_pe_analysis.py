import pefile
import lief
import sys

def analyze_with_pefile(filepath):
    """Analyze PE file using pefile library"""
    print("=" * 80)
    print("ADVANCED PE ANALYSIS USING PEFILE")
    print("=" * 80)
    
    try:
        pe = pefile.PE(filepath)
        
        print(f"\n[1] Basic Information:")
        print(f"  File: {filepath}")
        print(f"  Size: {pe.OPTIONAL_HEADER.SizeOfImage:,} bytes")
        print(f"  Entry Point: 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:x}")
        print(f"  Image Base: 0x{pe.OPTIONAL_HEADER.ImageBase:x}")
        print(f"  Machine Type: 0x{pe.FILE_HEADER.Machine:x}")
        print(f"  Number of Sections: {pe.FILE_HEADER.NumberOfSections}")
        
        print(f"\n[2] Sections:")
        for section in pe.sections:
            name = section.Name.decode().rstrip('\x00')
            print(f"  {name}")
            print(f"    Virtual Address: 0x{section.VirtualAddress:x}")
            print(f"    Virtual Size: {section.Misc_VirtualSize:,}")
            print(f"    Raw Size: {section.SizeOfRawData:,}")
            print(f"    Characteristics: 0x{section.Characteristics:x}")
            print(f"    Entropy: {section.get_entropy():.4f}")
            print()
        
        print(f"\n[3] Imported DLLs:")
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                print(f"  {entry.dll.decode('utf-8')}")
                for imp in entry.imports:
                    if imp.name:
                        print(f"    - {imp.name.decode('utf-8')}")
        
        print(f"\n[4] Exported Functions:")
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            print(f"  Name: {pe.DIRECTORY_ENTRY_EXPORT.name.decode('utf-8')}")
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols[:20]:
                if exp.name:
                    print(f"    - {exp.name.decode('utf-8')} @ 0x{exp.address:x}")
        
        print(f"\n[5] Data Directories:")
        for idx, directory in enumerate(pe.OPTIONAL_HEADER.DATA_DIRECTORY):
            if directory.Size != 0:
                print(f"  Directory {idx}: RVA=0x{directory.VirtualAddress:x}, Size={directory.Size}")
        
        print(f"\n[6] Rich Header (if present):")
        try:
            if hasattr(pe, 'RICH_HEADER'):
                print("  Rich header found")
                for comp_id, count, use_count in pe.RICH_HEADER.values:
                    print(f"    CompID: 0x{comp_id:x}, Count: {count}, UseCount: {use_count}")
        except:
            print("  No rich header or unable to parse")
        
        print(f"\n[7] Digital Signatures:")
        if hasattr(pe, 'VS_FIXEDFILEINFO'):
            ffi = pe.VS_FIXEDFILEINFO
            print(f"  File Version: {ffi.FileVersionMS >> 16}.{ffi.FileVersionMS & 0xFFFF}.{ffi.FileVersionLS >> 16}.{ffi.FileVersionLS & 0xFFFF}")
            print(f"  Product Version: {ffi.ProductVersionMS >> 16}.{ffi.ProductVersionMS & 0xFFFF}.{ffi.ProductVersionLS >> 16}.{ffi.ProductVersionLS & 0xFFFF}")
        
        pe.close()
        
    except Exception as e:
        print(f"Error with pefile: {e}")

def analyze_with_lief(filepath):
    """Analyze PE file using LIEF library"""
    print("\n" + "=" * 80)
    print("ADVANCED PE ANALYSIS USING LIEF")
    print("=" * 80)
    
    try:
        binary = lief.parse(filepath)
        
        print(f"\n[1] LIEF Basic Information:")
        print(f"  Format: {binary.format.name if hasattr(binary.format, 'name') else binary.format}")
        print(f"  Entry point: 0x{binary.entrypoint:x}")
        print(f"  Image base: 0x{binary.imagebase:x}")
        if hasattr(binary.header, 'characteristics'):
            print(f"  Characteristics: 0x{binary.header.characteristics:x}")
        
        print(f"\n[2] Sections:")
        for section in binary.sections:
            print(f"  {section.name}")
            print(f"    Virtual address: 0x{section.virtual_address:x}")
            print(f"    Virtual size: {section.virtual_size:,}")
            print(f"    Size: {section.size:,}")
            print(f"    Entropy: {section.entropy:.4f}")
            print()
        
        print(f"\n[3] Imported Functions:")
        for lib in binary.imports:
            print(f"  {lib.name}")
            for func in lib.entries[:10]:
                print(f"    - {func.name if func.name else 'ordinal'}")
        
        print(f"\n[4] Exported Functions:")
        if binary.exported_functions:
            for func in binary.exported_functions[:20]:
                print(f"  - {func.name} @ 0x{func.address:x}")
        
        print(f"\n[5] Relocations:")
        print(f"  Number of relocations: {len(binary.relocations)}")
        
        print(f"\n[6] Resources:")
        if binary.has_resources:
            print("  Resources present")
            # Try to get resource manager
            try:
                resources = binary.resources
                print(f"  Resource manager available")
            except:
                print("  Unable to parse detailed resources")
        
        print(f"\n[7] Security Features:")
        print(f"  NX Compatible: {'Yes' if binary.has_nx else 'No'}")
        print(f"  ASLR: {'Yes' if binary.has_aslr else 'No'}")
        print(f"  DEP: {'Yes' if binary.has_dep else 'No'}")
        print(f"  SEH: {'Yes' if binary.has_seh else 'No'}")
        
        print(f"\n[8] Authentihash:")
        print(f"  Authentihash: {binary.authentihash.hex()}")
        
        print(f"\n[9] DOS Stub:")
        dos_stub = binary.dos_stub
        if dos_stub:
            print(f"  DOS stub size: {len(dos_stub)} bytes")
            try:
                stub_text = dos_stub.decode('ascii', errors='ignore')
                if 'This program' in stub_text:
                    print(f"  Standard DOS stub message found")
            except:
                pass
        
    except Exception as e:
        print(f"Error with LIEF: {e}")

def check_for_anomalies(filepath):
    """Check for suspicious anomalies in the PE file"""
    print("\n" + "=" * 80)
    print("ANOMALY DETECTION")
    print("=" * 80)
    
    try:
        pe = pefile.PE(filepath, fast_load=True)
        
        anomalies = []
        
        # Check for unusual section names
        unusual_sections = []
        valid_chars = '._abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for section in pe.sections:
            name = section.Name.decode().rstrip('\x00')
            if any(c not in valid_chars for c in name):
                unusual_sections.append(name)
        
        if unusual_sections:
            anomalies.append(f"Unusual section names: {unusual_sections}")
        
        # Check for high entropy sections (possible packing)
        high_entropy_sections = []
        for section in pe.sections:
            entropy = section.get_entropy()
            if entropy > 7.5:
                name = section.Name.decode().rstrip('\x00')
                high_entropy_sections.append(f"{name} (entropy: {entropy:.4f})")
        
        if high_entropy_sections:
            anomalies.append(f"High entropy sections (possible packing): {high_entropy_sections}")
        
        # Check overlay
        overlay_size = len(pe.get_overlay()) if pe.get_overlay() else 0
        if overlay_size > 0:
            anomalies.append(f"Overlay detected: {overlay_size:,} bytes")
        
        # Check for suspicious imports
        suspicious_imports = []
        suspicious_dlls = ['wininet.dll', 'winhttp.dll', 'ws2_32.dll', 'urlmon.dll']
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode().lower()
                if any(sus in dll_name for sus in suspicious_dlls):
                    suspicious_imports.append(dll_name)
        
        if suspicious_imports:
            anomalies.append(f"Suspicious network-related imports: {suspicious_imports}")
        
        # Check for exports (rare in malware, common in legitimate apps)
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            export_count = len(pe.DIRECTORY_ENTRY_EXPORT.symbols)
            anomalies.append(f"Exported functions: {export_count}")
        
        if anomalies:
            print("\nDetected Anomalies:")
            for anomaly in anomalies:
                print(f"  - {anomaly}")
        else:
            print("\nNo significant anomalies detected")
        
        pe.close()
        
    except Exception as e:
        print(f"Error during anomaly detection: {e}")

if __name__ == '__main__':
    exe_path = r'c:\Nan\AI\sacy\SRM.exe'
    
    analyze_with_pefile(exe_path)
    analyze_with_lief(exe_path)
    check_for_anomalies(exe_path)
