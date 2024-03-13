# indihome-router-decoder
Indihome Router Decoder adalah utilitas sederhana untuk mendecoder file config pada router indihome

1. Login ke router 192.168.1.1 menggunakan user user lalu backup confignya

2. Catat mac address dan serial number router
Contoh Mac address: AA:BB:CC:DD:EE:FF
Contoh serial number: ZTE123456789

3. Download dan instal python3
https://www.python.org/downloads/

4. Download dan instal Git
https://git-scm.com/downloads

5. Jalankan Git CMD (run as administrator)
git clone https://github.com/MichaelJorky/indihome-router-decoder .zte-decoder

7. Instal pycryptodomex 
python -m pip install pycryptodome (optional)
python -m pip install pycryptodomex (optional)
atau
python pip3 install pycryptodome
python pip3 install pycryptodomex

8. Intsal setuptools
python -m pip install setuptools (optional)
atau
python pip3 install setuptools

9. Instal selenium
python -m pip install selenium (wajib)
atau
python pip3 install selenium

10. Pindahkan config.bin ke folder .zte-decoder

9. Jalankan script python
Buka git cmd lalu ketik perintah cd .zte-decoder

10. Lalu pasteukan salah satu kode dibawah ini dan jangan lupa ganti dulu untuk serial numbernya maupun mac addressnya

python decoder.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config.bin config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --model "F670L" config.bin config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --signature "ZXHN F670L V9.0" config.bin config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF --key 'Telkomdso123' config.bin config.xml

python decoder.py --mac AA:BB:CC:DD:EE:FF config.bin config.xml

python decoder.py --model "F670L" --serial ZTE123456789 config.bin config.xml

python decoder.py --model "F670L" --key 'Telkomdso123' config.bin config.xml

python decoder.py --model "F670L" --signature "ZXHN F670L V9.0" config.bin config.xml

python decoder.py --model "F609" config.bin config.xml

python decoder.py --serial ZTE123456789 config.bin config.xml

python decoder.py --serial ZTE123456789 --key 'Telkomdso123' config.bin config.xml

python decoder.py --serial ZTE123456789 --signature "ZXHN F670L V9.0" config.bin config.xml

python decoder.py --key 'Telkomdso123' --signature "ZXHN F670L V9.0" config.bin config.xml

python decoder.py --key 'Telkomdso123' config.bin config.xml

python decoder.py --signature "F609" config.bin config.xml

python decoder.py config.bin config.xml
