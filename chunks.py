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

def print_chunk_details(chunk_type, data):
    if chunk_type == 'IHDR':
        width = bytes_to_int(data[0:4])
        height = bytes_to_int(data[4:8])
        bit_depth = data[8]
        color_type = data[9]
        compression = data[10]
        filter_method = data[11]
        interlace = data[12]
        print(f"  Width: {width} pixels")
        print(f"  Height: {height} pixels")
        print(f"  Bit depth: {bit_depth} bits per pixel")
        print(f"  Color type: {color_type}")
        print(f"  Compression method: ({compression})")
        print(f"  Filter method: ({filter_method})")
        print(f"  Interlace method: ({interlace})")

    elif chunk_type == 'PLTE':
        num_colors = len(data) // 3
        print(f"  Number of colors in palette: {num_colors}")

    elif chunk_type == 'IDAT':
        print("  Image data chunk (IDAT)")

    elif chunk_type == 'IEND':
        print("  Image end chunk (IEND)")

    elif chunk_type == 'cHRM':
        white_point_x = bytes_to_int(data[0:4]) / 100000
        white_point_y = bytes_to_int(data[4:8]) / 100000
        red_x = bytes_to_int(data[8:12]) / 100000
        red_y = bytes_to_int(data[12:16]) / 100000
        green_x = bytes_to_int(data[16:20]) / 100000
        green_y = bytes_to_int(data[20:24]) / 100000
        blue_x = bytes_to_int(data[24:28]) / 100000
        blue_y = bytes_to_int(data[28:32]) / 100000
        print(f"  White point x: {white_point_x}")
        print(f"  White point y: {white_point_y}")
        print(f"  Red x: {red_x}")
        print(f"  Red y: {red_y}")
        print(f"  Green x: {green_x}")
        print(f"  Green y: {green_y}")
        print(f"  Blue x: {blue_x}")
        print(f"  Blue y: {blue_y}")

    elif chunk_type == 'gAMA':
        gamma_value = bytes_to_int(data) / 100000
        print(f"  Gamma: {gamma_value:.5f}")

    elif chunk_type == 'pHYs':
        px_per_unit_x = bytes_to_int(data[0:4])
        px_per_unit_y = bytes_to_int(data[4:8])
        unit_specifier = data[8]
        unit_name = "Meter" if unit_specifier == 1 else "Unknown"
        print(f"  Horizontal resolution: {px_per_unit_x} pixels per unit ({int(px_per_unit_x * 0.0254)} DPI)")
        print(f"  Vertical resolution: {px_per_unit_y} pixels per unit ({int(px_per_unit_y * 0.0254)} DPI)")
        print(f"  Unit specifier: {unit_name}")

    elif chunk_type == 'tIME':
        year, month, day, hour, minute, second = [bytes_to_int(data[i:i+1]) for i in range(6)]
        print(f"  Year: {year}")
        print(f"  Month: {month}")
        print(f"  Day: {day}")
        print(f"  Hour: {hour}")
        print(f"  Minute: {minute}")
        print(f"  Second: {second}")

def print_chunks(chunks):
    for chunk in chunks:
        chunk_type, data, crc = chunk
        print(f"{chunk_type}")
        print_chunk_details(chunk_type, data)
        print(f"Długość danych: {len(data)}")
        print(f"CRC: {crc.hex()}")
        print("___________________________________________________")

def main():
    if len(sys.argv) < 2:
        print("Podaj poprawny format wywolania pliku: python script.py <ścieżka_do_pliku>")
        return
    
    file_path = sys.argv[1]
    file_bytes = read_file_bytes(file_path)
    
    print("Raw bytes:")
    print(file_bytes[:64])
    print("___________________________________________________")
    
    chunks = parse_chunks(file_bytes)
    print_chunks(chunks)

if __name__ == '__main__':
    main()