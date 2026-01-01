from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_modular_courses(driver):
    courses = []

    cards = driver.find_elements(By.CSS_SELECTOR, "div.c_cat_box")

    for card in cards:
        try:
            info_text = card.find_element(By.CLASS_NAME, "c_info").text.strip()
        except:
            continue

        lines = [l.strip() for l in info_text.split("\n") if l.strip()]
        name = lines[0] if len(lines) > 0 else ""
        duration = lines[1] if len(lines) > 1 else ""

        try:
            link = card.find_element(
                By.CSS_SELECTOR, "a.c_cat_more_btn"
            ).get_attribute("href")
        except:
            link = ""

        if link and name:
            courses.append({
                "name": name,
                "duration": duration,
                "url": link
            })

    return courses

def scrape_course_detail(driver, course):
    driver.get(course["url"])
    wait = WebDriverWait(driver, 10)

    content = ""

    selectors = [
        (By.CLASS_NAME, "inner_page_wrap"),
        (By.CLASS_NAME, "container"),
        (By.TAG_NAME, "body")
    ]

    for by, value in selectors:
        try:
            element = wait.until(
                EC.presence_of_element_located((by, value))
            )
            content = element.text.strip()
            if content:
                break
        except:
            continue

    return {
        "name": course["name"],
        "duration": course["duration"],
        "url": course["url"],
        "content": content
    }
