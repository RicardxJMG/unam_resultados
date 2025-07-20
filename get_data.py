import pandas as pd 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 




pages: list = [f"https://www.dgae.unam.mx/Licenciatura2025/resultados/{i}5.html" for i in range(1,5)]
driver_path = "C:/WebDrivers/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get(pages[0])  # testing just for one page

bs_object = BeautifulSoup(driver.page_source, "html.parser")






driver.quit()  # Cierra el navegador al finalizar











