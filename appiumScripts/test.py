from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
import time

# Set desired capabilities
desired_caps = {
    "platformName": "Android",
    "appPackage": "com.example.app",
    "appActivity": ".MainActivity",
    "automationName": "UiAutomator2"
}

# Initialize the Appium driver
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

try:
    # Perform actions on the app
    # Example: Click a button
    driver.find_element(MobileBy.ID, "com.example.app:id/button_id").click()
    
    # Example: Input text in a text field
    text_field = driver.find_element(MobileBy.ID, "com.example.app:id/text_field_id")
    text_field.send_keys("Hello, Appium!")
    
    # Example: Swipe
    action = TouchAction(driver)
    action.press(x=500, y=1000).move_to(x=500, y=500).release().perform()

    # Add more actions as needed...

    # Pause for a few seconds to observe the changes
    time.sleep(3)

finally:
    # Quit the driver session
    driver.quit()
