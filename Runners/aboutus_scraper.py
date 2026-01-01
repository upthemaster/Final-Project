from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_about_sunbeam(driver):
    wait = WebDriverWait(driver, 15)

    # Hover on About Us
    about_us = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//nav//a[contains(text(),'About')]")
        )
    )
    driver.execute_script(
        "arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles:true}));",
        about_us
    )
    time.sleep(1)

    # Click About Sunbeam
    about_sunbeam = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//ul[contains(@class,'dropdown-menu')]//a[contains(@href,'about-us')]")
        )
    )
    about_sunbeam.click()
    time.sleep(3)

    paragraphs = driver.find_elements(By.TAG_NAME, "p")

    text = []
    for p in paragraphs:
        if p.text.strip():
            text.append(p.text.strip())

    return text
