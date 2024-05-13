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
import random
from datetime import datetime

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
        error_prices = []

        self.driver.get("https://www.tripshepherd.com")
        time.sleep(5)

        def extract_number(text):
            match = re.search(r'\d+', text)
            if match:
                return(int(match.group()))

        wait = WebDriverWait(self.driver, 10)

        for j in range(1, 41):
            time.sleep(5)
            all_cities = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="hero"]/div[1]/button')))
            all_cities.click()
            city = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="hero"]/div[2]/div/div[2]/a[{j}]')))
            city.click()
            try:
                count_product = len(wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="feature_experiences_cards"]/div/a'))))
            except:
                print('City has no tours')
                continue
            for i in range(1, count_product+1):
                print(str(j) + ':' + str(i)) 
                try:
                    product = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="feature_experiences_cards"]/div/a[{i}]')))
                    match = re.search(r'\$([\d,]+)$', product.text.splitlines()[-1])
                    if match:
                        price = match.group(1)
                        price = int(price.replace(',', ''))
                        product_main_price = price
                    product.click()
                    issues = []
                except:
                    print('tour_name' + ": Error Checking Prices")
                    error_prices.append({"name": 'tour_name', "city_number": j, "product_number": i})
                    continue

                time.sleep(5)
                try:
                    popup = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#elizabeth\\ kinder > button > svg'))).click()
                except:
                    pass

                try:
                    max_no_p = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/p[1]')))
                    if 'Maximum' in max_no_p.text:
                        max_limit_flag = True
                        # print('Max')
                    else:
                        max_limit_flag = False
                except:
                    # print('96')
                    max_limit_flag = False
                try:
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
                    # date_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/div[2]/button[31]/div')))
                    # calendar_price = extract_number(date_btn.text)
                    # date_btn.click()
                    while True:
                        random_day = random.randint(int(datetime.now().day), 31)
                        try:
                            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/div[2]/button[{random_day}]/div')))
                            date = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, f"//*[@id=\"__next\"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/div[2]/button[{random_day}]")))
                            calendar_price = extract_number(WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/div/div/div[2]/button[{random_day}]/div'))).text)
                            date.click()
                            # print(str(random_day) + ': Available')
                            break
                        except:
                            # print(str(random_day) + ': Unavailable')
                            print('144')
                            pass

                    no_of_pax_expand = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]/button')))
                    pax_check = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]'))).text
                    no_of_pax_expand.click()
                    pax_check_flag = False
                    if 'Passenger' in pax_check:
                        pax_check_flag = True

                    if pax_check_flag:
                        no_of_pax = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/p[2]')))
                        no_of_pax_price = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div/p[2]/span'))).text)
                        if not max_limit_flag:
                            no_of_pax.click()
                    else:
                        add_adult = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/div[2]/div[3]')))
                        add_adult_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/div/span')))
                        add_child = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div[2]/div[3]')))
                        add_child_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/span')))
                        adult_price = extract_number(add_adult_price.text)
                        child_price = extract_number(add_child_price.text)
                        # add_infant = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[3]/div[2]/div[3]')))
                        # add_infant.click()
                        # add_infant_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div/div[2]/div[3]/div[1]/div[2]/div/span')))
                        # infant_price = extract_number(add_infant_price.text)
                        if max_limit_flag:
                            no_of_pax_price = adult_price*2
                        else:
                            add_adult.click()
                            add_child.click()
                            no_of_pax_price = child_price + adult_price*3

                    book_now_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/button')))
                    book_now_price = extract_number(book_now_button.text)
                    book_now_button.click()
                except:
                    print(tour_name + ": Error Checking Prices")
                    self.driver.back()
                    error_prices.append({"name": tour_name, "city_number": j, "product_number": i})
                    continue
            
                time.sleep(2)
                try:
                    if pax_check_flag:
                        # print('here 1')
                        try:
                            no_of_pax_price_2 = extract_number(WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[4]/div[1]/h2'))).text)
                        except:
                            print('204')
                            no_of_pax_price_2 = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[1]/h2'))).text)
                        # print('here 2')
                        
                        try:
                            total_price = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[4]/div[2]/div[2]/h2'))).text)
                        except:
                            total_price = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/h2'))).text)
                            print('212')
                        # print(no_of_pax_price_2)
                        # print(total_price)
                    else:
                        adult_price_2 = extract_number(WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[1]/h2'))).text)
                        child_price_2 = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[2]/h2'))).text)
                        # infant_price_2 = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[3]/h2'))).text)
                        no_of_pax_price_2 =child_price_2 + adult_price_2
                        total_price = extract_number(wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div[3]/div[3]/div[2]/h2'))).text)
                except:
                    print(tour_name + ": Error Checking Prices")
                    self.driver.back()
                    self.driver.back()
                    error_prices.append({"name": tour_name, "city_number": j, "product_number": i})
                    continue

                if total_price == book_now_price == no_of_pax_price == no_of_pax_price_2 and adult_price == starting_from_price == calendar_price == product_main_price and adult_price != child_price  :
                    print(tour_name + ": Prices are correct")
                else:
                    if total_price != book_now_price:
                        issues.append('Checkout Page Total Price != Book Now Button Price')
                    if book_now_price != no_of_pax_price:
                        issues.append('Book Now Button Price != Prices In Pax Dropdown')
                    if no_of_pax_price != no_of_pax_price_2:
                        issues.append('Prices In Pax Dropdown != Individual Prices in Checkout')
                    if book_now_price != no_of_pax_price_2:
                        issues.append('Book Now Button Price != Individual Prices in Checkout')
                    if total_price != no_of_pax_price:
                        issues.append('Checkout Page Total Price != Prices In Pax Dropdown')
                    if total_price != no_of_pax_price_2:
                        issues.append('Checkout Page Total Price != Individual Prices in Checkout')
                    if starting_from_price != calendar_price:
                        issues.append('Advertised Price != Calendar Price')
                    if starting_from_price != product_main_price:
                        issues.append('Advertised Price != Main Page Card Price')
                    if calendar_price != product_main_price:
                        issues.append('Calendar Price != Main Page Card Price')
                    if adult_price == child_price:
                        issues.append('Child Price & Adult Price Is Same')
                    if adult_price != starting_from_price:
                        issues.append('Adverised Price != Adult Price')
                    print(tour_name + ": Prices are incorrect" + '/n Issues: ' + str(issues))
                    incorrect_prices.append({"name": tour_name, "city_number": j, "product_number": i, 'issues' : issues})

                self.driver.back()
                self.driver.back()

            self.driver.back()
            

        data = {
            "incorrect_prices": incorrect_prices
        }
        error_data = {
            "error_checking_prices": error_prices
        }

        with open(f"product_prices_{int(time.time())}.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        with open(f"error_product_prices_{int(time.time())}.json", "w") as json_file:
            json.dump(error_data, json_file, indent=4)

        time.sleep(20)
        self.driver.quit()



priceChecker = productChecker()
priceChecker.verify_product()
    