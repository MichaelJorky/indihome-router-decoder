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

6. Instal pycryptodomex 
python -m pip install pycryptodome (optional)
python -m pip install pycryptodomex (optional)
python pip3 install pycryptodome
python pip3 install pycryptodomex

7. Intsal setuptools
python -m pip install setuptools (optional)
pip3 install setuptools

8. Instal selenium
python -m pip install selenium (wajib)
python pip3 install selenium

9. Pindahkan config.bin ke folder .zte-decoder

9. Jalankan script python
Buka cmd lalu ketik perintah .zte-decoder

python decode.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config.bin config.xml
python decode.py --model "F670L" --serial ZTE123456789 config.bin config.xml
python decode.py --mac AA:BB:CC:DD:EE:FF --model "F670L" config.bin config.xml
python decode.py --mac AA:BB:CC:DD:EE:FF --serial ZTE123456789 config.bin config.xml
python decode.py --mac AA:BB:CC:DD:EE:FF config.bin config.xml
python decode.py --serial ZTE123456789 config.bin config.xml
python decode.py --key 'Telkomdso123' config.bin config.xml
python decode.py --model "F670L" config.bin config.xml
---------------------------------------------------------------
Subscribe: https://www.youtube.com/@DuniaMR?sub_confirmation=1
