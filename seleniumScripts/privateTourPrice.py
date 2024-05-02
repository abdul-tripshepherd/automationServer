import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.tripshepherd.com")
time.sleep(5)
city_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"hero\"]/div[1]/button")))
city_option.click()
time.sleep(2)
austin_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[alt='Austin']")))
austin_checkbox.click()
time.sleep(2)
private_tour = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Private Tours']")))
private_tour.click()
time.sleep(2)
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/tours/private-tour-of-austin']")))
element.click()
time.sleep(2)
date_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='calendar']")))
date_picker.click()
time.sleep(2)
button_19_april = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='react-calendar__tile react-calendar__month-view__days__day'][.//abbr[@aria-label='April 19, 2024']]")))
button_19_april.click()
time.sleep(2)

time_options = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DateAndPax__TimeOptions-sc-b4e7b67e-2")))
for time_option in time_options:
    if "9:00 am" in time_option.text:
        time_option.click()
        break

dropdown_passenger = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div"))
)
dropdown_passenger.click()
time.sleep(2)

dropdown_menu = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//*[@id=\"__next\"]/main/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/div[2]"))
)
passenger_option = dropdown_menu.find_element(By.XPATH, "//p[contains(text(), '5 Passengers')]")
passenger_price = passenger_option.find_element(By.XPATH, "./span").text
passenger_option.click()
time.sleep(2)

book_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book now')]")))
book_now_price = book_now_button.text.split('$')[1]
time.sleep(2)
if int(passenger_price.split('$')[1].split(".")[0]) == int(book_now_price):
    book_now_button.click()
else:
    print("Error: Prices do not match")

time.sleep(2)

name_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"payment-form\"]/div[1]/input")))
name_field.clear()
name_field.send_keys("john")

email_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"payment-form\"]/div[2]/input")))
email_field.clear()
email_field.send_keys("testing@gmail.com")

phone_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"payment-form\"]/div[3]/div/input")))
phone_field.clear()
phone_field.send_keys("6135550183")

time.sleep(5)

iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#payment-element > div > iframe")))

card_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"Field-numberInput\"]")))
card_field.clear()
card_field.send_keys("5555555555554443")

expiry_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"Field-expiryInput\"]")))
expiry_field.clear()
expiry_field.send_keys("1225")

cvc_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"Field-cvcInput\"]")))
cvc_field.clear()
cvc_field.send_keys("143")

driver.switch_to.default_content()

pay_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"ga4-event-listener-checkout\"]")))
pay_btn.click()
time.sleep(2)

try:
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#payment-element > div > iframe")))
    alert_element = driver.find_element(By.XPATH, "//p[contains(@class, 'Error')]")
    alert_text = alert_element.text
    print("Alert:", alert_text)
except:
    print('No Error Message')

time.sleep(10)

driver.quit()