import json
from driver_manager import get_driver
from courses_scraper import get_modular_courses, scrape_course_detail


def main():
    driver = get_driver()

    try:
        driver.get("https://www.sunbeaminfo.in/modular-courses-home")

        courses = get_modular_courses(driver)
        courses_data = []

        for course in courses:
            detail = scrape_course_detail(driver, course)
            courses_data.append(detail)

        with open("data/modular_courses.json", "w", encoding="utf-8") as f:
            json.dump(courses_data, f, indent=2, ensure_ascii=False)

        print("Modular courses scraped Successfully.", len(courses_data))

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
