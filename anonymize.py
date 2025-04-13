import sys
import zlib

def read_file_bytes(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def bytes_to_int(byte_data):
    result = 0
    for byte in byte_data:
        result = result * 256 + int(byte)
    return result

def parse_chunks(file_bytes):
    index = 8
    chunks = []
    
    while index < len(file_bytes):
        chunk_len = bytes_to_int(file_bytes[index:index+4])
        chunk_type = file_bytes[index+4:index+8].decode('utf-8')
        data = file_bytes[index+8:index+8+chunk_len]
        crc = file_bytes[index+8+chunk_len:index+12+chunk_len]
        chunks.append((chunk_type, data, crc))
        index += 12 + chunk_len
        
    return chunks

def filter_chunks(chunks):
    allowed_types = {'IHDR', 'PLTE', 'IDAT', 'IEND'}
    filtered_chunks = []

    for chunk_type, data, _ in chunks:
        if chunk_type == 'IHDR':
            ihdr_modified = data[:10] + bytes([0, 0, 0])
            crc_data = chunk_type.encode('utf-8') + ihdr_modified
            new_crc = zlib.crc32(crc_data) & 0xffffffff
            filtered_chunks.append((chunk_type, ihdr_modified, new_crc.to_bytes(4, byteorder='big')))
        elif chunk_type in allowed_types:
            crc_data = chunk_type.encode('utf-8') + data
            crc = zlib.crc32(crc_data) & 0xffffffff
            filtered_chunks.append((chunk_type, data, crc.to_bytes(4, byteorder='big')))

    return filtered_chunks

def save_png(output_path, chunks):
    with open(output_path, 'wb') as file:
        file.write(b'\x89PNG\r\n\x1a\n')
        for chunk_type, data, crc in chunks:
            file.write(len(data).to_bytes(4, byteorder='big'))
            file.write(chunk_type.encode('utf-8'))
            file.write(data)
            file.write(crc)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_png_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = input_path.rsplit('.', 1)[0] + '_anonymised.png'
    
    file_bytes = read_file_bytes(input_path)
    chunks = parse_chunks(file_bytes)
    filtered_chunks = filter_chunks(chunks)
    save_png(output_path, filtered_chunks)
    
    print(f"Anonymised image saved as: {output_path}")

if __name__ == '__main__':
    main()
