from selenium.webdriver.common.by import By

def get_branch_detail_links(driver):
    cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='branch-details.php']")

    branches = []
    for card in cards:
        url = card.get_attribute("href")
        title = card.text.split("\n")[0].strip()

        branches.append({
            "name": title,
            "url": url
        })

    return branches


def scrape_branch_detail(driver, branch):
    driver.get(branch["url"])

    content = driver.find_element(By.CLASS_NAME, "main_info").text

    return {
        "name": branch["name"],
        "url": branch["url"],
        "content": content
    }
