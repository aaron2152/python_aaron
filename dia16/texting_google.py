from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

recurso = input("Ingrese algo: ")

driver = webdriver.Chrome()
driver.get("https://www.dinatran.gov.py:8443/wsint4/servlet/com.wsint3.veritvchapa")

web_element = driver.find_element(By.NAME,'vVCHAPA')
web_element.send_keys("" + Keys.ENTER)
time.sleep(30)