# indihome-router-decoder
Indihome Router Decoder adalah utilitas sederhana untuk mendecoder file config pada router indihome

1. Login ke router 192.168.1.1 menggunakan user user lalu backup confignya

2. Catat mac address dan serial number router
Contoh Mac address: AA:BB:CC:DD:EE:FF
Contoh serial number: ZTE123456789

3. Download dan instal python3 (minimum python 3.5)
https://www.python.org/downloads/

4. Download dan instal Git
https://git-scm.com/downloads

5. Jalankan Git CMD (run as administrator)
git clone https://github.com/MichaelJorky/indihome-router-decoder .zte-decoder

6. Instal pycryptodomex 
python -m pip install pycryptodome 
dan
python -m pip install pycryptodomex 
atau
python pip3 install pycryptodome
dan
python pip3 install pycryptodomex

7. Intsal setuptools
python -m pip install setuptools 
atau
python pip3 install setuptools

8. Instal selenium
python -m pip install selenium 
atau
python pip3 install selenium

9. Pindahkan config.bin ke folder C:\Users\Nama_User\.zte-decoder\config

10. Jalankan script python
Buka git cmd lalu ketik perintah cd .zte-decoder

11. Lalu pasteukan salah satu kode dibawah ini dan jangan lupa ganti dulu untuk serial number, model, key, signature maupun mac addressnya

***** Just tried it on ZTE F670L V9.0 *****

python decoder.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --model "F670L" config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --key 'Telkomdso123' config/config.bin config/config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF config/config.bin config/config.xml

python decoder.py --model "F670L" --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --model "F670L" --key 'Telkomdso123' config/config.bin config/config.xml

python decoder.py --model "F670L" --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --model "F670L" config/config.bin config/config.xml

python decoder.py --serial ZTE123456789 config/config.bin config/config.xml

python decoder.py --serial ZTE123456789 --key 'Telkomdso123' config/config.bin config/config.xml

python decoder.py --serial ZTE123456789 --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --key 'Telkomdso123' --signature "ZXHN F670L V9.0" config/config.bin config/config.xml

python decoder.py --key 'Telkomdso123' config/config.bin config/config.xml

python decoder.py --signature "F670L" config/config.bin config/config.xml

python decoder.py config/config.bin config/config.xml


***** Just tried it on F609 V5.2 and ZTE F660 V6.0 *****

python uni_decoder.py --longpass '' config/config.bin config/config.xml

python uni_decoder.py config/config.bin config/config.xml

python uni_decoder.py --serial " " config/config.bin config/config.xml

python uni_decoder.py --signature " " config/config.bin config/config.xml

python uni_decoder.py --model " " config/config.bin config/config.xml

python uni_decoder.py --mac AA:BB:CC:DD:EE:FF config/config.bin config/config.xml

python uni_decoder.py --try-all-known-keys config/config.bin config/config.xml

python uni_decoder.py --key 'Telkomdso123' config/config.bin config/config.xml

python uni_decoder.py --serial ZTE123456789 config/config.bin config/config.xml

python uni_decoder.py --model "F609" config/config.bin config/config.xml

python uni_decoder.py --signature "ZTE F609 V5.2" config/config.bin config/config.xml
