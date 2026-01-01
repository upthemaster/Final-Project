from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class InternshipScraper:
    URL = "https://www.sunbeaminfo.in/internship"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def scrape(self):
        self.driver.get(self.URL)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        return {
            "available_programs": self._available_programs(),
            "training_structure": self._training_structure(),
            "batch_schedule": self._batch_schedule()
        }

    def _available_programs(self):
        data = []
        self._open_accordion("//a[@href='#collapseSix']")

        rows = self.driver.find_element(By.ID, "collapseSix") \
            .find_element(By.TAG_NAME, "tbody") \
            .find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue

            data.append({
                "Technology": cols[0].text.strip(),
                "Aim": cols[1].text.strip(),
                "Prerequisite": cols[2].text.strip(),
                "Learning": cols[3].text.strip(),
                "Location": cols[4].text.strip()
            })
        return data

    def _training_structure(self):
        data = []
        self._open_accordion("//a[@href='#collapseOneA']")

        rows = self.driver.find_element(By.ID, "collapseOneA") \
            .find_element(By.CLASS_NAME, "list_style") \
            .find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 4:
                continue

            data.append({
                "Duration": cols[1].text.strip(),
                "Structure": cols[2].text.strip(),
                "Mode": cols[3].text.strip()
            })
        return data

    def _batch_schedule(self):
        data = []

        table = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-responsive"))
        ).find_element(By.TAG_NAME, "tbody")

        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 7:
                continue

            data.append({
                "Batch": cols[1].text.strip(),
                "Duration": cols[2].text.strip(),
                "Start Date": cols[3].text.strip(),
                "End Date": cols[4].text.strip(),
                "Time": cols[5].text.strip(),
                "Fees": cols[6].text.strip()
            })
        return data

    def _open_accordion(self, xpath):
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()
        time.sleep(2)
