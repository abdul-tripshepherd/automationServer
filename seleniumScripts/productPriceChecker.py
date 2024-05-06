import json
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import dotenv

class productChecker:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def send_email():
        dotenv.load_dotenv('secret.env')
        password = os.environ["GMAIL_PASSWORD"]
        msg = MIMEMultipart()
        msg['From'] = 'abdulmuhaymintripshepherd@gmail.com'
        msg['To'] = 'abdulmuhaymim@gmail.com'
        msg['Subject'] = 'Link Status Report'
        body = 'Please find attached the link status report.'
        msg.attach(MIMEText(body, 'plain'))

        with open('C:/Users/HP/automationServer/links_status.json', 'rb') as f:
            part = MIMEApplication(f.read(), _subtype='json')
            part.add_header('Content-Disposition', 'attachment', filename='link_status.json')
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        print(password)
        server.login('abdulmuhaymintripshepherd@gmail.com', password)
        text = msg.as_string()
        server.sendmail('abdulmuhaymintripshepherd@gmail.com', 'abdulmuhaymim@gmail.com', text)
        server.quit()
        print('Email Sent Succesfully!')

    def verify_product(self):

        self.driver.get("https://www.tripshepherd.com")

        wait = WebDriverWait(self.driver, 10)

        all_cities = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="hero"]/div[1]/button')))
        all_cities.click()
        city = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="hero"]/div[2]/div/div[2]/a[1]')))
        city.click()
        product = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="feature_experiences_cards"]/div/a[1]')))
        product.click()

        price_tag = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/p')))
        print(price_tag.text)
        no_of_pax = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]/span')))
        print(no_of_pax.text)
        book_now_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/button')))
        book_now_price.click()
        calendar_expand = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/img')))
        calendar_expand.click()
        date_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/div[2]/button[18]')))
        print(date_btn.text)
        date_btn.click()
        calendar_expand.click()
        no_of_pax_expand = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]/button/img')))
        add_adult = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/div[2]/div[3]')))
        add_child = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div[2]/div[3]')))
        add_infant = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[3]/div[2]/div[3]')))

        time.sleep(20)
        self.driver.quit()



priceChecker = productChecker()
priceChecker.verify_product()
    