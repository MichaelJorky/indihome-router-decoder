#Script Cari Ip Public di ONT ZTE F670L (V9.0.11P1N13)
#Selinum IDE 
#Tested pada Chrome windows versi 108
#Modif by Dunia MR
#PPPOE setting set IP version ipv4/v6

import time
import datetime  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

ipont = "http://192.168.1.1/"
user = "admin"
passwd = "Telkomdso123"

options = Options()
driver = webdriver.Chrome(options=options)
#options.add_experimental_option("detach", True)

driver.implicitly_wait(20)  # gives an implicit wait for 20 seconds
driver.get(ipont)
driver.set_window_size(968, 992)
#Bukan Page Login
driver.find_element(By.ID, "Frm_Username").click()
driver.find_element(By.ID, "Frm_Username").send_keys(user)
driver.find_element(By.ID, "Frm_Password").send_keys(passwd)
driver.find_element(By.ID, "LoginId").click()
#time.sleep(3)
#Buka Page WAN Status untuk melihat IP 
driver.find_element(By.ID, "internet").click()
#time.sleep(3)
driver.find_element(By.ID, "internetStatus").click()
#time.sleep(3)
driver.find_element(By.ID, "ethWanStatus").click()
driver.find_element(By.ID, "cIPAddress:1").click()
#Asumsi ada 2 profile koneksi WAN : TR069 dan omci_ipv4_pppoe_1 
ipaddr = driver.find_element(
    By.XPATH, "//div[@id=\'Prefix_sub_cIPAddress:1\']/span[2]").text 

logfile = open("logip-indi.txt","a") #log semua ip ke file logip-indi.txt
while ipaddr.startswith(("10", "0")): # Jika ip dengan awalan 10 atau 0 restart koneksi
    x = datetime.datetime.now()
    print(x.strftime("%d%b%Y-%H:%M:%S") +" "+ipaddr)
    logfile.write(x.strftime("%d%b%Y-%H:%M:%S")+" "+ipaddr)
    driver.find_element(By.ID, "internetConfig").click()
    driver.find_element(By.ID, "instName_Internet:1").click()
    driver.find_element(By.ID, "Btn_apply_internet:1").click()
    time.sleep(12)
    driver.find_element(By.ID, "internetStatus").click()
    driver.find_element(By.ID, "ethWanStatus").click()
    time.sleep(3)
    driver.find_element(By.ID, "cIPAddress:1").click()
    ipaddr = driver.find_element(
        By.XPATH, "//div[@id=\'Prefix_sub_cIPAddress:1\']/span[2]").text    
logfile.close()
