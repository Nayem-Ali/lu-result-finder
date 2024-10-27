import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta


class ResultFinder:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(chrome_options)

    def get_result_page(self, year):
        self.driver.get("https://www.lus.ac.bd/result/")
        time.sleep(5)
        start_date = datetime(year=year, month=3, day=1)
        id_field = self.driver.find_element(By.XPATH, value='//*[@id="student_id"]')
        id_field.send_keys("2012020023")
        dob_field = self.driver.find_element(By.XPATH, value='//*[@id="dob"]')
        search_button = self.driver.find_element(By.XPATH, value='//*[@id="result-form"]/div[1]/div[3]/button')

        for day in range(720):  # Assuming a non-leap year
            current_date = start_date + timedelta(days=day)
            print(f"Day {day + 1}: {current_date.strftime('%Y-%m-%d')}")
            dob_field.send_keys(current_date.strftime('%Y-%m-%d'))
            search_button.click()
            time.sleep(2)

            try:
                result_details = self.driver.find_element(By.XPATH, value='//*[@id="results"]/div/div[1]/div[1]')
                print(current_date.strftime('%Y-%m-%d'))
                break
            except NoSuchElementException:
                dob_field.clear()


bot = ResultFinder()
bot.get_result_page(1999)
