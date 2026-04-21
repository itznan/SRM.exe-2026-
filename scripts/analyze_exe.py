import struct
import sys
import os

def analyze_pe(filepath):
    """Analyze PE file structure"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print("=" * 80)
    print(f"Analyzing: {filepath}")
    print(f"File size: {len(data):,} bytes ({len(data)/1024/1024:.2f} MB)")
    print("=" * 80)
    
    # DOS Header
    if len(data) < 64:
        print("File too small to be a valid PE")
        return
    
    # Check MZ signature
    if data[0:2] != b'MZ':
        print("Invalid DOS signature (not MZ)")
        return
    
    print("\n[1] DOS Header:")
    print(f"  Signature: {data[0:2]}")
    e_lfanew = struct.unpack('<I', data[60:64])[0]
    print(f"  PE header offset: 0x{e_lfanew:x} ({e_lfanew})")
    
    # PE Signature
    if e_lfanew + 4 > len(data):
        print("PE header offset beyond file size")
        return
    
    pe_sig = data[e_lfanew:e_lfanew+4]
    if pe_sig != b'PE\x00\x00':
        print(f"Invalid PE signature: {pe_sig}")
        return
    
    print(f"\n[2] PE Signature: {pe_sig}")
    
    # COFF/NT Header
    machine = struct.unpack('<H', data[e_lfanew+4:e_lfanew+6])[0]
    num_sections = struct.unpack('<H', data[e_lfanew+6:e_lfanew+8])[0]
    timestamp = struct.unpack('<I', data[e_lfanew+8:e_lfanew+12])[0]
    characteristics = struct.unpack('<H', data[e_lfanew+18:e_lfanew+20])[0]
    
    print(f"\n[3] File Header:")
    print(f"  Machine: 0x{machine:x} ({get_machine_name(machine)})")
    print(f"  Number of sections: {num_sections}")
    print(f"  TimeDateStamp: {timestamp}")
    print(f"  Characteristics: 0x{characteristics:x}")
    
    # Optional Header
    magic = struct.unpack('<H', data[e_lfanew+20:e_lfanew+22])[0]
    entry_point = struct.unpack('<I', data[e_lfanew+40:e_lfanew+44])[0]
    image_base = struct.unpack('<I', data[e_lfanew+28:e_lfanew+32])[0]
    code_size = struct.unpack('<I', data[e_lfanew+20:e_lfanew+24])[0] if magic == 0x10b else struct.unpack('<Q', data[e_lfanew+20:e_lfanew+28])[0]
    init_data_size = struct.unpack('<I', data[e_lfanew+24:e_lfanew+28])[0] if magic == 0x10b else struct.unpack('<Q', data[e_lfanew+28:e_lfanew+36])[0]
    
    print(f"\n[4] Optional Header:")
    print(f"  Magic: 0x{magic:x} ({'PE32' if magic == 0x10b else 'PE32+' if magic == 0x20b else 'Unknown'})")
    print(f"  Entry point: 0x{entry_point:x}")
    print(f"  Image base: 0x{image_base:x}")
    print(f"  Code size: {code_size}")
    print(f"  Initialized data size: {init_data_size}")
    
    # Data directories
    print(f"\n[5] Data Directories:")
    dir_names = ["Export", "Import", "Resource", "Exception", "Certificate", 
                 "BaseReloc", "Debug", "Architecture", "GlobalPtr", "TLS",
                 "LoadConfig", "BoundImport", "IAT", "DelayImport", "CLR", "Reserved"]
    
    dir_offset = e_lfanew + (96 if magic == 0x10b else 112)
    for i in range(16):
        rva = struct.unpack('<I', data[dir_offset + i*8:dir_offset + i*8 + 4])[0]
        size = struct.unpack('<I', data[dir_offset + i*8 + 4:dir_offset + i*8 + 8])[0]
        if rva != 0 or size != 0:
            print(f"  {dir_names[i]}: RVA=0x{rva:x}, Size={size}")
    
    # Section Headers
    section_offset = e_lfanew + (24 + (224 if magic == 0x10b else 240))
    print(f"\n[6] Section Headers:")
    
    sections = []
    for i in range(num_sections):
        name = data[section_offset + i*40:section_offset + i*40 + 8].rstrip(b'\x00').decode('ascii', errors='ignore')
        virt_size = struct.unpack('<I', data[section_offset + i*40 + 8:section_offset + i*40 + 12])[0]
        virt_addr = struct.unpack('<I', data[section_offset + i*40 + 12:section_offset + i*40 + 16])[0]
        raw_size = struct.unpack('<I', data[section_offset + i*40 + 16:section_offset + i*40 + 20])[0]
        raw_ptr = struct.unpack('<I', data[section_offset + i*40 + 20:section_offset + i*40 + 24])[0]
        characteristics = struct.unpack('<I', data[section_offset + i*40 + 36:section_offset + i*40 + 40])[0]
        
        sections.append({
            'name': name,
            'virt_addr': virt_addr,
            'raw_ptr': raw_ptr,
            'raw_size': raw_size,
            'virt_size': virt_size,
            'characteristics': characteristics
        })
        
        print(f"  Section {i+1}: {name}")
        print(f"    Virtual address: 0x{virt_addr:x}")
        print(f"    Virtual size: {virt_size}")
        print(f"    Raw data pointer: 0x{raw_ptr:x}")
        print(f"    Raw data size: {raw_size}")
        print(f"    Characteristics: 0x{characteristics:x} ({get_section_flags(characteristics)})")
    
    # Import Directory
    import_dir_rva = struct.unpack('<I', data[dir_offset + 8:dir_offset + 12])[0]
    import_dir_size = struct.unpack('<I', data[dir_offset + 12:dir_offset + 16])[0]
    
    if import_dir_rva != 0:
        print(f"\n[7] Import Directory:")
        import_offset = rva_to_offset(import_dir_rva, sections)
        if import_offset:
            idx = 0
            while True:
                original_first_thunk = struct.unpack('<I', data[import_offset + idx*20:import_offset + idx*20 + 4])[0]
                time_date_stamp = struct.unpack('<I', data[import_offset + idx*20 + 4:import_offset + idx*20 + 8])[0]
                forwarder_chain = struct.unpack('<I', data[import_offset + idx*20 + 8:import_offset + idx*20 + 12])[0]
                name_rva = struct.unpack('<I', data[import_offset + idx*20 + 12:import_offset + idx*20 + 16])[0]
                first_thunk = struct.unpack('<I', data[import_offset + idx*20 + 16:import_offset + idx*20 + 20])[0]
                
                if name_rva == 0:
                    break
                
                name_offset = rva_to_offset(name_rva, sections)
                if name_offset:
                    dll_name = data[name_offset:].split(b'\x00')[0].decode('ascii', errors='ignore')
                    print(f"  DLL {idx}: {dll_name}")
                    
                    # Import functions
                    thunk_offset = rva_to_offset(first_thunk if first_thunk != 0 else original_first_thunk, sections)
                    if thunk_offset:
                        func_idx = 0
                        while True:
                            thunk = struct.unpack('<I', data[thunk_offset + func_idx*4:thunk_offset + func_idx*4 + 4])[0]
                            if thunk == 0:
                                break
                            
                            if thunk & 0x80000000:
                                # Import by ordinal
                                ordinal = thunk & 0xFFFF
                                print(f"    Ordinal: {ordinal}")
                            else:
                                # Import by name
                                hint_name_offset = rva_to_offset(thunk, sections)
                                if hint_name_offset:
                                    hint = struct.unpack('<H', data[hint_name_offset:hint_name_offset+2])[0]
                                    func_name = data[hint_name_offset+2:].split(b'\x00')[0].decode('ascii', errors='ignore')
                                    print(f"    {func_name} (hint: {hint})")
                            
                            func_idx += 1
                            if func_idx > 100:  # Limit output
                                print(f"    ... (and more)")
                                break
                
                idx += 1
                if idx > 50:  # Limit output
                    print(f"  ... (and more DLLs)")
                    break
    
    # Export Directory
    export_dir_rva = struct.unpack('<I', data[dir_offset:dir_offset + 4])[0]
    export_dir_size = struct.unpack('<I', data[dir_offset + 4:dir_offset + 8])[0]
    
    if export_dir_rva != 0:
        print(f"\n[8] Export Directory:")
        export_offset = rva_to_offset(export_dir_rva, sections)
        if export_offset:
            num_exports = struct.unpack('<I', data[export_offset + 20:export_offset + 24])[0]
            num_names = struct.unpack('<I', data[export_offset + 24:export_offset + 28])[0]
            addr_of_functions = struct.unpack('<I', data[export_offset + 28:export_offset + 32])[0]
            addr_of_names = struct.unpack('<I', data[export_offset + 32:export_offset + 36])[0]
            addr_of_ordinals = struct.unpack('<I', data[export_offset + 36:export_offset + 40])[0]
            
            print(f"  Number of functions: {num_exports}")
            print(f"  Number of names: {num_names}")
            
            if num_names > 0 and num_names < 100:
                names_offset = rva_to_offset(addr_of_names, sections)
                ordinals_offset = rva_to_offset(addr_of_ordinals, sections)
                functions_offset = rva_to_offset(addr_of_functions, sections)
                
                if names_offset and ordinals_offset and functions_offset:
                    for i in range(min(num_names, 20)):
                        name_rva = struct.unpack('<I', data[names_offset + i*4:names_offset + i*4 + 4])[0]
                        ordinal = struct.unpack('<H', data[ordinals_offset + i*2:ordinals_offset + i*2 + 2])[0]
                        func_rva = struct.unpack('<I', data[functions_offset + ordinal*4:functions_offset + ordinal*4 + 4])[0]
                        
                        name_offset = rva_to_offset(name_rva, sections)
                        if name_offset:
                            func_name = data[name_offset:].split(b'\x00')[0].decode('ascii', errors='ignore')
                            print(f"    {func_name} @ 0x{func_rva:x}")
    
    # String extraction
    print(f"\n[9] Extracted Strings (ASCII, length >= 4):")
    strings = extract_strings(data, min_length=4)
    interesting_strings = []
    for s in strings:
        s_lower = s.lower()
        if any(keyword in s_lower for keyword in ['http', 'www', 'dll', 'exe', 'error', 'fail', 'password', 'key', 'api', 'config', 'file', 'path']):
            interesting_strings.append(s)
    
    for s in interesting_strings[:50]:  # Limit output
        print(f"  {s}")
    
    print(f"\n[10] Summary:")
    print(f"  This is a valid PE{32 if magic == 0x10b else 64} executable")
    print(f"  Entry point at RVA 0x{entry_point:x}")
    print(f"  Contains {num_sections} sections")
    print(f"  Total strings found: {len(strings)}")
    print(f"  Interesting strings: {len(interesting_strings)}")

def rva_to_offset(rva, sections):
    """Convert RVA to file offset"""
    for section in sections:
        if section['virt_addr'] <= rva < section['virt_addr'] + section['virt_size']:
            return rva - section['virt_addr'] + section['raw_ptr']
    return None

def get_machine_name(machine):
    machines = {
        0x14c: 'IMAGE_FILE_MACHINE_I386',
        0x8664: 'IMAGE_FILE_MACHINE_AMD64',
        0x1c0: 'IMAGE_FILE_MACHINE_ARM',
        0xaa64: 'IMAGE_FILE_MACHINE_ARM64'
    }
    return machines.get(machine, 'UNKNOWN')

def get_section_flags(characteristics):
    flags = []
    if characteristics & 0x00000020:
        flags.append('CODE')
    if characteristics & 0x40000000:
        flags.append('READABLE')
    if characteristics & 0x80000000:
        flags.append('WRITABLE')
    if characteristics & 0x20000000:
        flags.append('EXECUTABLE')
    if characteristics & 0x02000000:
        flags.append('CNT_CODE')
    if characteristics & 0x04000000:
        flags.append('CNT_INITIALIZED_DATA')
    if characteristics & 0x08000000:
        flags.append('CNT_UNINITIALIZED_DATA')
    return ', '.join(flags)

def extract_strings(data, min_length=4):
    """Extract ASCII strings from binary data"""
    strings = []
    current_string = []
    
    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string.append(chr(byte))
        else:
            if len(current_string) >= min_length:
                strings.append(''.join(current_string))
            current_string = []
    
    if len(current_string) >= min_length:
        strings.append(''.join(current_string))
    
    return strings

if __name__ == '__main__':
    exe_path = r'c:\Nan\AI\sacy\SRM.exe'
    analyze_pe(exe_path)
