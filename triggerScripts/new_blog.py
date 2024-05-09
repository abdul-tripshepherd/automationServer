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

class CanonicalVerifier:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def send_email(filename):
        dotenv.load_dotenv('secret.env')
        password = os.environ["GMAIL_PASSWORD"]
        msg = MIMEMultipart()
        msg['From'] = 'abdulmuhaymintripshepherd@gmail.com'
        msg['To'] = 'abdulmuhaymim@gmail.com'
        msg['Subject'] = 'Link Status Report'
        body = 'Please find attached the link status report.'
        msg.attach(MIMEText(body, 'plain'))

        with open(filename, 'rb') as f:
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

    def check_link(self, canonical):

        self.driver.get(canonical)

        wait = WebDriverWait(self.driver, 10)

        total_links = 0
        valid_links = 0
        invalid_links_count = 0
        invalid_links = []
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
                # print(f"Link '{link}' on Page {j}, Blog {i} is valid.") 
            else:
                invalid_links_count += 1
                invalid_links.append({"link": link, "status_code": response.status_code})
                # print(f"Link '{link}' on Page {j}, Blog {i} is broken. Status code: {response.status_code}")
        self.driver.back()
        data = {
            "total_links": total_links,
            "valid_links_count": valid_links,
            "invalid_links_count": invalid_links_count,
            "duplicate_links": total_links - valid_links - invalid_links_count,
            "invalid_links": invalid_links
        }

        timestamp = int(time.time())
        filename = f"links_status_{timestamp}.json"

        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        # CanonicalVerifier.send_email(filename)

        self.driver.quit()