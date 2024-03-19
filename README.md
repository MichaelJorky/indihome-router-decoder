# indihome-router-decoder
Indihome Router Decoder adalah utilitas sederhana untuk mendecoder file config pada router indihome
#
<b>***** Auto Install *****</b>

Kloning atau Download Repo/Folder ini
```
git clone https://github.com/MichaelJorky/indihome-router-decoder.git .zte-decoder
```
cd .zte-decoder

python setup.py install
#
<b>***** Manual Install *****</b>

1. Login ke router via web browser misal ip routernya 192.168.1.1 lalu login menggunakan username: admin password: admin atau username: user password: user (tinggal disesuaikan untuk loginnya) lalu backup confignya

2. Catat mac address dan serial number router
Contoh Mac address: AA:BB:CC:DD:EE:FF
Contoh serial number: ZTE123456789
Contoh model: F670L
Contoh signature: ZXHN F670L V9.0
Contoh key: jjxx

4. Download dan instal python3 (minimum python 3.5)
https://www.python.org/downloads/

5. Download dan instal Git
https://git-scm.com/downloads

6. Jalankan Git CMD (run as administrator)
git clone https://github.com/MichaelJorky/indihome-router-decoder .zte-decoder

7. Instal pycryptodomex 
python -m pip install pycryptodome 
dan
python -m pip install pycryptodomex 
atau
python pip3 install pycryptodome
dan
python pip3 install pycryptodomex

8. Intsal setuptools
python -m pip install setuptools 
atau
python pip3 install setuptools

9. Instal selenium
python -m pip install selenium 
atau
python pip3 install selenium

10. Install Dependencies
python -m pip install -r requirements.txt
atau
python pip3 install -r requirements.txt

11. Pindahkan config.bin (config yang sudah di download pada step 1) ke folder C:\Users\Nama_User\\.zte-decoder\config

12. Jalankan script python
Buka git cmd lalu ketik perintah cd .zte-decoder

13. Lalu pasteukan salah satu kode dibawah ini dan jangan lupa ganti dulu untuk serial number, model, key, signature maupun mac addressnya
#
<b>***** Decoder baru di test untuk ZTE F670L V9.0 *****</b>

python decoder.py --key-prefix CEFD1234567890123456 --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --key-suffix 14e1b600b1fd579f47433b88e8d85291 --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --iv-suffix 3acf16259def65456fc2a68ab5e10d96 --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --model "F670L" config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --key 'jjww' config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF config/config.bin config/config.xml

python decoder.py --model "F670L" --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --model "F670L" --key 'jjww' config/config.bin config/config.xml

python decoder.py --model "F670L" --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --model "F670L" config/config.bin config/config.xml

python decoder.py --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --serial ZTE123456789 --key 'jjww' config/config.bin config/config.xml

python decoder.py --serial ZTE123456789 --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --key 'Telkomdso123' --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --key 'jjww' config/config.bin config/config.xml

python decoder.py --signature "F670L" config/config.bin config/config.xml

python decoder.py config/config.bin config/config.xml
#
<b>***** Decoder baru di test untuk ZTE F609 V5.2, ZTE F660 V6.0 *****</b>

python uni_decoder.py --key-prefix CEFD1234567890123456 --try-all-known-keys --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --key-prefix CEFD1234567890123456 --signature "ZXHN F609 V5.2" --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --key-suffix 14e1b600b1fd579f47433b88e8d85291 --try-all-known-keys --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --key-suffix 14e1b600b1fd579f47433b88e8d85291 --signature "ZXHN F609 V5.2" --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --iv-suffix 3acf16259def65456fc2a68ab5e10d96 --try-all-known-keys --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --iv-suffix 3acf16259def65456fc2a68ab5e10d96 --signature "ZXHN F609 V5.2" --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --try-all-known-keys --signature "ZXHN F609 V5.2" --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py config/config.bin config/config.xml

python uni_decoder.py --longpass '' config/config.bin config/config.xml

python uni_decoder.py --serial " " config/config.bin config/config.xml

python uni_decoder.py --signature " " config/config.bin config/config.xml

python uni_decoder.py --model " " config/config.bin config/config.xml

python uni_decoder.py --mac AA:BB:CC:DD:EE:FF config/config.bin config/config.xml

python uni_decoder.py --try-all-known-keys config/config.bin config/config.xml

python uni_decoder.py --key 'jjww' config/config.bin config/config.xml

python uni_decoder.py --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --model "F609" config/config.bin config/config.xml

python uni_decoder.py --signature "ZXHN F609 V5.2" config/config.bin config/config.xml
#
<b>***** MD5 File Checksum *****</b>

python md5sum.py config/config.bin

python md5sum.py config/<name_file>.bin

python md5sum.py config/<name_file>.xml

python md5sum.py config/<name_file>.iso

python md5sum.py config/<name_file>.exe

python md5sum.py config/<name_file>

python md5sum.py config/<name_file>.<type_file>

python md5sum.py <folder_path>/<name_file>.<type_file>
#
<b>***** Encoder baru di test untuk ZTE F609 V5.2, ZTE F660 V6.0 *****</b>

python uni_encoder.py --key-prefix CEFD1234567890123456 --signature "ZXHN F609 V5.2" --serial ZTE123456789 config/config.xml config/new.config.bin

python uni_encoder.py --key-suffix 14e1b600b1fd579f47433b88e8d85291 --signature "ZXHN F609 V5.2" --serial ZTE123456789 config/config.xml config/new.config.bin

python uni_encoder.py --iv-suffix 3acf16259def65456fc2a68ab5e10d96 --signature "ZXHN F609 V5.2" --serial ZTE123456789 config/config.xml config/new.config.bin

python uni_encoder.py --signature ZXHN F609 V5.2 --payload-type 0 config/config.xml config/new.config.bin

python uni_encoder.py --signature ZXHN F609 V5.2 --payload-type 2 config/config.xml config/new.config.bin

python uni_encoder.py --signature ZXHN F609 V5.2 --payload-type 4 config/config.xml config/new.config.bin

python uni_encoder.py --signature "ZXHN F609 V5.2" config/config.xml config/new.config.bin

python uni_encoder.py --signature "ZXHN F609 V5.2" --version 1 --include-header config/config.xml config/new.config.bin

python uni_encoder.py --signature "ZXHN F609 V5.2" --version 2 --include-header config/config.xml config/new.config.bin

python uni_encoder.py --signature "ZXHN F609 V5.2" --include-unencrypted-length --include-header config/config.xml config/new.config.bin

python uni_encoder.py --signature "ZXHN F609 V5.2" --use-signature-encryption config/config.xml config/new.config.bin

python uni_encoder.py --signature "ZXHN F609 V5.2" --include-header config/config.xml config/new.config.bin

python uni_encoder.py --serial ZTE123456789 --signature "ZXHN F609 V5.2" config/config.xml config/new.config.bin

python uni_encoder.py --serial ZTE123456789 --signature " " config/config.xml config/new.config.bin

python uni_encoder.py --serial ZTE123456789 --model "F609" config/config.xml config/new.config.bin

python uni_encoder.py --model "F609" config/config.xml config/new.config.bin

python uni_encoder.py --include-header --version 1 config/config.xml config/new.config.bin

python uni_encoder.py --include-header --version 2 config/config.xml config/new.config.bin

python uni_encoder.py --include-header --include-unencrypted-length config/config.xml config/new.config.bin

python uni_encoder.py --include-header config/config.xml config/new.config.bin

python uni_encoder.py --key 'jjxx' --signature 'ZXHN F609 V5.2' --include-header config/config.xml config/new.config.bin

python uni_encoder.py --key 'jjxx' --signature 'ZXHN F609 V5.2' --version 1 --include-header config/config.xml config/new.config.bin
