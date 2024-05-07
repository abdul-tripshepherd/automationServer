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
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import dotenv

class productChecker:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

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

        incorrect_prices = []

        self.driver.get("https://www.tripshepherd.com")
        time.sleep(5)

        def extract_number(text):
            match = re.search(r'\d+', text)
            if match:
                return(int(match.group()))

        wait = WebDriverWait(self.driver, 10)

        for j in range(5, 41):
            try:
                time.sleep(5)
                all_cities = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="hero"]/div[1]/button')))
                all_cities.click()
                print('here')
                print(j)
                city = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="hero"]/div[2]/div/div[2]/a[{j}]')))
                city.click()
            except:
                continue
            for i in range(1, 15):
                print(str(j) + ':' + str(i))
                try:
                    product = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="feature_experiences_cards"]/div/a[{i}]')))
                except:
                    continue
                match = re.search(r'\$([\d,]+)$', product.text.splitlines()[-1])
                if match:
                    price = match.group(1)
                    price = int(price.replace(',', ''))
                    product_main_price = price
                product.click()

                try:
                    popup = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Judith Blake"]/button/svg'))).click()
                except:
                    pass

                tour_name = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[3]/div[1]/div[1]/h1'))).text
                try:
                    if 'Coming Soon' in wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div/div/div'))).text:
                        self.driver.back()
                        print(tour_name +': Coming Soon')
                        continue
                except:
                    pass

                starting_from_text = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/p')))
                starting_from_price = extract_number(starting_from_text.text)
                
                calendar_expand = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/img')))
                calendar_expand.click()
                date_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/div[2]/button[18]/div')))
                calendar_price = extract_number(date_btn.text)
                date_btn.click()
                no_of_pax_expand = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]/button')))
                no_of_pax_expand.click()

                pax_check = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]'))).text
                pax_check_flag = False
                if 'Passenger' in pax_check:
                    pax_check_flag = True

                if pax_check_flag:
                    
                    print(tour_name + ': Private Tour')
                    no_of_pax = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/p[2]')))
                    no_of_pax_price = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/p[2]/span'))).text)
                    # print(no_of_pax_price)
                    no_of_pax.click()
                else:
                    
                    add_adult = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/div[2]/div[3]')))
                    add_adult.click()
                    add_adult_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/div/span')))
                    adult_price = extract_number(add_adult_price.text)
                    add_child = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div[2]/div[3]')))
                    add_child.click()
                    add_child_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/span')))
                    child_price = extract_number(add_child_price.text)
                    # add_infant = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[3]/div[2]/div[3]')))
                    # add_infant.click()
                    # add_infant_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[3]/div[1]/div[2]/div/span')))
                    # infant_price = extract_number(add_infant_price.text)
                    no_of_pax_price = child_price + adult_price*3

                book_now_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/button')))
                book_now_price = extract_number(book_now_button.text)
                book_now_button.click()

                if pax_check_flag:
                    no_of_pax_price_2 = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[4]/div[1]/h2'))).text)
                    total_price = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[4]/div[2]/div[2]/h2'))).text)
                else:
                    adult_price_2 = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[1]/h2'))).text)
                    child_price_2 = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[2]/h2'))).text)
                    # infant_price_2 = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[3]/h2'))).text)
                    no_of_pax_price_2 =child_price_2 + adult_price_2
                    total_price = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[4]/div[2]/h2'))).text)

                if total_price == book_now_price == no_of_pax_price == no_of_pax_price_2 and starting_from_price == calendar_price == product_main_price:
                    print(tour_name + ": Prices are correct")
                else:
                    print(tour_name + ": Prices are incorrect")
                    incorrect_prices.append({"name": tour_name, "city_number": j, "product_number": i})

                self.driver.back()
                self.driver.back()
            self.driver.back()
            

        data = {
            "incorrect_prices": incorrect_prices
        }

        with open("product_prices.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        time.sleep(20)
        self.driver.quit()



priceChecker = productChecker()
priceChecker.verify_product()
    