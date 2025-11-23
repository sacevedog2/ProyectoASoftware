"""
Script para compilar traducciones .po a .mo compatible con Django y UTF-8
Ejecutar: python compile_translations.py
"""
import os
import struct

def create_mo_file_simple(po_path, mo_path):
    """Crea un archivo .mo básico pero funcional desde un .po"""
    
    translations = {}
    
    # Leer archivo .po
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parsear de forma simple
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            msgid = line[7:-1]
            i += 1
            
            # Leer msgstr
            while i < len(lines) and not lines[i].strip().startswith('msgstr'):
                i += 1
            
            if i < len(lines):
                msgstr_line = lines[i].strip()
                if msgstr_line.startswith('msgstr "'):
                    msgstr = msgstr_line[8:-1]
                    if msgid and msgstr:  # Solo agregar si ambos tienen contenido
                        translations[msgid] = msgstr
        
        i += 1
    
    print(f" Encontradas {len(translations)} traducciones")
    
    # Crear archivo .mo en formato gettext
    keys = sorted(translations.keys())
    
    # Encode todo a UTF-8
    encoded_keys = [k.encode('utf-8') for k in keys]
    encoded_values = [translations[k].encode('utf-8') for k in keys]
    
    # Agregar header vacío al principio
    encoded_keys.insert(0, b'')
    # Header con charset UTF-8
    header = b'Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n'
    encoded_values.insert(0, header)
    
    # Calcular offsets
    key_start = 7 * 4 + 16 * len(encoded_keys)
    value_start = key_start + sum(len(k) + 1 for k in encoded_keys)
    
    key_offsets = []
    offset = key_start
    for k in encoded_keys:
        key_offsets.append((len(k), offset))
        offset += len(k) + 1
    
    value_offsets = []
    offset = value_start
    for v in encoded_values:
        value_offsets.append((len(v), offset))
        offset += len(v) + 1
    
    # Escribir archivo .mo
    with open(mo_path, 'wb') as f:
        # Magic number (little endian)
        f.write(struct.pack('<I', 0x950412de))
        # Version
        f.write(struct.pack('<I', 0))
        # Number of strings
        f.write(struct.pack('<I', len(encoded_keys)))
        # Offset of table with original strings
        f.write(struct.pack('<I', 7 * 4))
        # Offset of table with translation strings
        f.write(struct.pack('<I', 7 * 4 + 8 * len(encoded_keys)))
        # Size of hashing table (0 = no hashing)
        f.write(struct.pack('<I', 0))
        # Offset of hashing table
        f.write(struct.pack('<I', 0))
        
        # Write key index
        for length, offset in key_offsets:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))
        
        # Write value index
        for length, offset in value_offsets:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))
        
        # Write keys
        for k in encoded_keys:
            f.write(k)
            f.write(b'\x00')
        
        # Write values
        for v in encoded_values:
            f.write(v)
            f.write(b'\x00')
    
    print(f" Archivo .mo generado correctamente: {mo_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    po_file = os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'django.po')
    mo_file = os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'django.mo')
    
    if os.path.exists(po_file):
        print(" Compilando traducciones...")
        create_mo_file_simple(po_file, mo_file)
        print(" Compilación exitosa!")
    else:
        print(f" Archivo no encontrado: {po_file}")
