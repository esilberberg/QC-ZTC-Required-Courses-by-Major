# 1_get_core_courses.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure headless Chrome options
options = Options()
options.add_argument("--headless=new")  
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(options=options)

try:
    major_list = []

    # 1. COLLECT ALL MAJORS (LINKS)
    print(f"--- Step 1: Collecting Majors ---")

    # >>>>>> SET THE PAGE NUMBER <<<<<
    page_num = input("What page in the undergraduate bulletin should I crawl? ")
    
    page_url = f"https://qc-undergraduate.catalog.cuny.edu/programs?page={page_num}"
    print(f"Scraping list from Page {page_num}: {page_url}")
    
    driver.get(page_url)

    # Wait for table to load
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.ui-font.bg-white"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        all_tds = row.find_elements(By.TAG_NAME, "td")
        
        if len(all_tds) >= 3:
            program_category = all_tds[2].get_attribute("textContent").strip()
            
            if program_category.lower() == "major":
                degree_type = all_tds[1].get_attribute("textContent").strip()
                sticky_tds = row.find_elements(By.CSS_SELECTOR, "td.sticky-cell.bg-white")
                
                if sticky_tds:
                    a_tags = sticky_tds[0].find_elements(By.TAG_NAME, "a")
                    
                    if a_tags:
                        link = a_tags[0]
                        program_name = link.get_attribute("textContent").strip()
                        href = link.get_attribute("href")
                        
                        major_list.append({
                            "program_name": program_name,
                            "degree_type": degree_type,
                            "url": href
                        })

    print(f"\nDone! Total Major links collected: {len(major_list)}\n")

    # 2. CYCLE THROUGH ALL MAJORS & EXTRACT CORE COURSES
    print("--- Step 2: Extracting Core Courses for Each Major ---")
    spreadsheet_rows = []

    for index, major in enumerate(major_list, start=1):
        print(f"[{index}/{len(major_list)}] Processing: {major['program_name']}")
        
        driver.execute_script("window.open(arguments[0], '_blank');", major['url'])
        driver.switch_to.window(driver.window_handles[-1])
        
        found_courses = []

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test='accordion-button']"))
            )
            
            accordion_buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-test='accordion-button']")
            
            for btn in accordion_buttons:
                btn_text = btn.get_attribute("textContent").strip()
                
                if "Major Requirements - Core" in btn_text:
                    if btn.get_attribute("aria-expanded") == "false":
                        driver.execute_script("arguments[0].click();", btn)
                    
                    panel = btn.find_element(By.XPATH, "following-sibling::div[@data-test='accordion-div']")
                    courses = panel.find_elements(By.CSS_SELECTOR, "button.link.cursor-pointer.text-left")
                    
                    for course in courses:
                        course_name = course.get_attribute("textContent").strip()
                        if course_name:
                            found_courses.append(course_name)

        except Exception as e:
            print(f"  Could not process {major['program_name']}: {e}")

        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Add findings to CSV row buffer
        if found_courses:
            for course in found_courses:
                spreadsheet_rows.append({
                    "Program": major['program_name'],
                    "Degree": major['degree_type'],
                    "URL": major['url'],
                    "Required_Course": course
                })
        else:
            spreadsheet_rows.append({
                "Program": major['program_name'],
                "Degree": major['degree_type'],
                "URL": major['url'],
                "Required_Course": "N/A"
            })

    # 3. EXPORT TO Excel
    filename = f"qc_majors_core_courses_{page_num}.xlsx"
    fieldnames = ["Program", "Degree", "URL", "Required_Course"]

    # Convert extracted list of dicts to pandas DataFrame
    df = pd.DataFrame(spreadsheet_rows)
    
    df.to_excel(filename, index=False)

    print(f"\nSuccessfully exported {len(spreadsheet_rows)} course rows to '{filename}'!")

finally:
    driver.quit()
