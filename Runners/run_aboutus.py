import json
import os
from driver_manager import get_driver
from aboutus_scraper import scrape_about_sunbeam
from branches_scraper import get_branch_detail_links, scrape_branch_detail

def main():
    driver = get_driver()

    try:
        driver.get("https://www.sunbeaminfo.in/")
        about_text = scrape_about_sunbeam(driver)

        os.makedirs("data", exist_ok=True)

        with open("data/about_us.json", "w", encoding="utf-8") as f:
            json.dump(
                {"about_sunbeam": about_text},
                f,
                indent=2,
                ensure_ascii=False
            )

        print("About Sunbeam scraped")

        driver.get("https://www.sunbeaminfo.in/sunbeam-branches-home")
        branch_links = get_branch_detail_links(driver)

        branches_data = {}

        for branch in branch_links:
            detail = scrape_branch_detail(driver, branch)
            branches_data[detail["name"]] = detail["content"]

        with open("data/branches.json", "w", encoding="utf-8") as f:
            json.dump(branches_data, f, indent=2, ensure_ascii=False)

        print("Branches scraped")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
