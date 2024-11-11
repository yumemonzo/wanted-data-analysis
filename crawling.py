import os
import time
import pandas as pd
import yaml
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def load_job_name():
    with open("./config/crawling.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def setup_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=ko-KR")
    driver = webdriver.Chrome(options=options)

    return driver


def search_job(driver, job_name):
    driver.get("https://www.wanted.co.kr/")
    search_box_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/nav/aside/ul/li[1]')
    search_box_button.click()
    search_box = driver.find_element(By.XPATH, '//*[@id="nav_searchbar"]/div/div[2]/div/form/input')
    search_box.send_keys(job_name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    more_position_button = driver.find_element(By.XPATH, '//*[@id="search_tabpanel_overview"]/div[1]/div[3]/button/div')
    more_position_button.click()


def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def collect_job_data(driver, num_of_positions):
    job_cards, company_names, locations, careers, main_jobs, check_lists, good_lists = [], [], [], [], [], [], []
    for num in tqdm(range(int(num_of_positions)), desc="crawling..."):
        try:
            picture_click_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[3]/div[{num + 1}]'))
            )
            picture_click_button.click()
            time.sleep(1)

            see_more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/button/span[2]'))
            )
            see_more_button.click()

            job_cards.append(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/h1'))
            ).text)
            
            company_names.append(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/a'))
            ).text)
            
            locations.append(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/span[2]'))
            ).text)
            
            careers.append(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/span[4]'))
            ).text)
            
            main_jobs.append(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[1]'))
            ).text)
            
            check_lists.append(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[2]'))
            ).text)
            
            good_lists.append(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[3]'))
            ).text)

            driver.back()
            time.sleep(1)

        except Exception as e:
            print(f"Error at index {num}: {e}")
            break  # 오류 발생 시 루프 탈출

    return pd.DataFrame({
        "직무명": job_cards,
        "회사명": company_names,
        "위치": locations,
        "경력": careers,
        "주요업무": main_jobs,
        "자격요건": check_lists,
        "우대사항": good_lists
    })


def main():
    config = load_job_name()
    
    job_name = config.get("job_name", "")
    driver = setup_driver()
    try:
        search_job(driver, job_name)
        scroll_to_bottom(driver)
        num_of_position = driver.find_element(By.XPATH, '//*[@id="search_tabpanel_position"]/div/div[1]/h2/span')
        df = collect_job_data(driver, int(num_of_position.text))
        os.makedirs('./data', exist_ok=True)
        df.to_csv('./data/crawled_data.csv', index=False)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
