import time
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import chromedriver_autoinstaller

app = Flask(__name__)


class ResultFinder:
    def __init__(self):
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_result_page(self, student_id, year):
        self.driver.get("https://www.lus.ac.bd/result/")
        time.sleep(5)
        start_date = datetime(year=year, month=1, day=1)
        id_field = self.driver.find_element(By.XPATH, value='//*[@id="student_id"]')
        id_field.send_keys(student_id)
        dob_field = self.driver.find_element(By.XPATH, value='//*[@id="dob"]')
        search_button = self.driver.find_element(By.XPATH, value='//*[@id="result-form"]/div[1]/div[3]/button')

        for day in range(720):  # Loop through days
            current_date = start_date + timedelta(days=day)
            dob_field.send_keys(current_date.strftime('%d-%m-%Y'))
            search_button.click()
            time.sleep(2)

            try:
                result_details = self.driver.find_element(By.XPATH, value='//*[@id="results"]/div/div[1]/div[1]')
                return {"date_of_birth": current_date.strftime('%d-%m-%Y'), "result_details": result_details.text}
            except NoSuchElementException:
                dob_field.clear()
        return {"error": "Result not found"}


result_finder = ResultFinder()


@app.route('/find-result', methods=['POST'])
def find_result():
    data = request.get_json()
    student_id = data.get("student_id")
    year = data.get("year")
    result = result_finder.get_result_page(student_id, year)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
