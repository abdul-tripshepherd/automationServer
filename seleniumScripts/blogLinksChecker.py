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

class LinkChecker:
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

    def check_links(self):

        self.driver.get("https://www.tripshepherd.com/blog")

        wait = WebDriverWait(self.driver, 10)

        total_links = 0
        valid_links = 0
        invalid_links_count = 0
        invalid_links = []

        for j in range(1,14):
            base_selector = "#__next > main > div.min-h-screen > div > div:nth-child(5) > div > div:nth-child({})"
            l = 9
            if j==13:
                l = 5

            for i in range(1, l):
                for k in range(1,j):
                    next_pg = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#pagination > div > ul > li.next > a')))
                    next_pg.click()
                    time.sleep(1)
                css_selector = base_selector.format(i)
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
                element.click()
                if i == 1: 
                    time.sleep(2)
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#__next > main > div.min-h-screen > div > div.lg\\:flex-row.flex-col.flex.gap-10.items-start.justify-center.relative.px-\\[4\\%\\].lg\\:px-\\[6\\%\\] > div.slug-__BLOGPAGE-sc-3179693b-0.kVEeAj")))
                html_content = element.get_attribute("innerHTML")
                soup = BeautifulSoup(html_content, "html.parser")
                anchor_tags = soup.find_all("a")
                links = [tag.get("href") for tag in anchor_tags]
                for link in links:
                    total_links += 1
                    response = requests.head(link)
                    if response.status_code == 200:
                        valid_links += 1
                        print(f"Link '{link}' on Page {j}, Blog {i} is valid.") 
                    else:
                        invalid_links_count += 1
                        invalid_links.append({"link": link, "page_number": j, "blog_number": i, "status_code": response.status_code})
                        print(f"Link '{link}' on Page {j}, Blog {i} is broken. Status code: {response.status_code}")
                self.driver.back()
        data = {
            "total_links": total_links,
            "valid_links_count": valid_links,
            "invalid_links_count": invalid_links_count,
            "repeated_invalid_links": total_links - valid_links - invalid_links_count,
            "invalid_links": invalid_links
        }

        with open(f'reports\\blogs_invalid_links_{int(time.time())}.json', "w") as json_file:
            json.dump(data, json_file, indent=4)
        # LinkChecker.send_email()

        self.driver.quit()
    
ptr = LinkChecker()
ptr.check_links()