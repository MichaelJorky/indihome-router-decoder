# Indihome Decoder Utility
Indihome Decoder Encoder Utility adalah Utilitas Sederhana untuk Mendecoder File Config pada Router Fiberhome, Huawei, dan ZTE indihome

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
Contoh: ```python decoder3.py config/config.bin config/config.xml```
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
python decoder1.py config/config.bin config/config.xml
python decoder2.py config/config.bin config/config.xml
python decoder3.py config/config.bin config/config.xml
python decoder1.py --model "F670L" config/config.bin config/config.xml
python decoder2.py --model "F670L" config/config.bin config/config.xml
python decoder3.py --model "F670L" config/config.bin config/config.xml
python decoder1.py --serial ZTE123456789 config/config.bin config/config.xml
python decoder2.py --serial ZTE123456789 config/config.bin config/config.xml
python decoder3.py --serial ZTE123456789 config/config.bin config/config.xml
python decoder1.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml
python decoder2.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml
python decoder3.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml
```
#
<b>***** Contoh daftar lengkap perintah yang bisa digunakan untuk Decoder *****</b>
```
--key 2bf3525fd2dcc7fe
--model F670L
--serial ZTE123456789
--mac AA:BB:CC:DD:EE:FF
--longpass Telkomdso123
--signature ZXHN F670L V9.0
--key-prefix CEFD0000000000174654
--iv-prefix ZTE%FN$GponNJ025
--key-suffix 574ffbb30a488a9e2d583a86719400a7
--iv-suffix dedb7b84041d5f10bfe84bca2a165e39
--try-all-known-keys
```
#
<b>***** Encoder Works for ZTE F670L, ZTE F609, ZTE F660, ZTE F450, ZTE F460, ZTE MF283, ZTE F663, ZTE GM220, ZTE F600W, ZTE H108N, ZTE H168N, ZTE H267A, ZTE H298N, ZTE H201L, ZTE H298Q, ZTE H298A,ZTE H268Q *****</b>
```
python encoder1.py --key 'isi_key' --signature 'F670L' --include-header config/config.xml config/new.config.bin
python encoder1.py --key 'isi_key' --signature 'F670L' --version 1 --include-header config/config.xml config/new.config.bin
python encoder1.py --signature F670L --payload-type 6 config/config.xml config/new.config.bin 
python encoder1.py --model "F670L" config/config.xml config/new.config.bin
python encoder1.py --serial ZTE123456789 --signature 'F670L' config/config.xml config/new.config.bin
python encoder1.py --signature 'F670L' --use-signature-encryption config/config.xml config/new.config.bin
```
<b>***** Contoh daftar lengkap perintah yang bisa digunakan untuk Encoder *****</b>
```
--key: jika terdeteksi di decoder silahkan gunakan kembali kombinasi kunci ini untuk encodernya
--signature: gunakan kembali tanda tangan untuk kombinasi encodernya, karena terkadang ada yang harus menggunakan seperti ini F670L atau menggunakan versi lengkapnya seperti ini ZXHN F670L V9.0
--payload-type: gunakan payload type yang terdeteksi di dekodernya
--serial: gunakan serial number yang sebelumnya digunakan pada decodernya

--key 2bf3525fd2dcc7fe
--model F670L
--serial ZTE123456789
--mac AA:BB:CC:DD:EE:FF
--longpass Telkomdso123
--signature ZXHN F670L V9.0
--iv {iv_key}
--use-signature-encryption
--chunk-size 65536
--payload-type {0/1/2/3/4/5/6}
--version {1/2}
--include-header
--little-endian-header
--include-unencrypted-length
--key-prefix CEFD0000000000174654
--iv-prefix ZTE%FN$GponNJ025
--key-suffix 574ffbb30a488a9e2d583a86719400a7
--iv-suffix dedb7b84041d5f10bfe84bca2a165e39
```
