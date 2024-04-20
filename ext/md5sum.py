import os
import sys
import hashlib

def md5sum(filename):
    try:
        fh = open(filename, 'rb')  # Membuka file dalam mode bacaan biner
    except IOError as e:  # Menangani kesalahan jika gagal membuka file
        print('Gagal membuka {} : {}'.format(filename, str(e)))  # Menampilkan pesan kesalahan
        return None

    md5 = hashlib.md5()  # Membuat objek md5
    try:
        while True:
            data = fh.read(4096)  # Membaca data file dalam potongan-potongan 4096 byte
            if not data:
                break
            md5.update(data)  # Mengupdate objek md5 dengan data yang dibaca
    except IOError as e:  # Menangani kesalahan jika gagal membaca file
        fh.close()  # Menutup file
        print('Gagal membaca {} : {}'.format(filename, str(e)))  # Menampilkan pesan kesalahan
        return None
    
    fh.close()  # Menutup file
    return md5.hexdigest()  # Mengembalikan nilai hash md5 dari file

def main():
    if(len(sys.argv) != 2):
        print('Penggunaan: {} <file>'.format(sys.argv[0]))  # Menampilkan cara penggunaan program
        sys.exit(-1)

    filename = sys.argv[1]  # Mendapatkan nama file dari argumen baris perintah
    if not os.path.isfile(filename):  # Memeriksa apakah nama file adalah file yang valid
        print('"{}" bukanlah sebuah file'.format(filename))  # Menampilkan pesan kesalahan jika bukan file
        sys.exit(-1)

    fh = md5sum(filename)  # Mendapatkan hash md5 dari file
    if(fh == None):
        print('Gagal')  # Menampilkan pesan kesalahan jika gagal menghitung hash md5
        sys.exit(-1)
        
    print(fh)  # Menampilkan hash md5
    sys.exit(0)

if __name__ == "__main__":
    main()
