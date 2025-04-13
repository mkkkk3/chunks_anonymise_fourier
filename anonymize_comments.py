# interakcje z systemem (arg)
import sys
# dekompresja
import zlib

def read_file_bytes(file_path):
    # rb - read, binary
    # with, zeby zostal prawidlowo zamkniety
    # with zapewnia, ze najpierw poprawnie zostanie otworzony plik i chwilowo bedzie to jako zmienna file
    with open(file_path, 'rb') as file:
        # a potem jesli sie udalo to zwroci file.read()
        # zwraca cala zawartosc jako bajty
        return file.read()

def bytes_to_int(byte_data):
    # ciag bajtow na liczbe calkowita
    # interpretujac bajty jako big-endian 
    # najwazniejszy bajt na poczatku
    result = 0
    for byte in byte_data:
        result = result * 256 + int(byte)
    return result

def parse_chunks(file_bytes):
    index = 8  # Pomijamy 8 bajtów sygnatury PNG
    chunks = []
    
    while index < len(file_bytes):
        # dlugosc chunka (a dokladniej dlugosc chunkow IDAT) - pierwsze 4 bajty
        chunk_len = bytes_to_int(file_bytes[index:index+4])
        # typ chunka - kolejke 4 bajty - (czyta jako ciag znakow UTF-8) - UTF8 - character encoding
        chunk_type = file_bytes[index+4:index+8].decode('utf-8')
        # dane chunka - od tego miejsca do tego miejsca + chunk_len
        data = file_bytes[index+8:index+8+chunk_len]
        # crc - (cyclic Redundancy Checksum) - sprawdzanie czy nie ma bledow
        crc = file_bytes[index+8+chunk_len:index+12+chunk_len]
        # Dodaje do listy, typ, dane i crc
        chunks.append((chunk_type, data, crc))
        # Przesuwamy index o długość chunka plus 8 bajtów na typ i 4 na CRC
        index += 12 + chunk_len
        
    return chunks

# usuniecie wszystkich ancillary chunks
# pozostawienie critical chunks
# modyfikacja IHDR, usuniecie info o kompresji, filtrze i interlacing
# przeliczenie CRC
def filter_chunks(chunks):
    allowed_types = {'IHDR', 'PLTE', 'IDAT', 'IEND'}
    # lista chunkow ktore przejda filtracje
    filtered_chunks = []

    for chunk_type, data, original_crc in chunks:
        if chunk_type == 'IHDR':
            # Zmieniamy compression, filter i interlace na 0
            ihdr_modified = data[:10] + bytes([0, 0, 0])
            # Obliczamy nowe CRC
            crc_data = chunk_type.encode('utf-8') + ihdr_modified
            print('crc_data')
            print(crc_data)
            print('chunk_type.encode(utf-8)')
            print(chunk_type.encode('utf-8'))
            print('ihdr_modified')
            print(ihdr_modified)
            # chunk_type.encode('utf-8')
            # "IHDR" -> b'IHDR' (zamienia na ciag bajtow)
            # ihdr_modified Ma długość 13 bajtów:
            # width (4)
            # height (4)
            # bit depth (1)
            # color type (1)
            # compression method (1) → ustawiony na 0
            # filter method (1) → ustawiony na 0
            # interlace method (1) → ustawiony na 0
            # 
            # czyli
            # b'IHDR' + <dane_chunku>
            # 
            # wynik printa:
            # crc_data
            # b'IHDR\x00\x00\x00\xae\x00\x00\x00\xc8\x08\x03\x00\x00\x00'
            # chunk_type.encode(utf-8)
            # b'IHDR'
            # ihdr_modified
            # b'\x00\x00\x00\xae\x00\x00\x00\xc8\x08\x03\x00\x00\x00'
            new_crc = zlib.crc32(crc_data) & 0xffffffff
            # zlib to biblioteka do kompresji
            # CRC w PNG to niepodpisane liczby 32-bitowe (unsigned int32)
            # 0xffffffff = 2**32 - 1 = 4294967295
            # Operacja & powoduje, że:
            # traktujemy wynik jako 32 bity bez znaku
            # crc = -123456789
            # print(crc & 0xffffffff)  # = 4171510507 -> poprawny, dodatni CRC
            # w skrocie konwertuje wynik na unsigned 32-bit int
            filtered_chunks.append((chunk_type, ihdr_modified, new_crc.to_bytes(4, byteorder='big')))
            # new_crc.to_bytes(4, byteorder='big')
            # Zamienia wartość CRC (np. 12345678) na ciąg 4 bajtów, w formacie big-endian (czyli najstarszy bajt jako pierwszy).
            # crc = 0x1A2B3C4D
            # crc.to_bytes(4, 'big') -> b'\x1A\x2B\x3C\x4D'
        elif chunk_type in allowed_types:
            # użyj oryginalnego CRC
            filtered_chunks.append((chunk_type, data, original_crc))

    return filtered_chunks

def save_png(output_path, chunks):
    # wb - write, binary
    with open(output_path, 'wb') as file:
        # 89 50 4E 47 0D 0A 1A 0A
        file.write(b'\x89PNG\r\n\x1a\n')  # podpis PNG
        for chunk_type, data, crc in chunks:
            # dlugosc data zmieniona na 4 bajty
            # np. len(data) = 13
            # (13).to_bytes(4, 'big') → b'\x00\x00\x00\r'
            file.write(len(data).to_bytes(4, byteorder='big'))     # długość danych
            file.write(chunk_type.encode('utf-8'))                  # typ chunka
            file.write(data)                                        # dane chunka
            file.write(crc)                                         # przekazany CRC

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
