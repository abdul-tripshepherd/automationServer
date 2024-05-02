# This scripts iterates all of the blog posts and checks for any broken links

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

driver = webdriver.Chrome()
driver.get("https://www.tripshepherd.com/blog")

wait = WebDriverWait(driver, 10)

total_links = 0
valid_links = 0
invalid_links = []

for j in range(1,14):

    base_selector = "#__next > main > div.min-h-screen > div > div:nth-child(5) > div > div:nth-child({})"

    for i in range(1, 9):
        try:
            for k in range(1,j):
                next_pg = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#pagination > div > ul > li.next > a')))
                next_pg.click()
                time.sleep(1)
            css_selector = base_selector.format(i)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            element.click()
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#__next > main > div.min-h-screen > div > div.lg\\:flex-row.flex-col.flex.gap-10.items-start.justify-center.relative.px-\\[4\\%\\].lg\\:px-\\[6\\%\\] > div.slug-__BLOGPAGE-sc-3179693b-0.kVEeAj")))
            html_content = element.get_attribute("innerHTML")
            soup = BeautifulSoup(html_content, "html.parser")
            paragraphs = soup.find_all("p")
            for paragraph in paragraphs:
                links = paragraph.find_all("a", href=True)
                for link in links:
                    total_links += 1
                    response = requests.head(link["href"])
                    if response.status_code == 200:
                        valid_links += 1
                        print(f"Link '{link['href']}' on Page {j}, Blog {i} is valid.") 
                    else:
                        invalid_links.append({"link": link["href"], "page_number": j, "blog_number": i, "status_code": response.status_code})
                        print(f"Link '{link['href']}' on Page {j}, Blog {i} is broken. Status code: {response.status_code}")

            driver.back()
        except:
            pass

data = {
    "total_links": total_links,
    "valid_links": valid_links,
    "invalid_links": invalid_links
}

with open("links_status.json", "w") as json_file:
    json.dump(data, json_file, indent=4)