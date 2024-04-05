# Indihome Router Decoder Encoder
Indihome Router Decoder Encoder adalah Utilitas Sederhana untuk Mendecoder File Config pada Router Fiberhome, Huawei, dan ZTE indihome

Rilis "Indihome Router Utility" versi aplikasi bisa cek disini https://github.com/MichaelJorky/Indihome-Router-Utility
#
<b>***** Cara Install di Android Termux *****</b>

jalankan perintah ```apt update``` untuk memperbarui daftar paket (package) lalu jalankan perintah ```apt install termux-api termux-am``` yang dimana termux-api untuk mengakses berbagai fitur api dan termux-am bermanfaat untuk memberikan akses ke activity manager android, lalu jalankan perintah ```termux-setup-storage``` dan perintah ini bermanfaat untuk memberikan akses ke penyimpanan perangkat anda, untuk melihat path directory termux ketik perintah ```pwd```, lalu jalankan perintah ```pkg install mc``` yang dimana perintah ini digunakan untuk menginstal Midnight Commander (mc) yang memungkinkan Anda untuk menjelajahi file dan direktori, mengelola file, mengompres dan mengekstrak arsip, dan melakukan berbagai tugas berkas lainnya dari antarmuka baris perintah, dan untuk membukanya cukup gunakan perintah ```mc``` kemudian untuk membuka kembali tool zte decodernya jika aplikasi termux sudah ditutup cukup gunakan perintah ```cd .zte-decoder```
```
pkg install git
```
```
pkg install python
```
```
pkg upg
```
```
pkg ins python
```
```
pkg ins python-pip
```
```
python -m pip install setuptools
```
```
git clone https://github.com/MichaelJorky/indihome-router-decoder.git .zte-decoder
```
```
cd .zte-decoder
```
```
python setup.py install
```
Contoh: ```python unidecoder.py config/config.bin config/config.xml```
#
<b>***** Auto Install di Windows*****</b>

Kloning atau Download Repo/Folder ini
```
python -m pip install setuptools
```
```
git clone https://github.com/MichaelJorky/indihome-router-decoder.git .zte-decoder
```
```
cd .zte-decoder
```
```
python setup.py install
```
#
<b>***** Manual Install di Windows *****</b>

1. Login ke router via web browser misal ip routernya 192.168.1.1 lalu login menggunakan username: admin password: admin atau username: user password: user (tinggal disesuaikan untuk loginnya) lalu backup confignya

2. Catat mac address dan serial number router:
Contoh Mac address: AA:BB:CC:DD:EE:FF
Contoh serial number: ZTE123456789
Contoh model: F670L
Contoh signature: ZXHN F670L V9.0
Contoh key: jjxx

4. Download dan instal python3 (minimum python 3.5):
https://www.python.org/downloads/

5. Download dan instal Git:
https://git-scm.com/downloads

6. Jalankan Git CMD (run as administrator):

   ```git clone https://github.com/MichaelJorky/indihome-router-decoder.git .zte-decoder```

7. Instal pycryptodomex: 

   ```python -m pip install pycryptodome``` 
dan
```python -m pip install pycryptodomex``` 
atau
```python pip3 install pycryptodome```
dan
```python pip3 install pycryptodomex```

8. Intsal setuptools:

   ```python -m pip install setuptools``` 
atau
```python pip3 install setuptools```

9. Instal selenium:

   ```python -m pip install selenium``` 
atau
```python pip3 install selenium```

10. Install Dependencies:

    ```python -m pip install -r requirements.txt```
atau
```python pip3 install -r requirements.txt```

11. Pindahkan config.bin (config yang sudah di download pada step 1) ke folder C:\Users\Nama_User\\.zte-decoder\config

12. Jalankan script python
Buka git cmd lalu ketik perintah ```cd .zte-decoder```

13. Lalu pasteukan salah satu kode dibawah ini dan jangan lupa ganti dulu untuk serial number, model, key, signature maupun mac addressnya
#
<b>***** Decoder Works for ZTE F670L, ZTE F609, ZTE F660, ZTE F450, ZTE F460, ZTE MF283, ZTE F663, ZTE GM220, ZTE F600W, ZTE H108N, ZTE H168N, ZTE H267A, ZTE H298N, ZTE H201L, ZTE H298Q, ZTE H298A,ZTE H268Q *****</b>
```
python autodecoder.py config/config.bin config/config.xml
python autodecoder.py --model "F670L" config/config.bin config/config.xml
python autodecoder.py --serial ZTEGCEFD0000 config/config.bin config/config.xml
python autodecoder.py --mac 60:E5:D8:00:00:00 --serial ZTEGCEFD0000 config/config.bin config/config.xml
python autodecoder.py --model "F670L" --serial ZTEGCEFD0000 config/config.bin config/config.xml
python decoder.py --key-prefix CEFD0000000000174654 --mac 60:E5:D8:00:00:00 --serial ZTEGCEFD0000 config/config.bin config/config.xml
python decoder.py --key-suffix 574ffbb30a488a9e2d583a86719400a7 --mac 60:E5:D8:00:00:00 --serial ZTEGCEFD0000 config/config.bin config/config.xml
python decoder.py --iv-suffix dedb7b84041d5f10bfe84bca2a165e39 --mac 60:E5:D8:00:00:00 --serial ZTEGCEFD0000 config/config.bin config/config.xml
python decoder.py --mac 60:E5:D8:00:00:00 --serial ZTEGCEFD0000 config/config.bin config/config.xml
python decoder.py --mac 60:E5:D8:00:00:00 --model "F670L" config/config.bin config/config.xml
python decoder.py --mac 60:E5:D8:00:00:00 --signature "ZXHN F670L V9.0" config/config.bin config/config.xml
python decoder.py --mac 60:E5:D8:00:00:00 --key '2bf3525fd2dcc7fe' config/config.bin config/config.xml
python decoder.py --mac 60:E5:D8:00:00:00 config/config.bin config/config.xml
python decoder.py --model "F670L" --serial ZTEGCEFD0000 config/config.bin config/config.xml
python decoder.py --model "F670L" --key '2bf3525fd2dcc7fe' config/config.bin config/config.xml
python decoder.py --model "F670L" --signature "ZXHN F670L V9.0" config/config.bin config/config.xml
python decoder.py --model "F670L" config/config.bin config/config.xml
python decoder.py --serial ZTEGCEFD0000 config/config.bin config/config.xml
python decoder.py --serial ZTEGCEFD0000 --key '2bf3525fd2dcc7fe' config/config.bin config/config.xml
python decoder.py --serial ZTEGCEFD0000 --signature "ZXHN F670L V9.0" config/config.bin config/config.xml
python decoder.py --key 'Telkomdso123' --signature "ZXHN F670L V9.0" config/config.bin config/config.xml
python decoder.py --key '2bf3525fd2dcc7fe' config/config.bin config/config.xml
python decoder.py --signature "F670L" config/config.bin config/config.xml
python decoder.py config/config.bin config/config.xml
python unidecoder.py --key-prefix CEFD0000000000174654 --try-all-known-keys --serial ZTEGCEFD0000 config/config.bin config/config.xml
python unidecoder.py --key-prefix CEFD0000000000174654 --signature "ZXHN F670L V9.0" --serial ZTEGCEFD0000 config/config.bin config/config.xml
python unidecoder.py --key-suffix 574ffbb30a488a9e2d583a86719400a7 --try-all-known-keys --serial ZTEGCEFD0000 config/config.bin config/config.xml
python unidecoder.py --key-suffix 574ffbb30a488a9e2d583a86719400a7 --signature "ZXHN F670 V9.0" --serial ZTEGCEFD0000 config/config.bin config/config.xml
python unidecoder.py --iv-suffix dedb7b84041d5f10bfe84bca2a165e39 --try-all-known-keys --serial ZTEGCEFD0000 config/config.bin config/config.xml
python unidecoder.py --iv-suffix dedb7b84041d5f10bfe84bca2a165e39 --signature "ZXHN F670 V9.0" --serial ZTEGCEFD0000 config/config.bin config/config.xml
python unidecoder.py --try-all-known-keys --signature "ZXHN F670L V9.0" --serial ZTEGCEFD0000 config/config.bin config/config.xml
python unidecoder.py config/config.bin config/config.xml
python unidecoder.py --longpass '' config/config.bin config/config.xml
python unidecoder.py --serial " " config/config.bin config/config.xml
python unidecoder.py --signature " " config/config.bin config/config.xml
python unidecoder.py --model " " config/config.bin config/config.xml
python unidecoder.py --mac 60:E5:D8:00:00:00 config/config.bin config/config.xml
python unidecoder.py --try-all-known-keys config/config.bin config/config.xml
python unidecoder.py --key '2bf3525fd2dcc7fe' config/config.bin config/config.xml
python unidecoder.py --serial ZTE123456789 config/config.bin config/config.xml
python unidecoder.py --model "F670L" config/config.bin config/config.xml
python unidecoder.py --signature "ZXHN F670L V9.0" config/config.bin config/config.xml
```
#
<b>***** Encoder Works for ZTE F670L, ZTE F609, ZTE F660, ZTE F450, ZTE F460, ZTE MF283, ZTE F663, ZTE GM220, ZTE F600W, ZTE H108N, ZTE H168N, ZTE H267A, ZTE H298N, ZTE H201L, ZTE H298Q, ZTE H298A,ZTE H268Q *****</b>
```
python uniencoder.py --key-prefix CEFD0000000000174654 --signature "ZXHN F670L V9.0" --serial ZTE123456789 config/config.xml config/new.config.bin
python uniencoder.py --key-suffix 574ffbb30a488a9e2d583a86719400a7 --signature "ZXHN F670L V9.0" --serial ZTEGCEFD0000 config/config.xml config/new.config.bin
python uniencoder.py --iv-suffix dedb7b84041d5f10bfe84bca2a165e39 --signature "ZXHN F670L V9.0" --serial ZTEGCEFD0000 config/config.xml config/new.config.bin
python uniencoder.py --signature ZXHN F670L V9.0 --payload-type 0 config/config.xml config/new.config.bin
python uniencoder.py --signature ZXHN F670L V9.0 --payload-type 2 config/config.xml config/new.config.bin
python uniencoder.py --signature ZXHN F670L V9.0 --payload-type 4 config/config.xml config/new.config.bin
python uniencoder.py --signature ZXHN F670L V9.0 --payload-type 6 config/config.xml config/new.config.bin
python uniencoder.py --signature "ZXHN F670L V9.0" config/config.xml config/new.config.bin
python uniencoder.py --signature "ZXHN F670L V9.0" --version 1 --include-header config/config.xml config/new.config.bin
python uniencoder.py --signature "ZXHN F670L V9.0" --version 2 --include-header config/config.xml config/new.config.bin
python uniencoder.py --signature "ZXHN F670L V9.0" --include-unencrypted-length --include-header config/config.xml config/new.config.bin
python uniencoder.py --signature "ZXHN F670L V9.0" --use-signature-encryption config/config.xml config/new.config.bin
python uniencoder.py --signature "ZXHN F670L V9.0" --include-header config/config.xml config/new.config.bin
python uniencoder.py --serial ZTEGCEFD0000 --signature "ZXHN F670L V9.0" config/config.xml config/new.config.bin
python uniencoder.py --serial ZTEGCEFD0000 --signature " " config/config.xml config/new.config.bin
python uniencoder.py --serial ZTEGCEFD0000 --model "F670L" config/config.xml config/new.config.bin
python uniencoder.py --model "F670L" config/config.xml config/new.config.bin
python uniencoder.py --include-header --version 1 config/config.xml config/new.config.bin
python uniencoder.py --include-header --version 2 config/config.xml config/new.config.bin
python uniencoder.py --include-header --include-unencrypted-length config/config.xml config/new.config.bin
python uniencoder.py --include-header config/config.xml config/new.config.bin
python uniencoder.py --key '2bf3525fd2dcc7fe' --signature 'ZXHN F670L V9.0' --include-header config/config.xml config/new.config.bin
python uniencoder.py --key '2bf3525fd2dcc7fe' --signature 'ZXHN F670L V9.0' --version 1 --include-header config/config.xml config/new.config.bin
```
#
<b>***** MD5 File Checksum *****</b>
```
python md5sum.py config/config.bin
python md5sum.py config/<name_file>.bin
python md5sum.py config/<name_file>.xml
python md5sum.py config/<name_file>.iso
python md5sum.py config/<name_file>.exe
python md5sum.py config/<name_file>
python md5sum.py config/<name_file>.<type_file>
python md5sum.py <folder_path>/<name_file>.<type_file>
```
