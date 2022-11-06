import json
import os
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

print("Bot started")

#  Set up the Chrome driver
options = Options()
options.add_argument("--disable-gpu")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
os.environ['WDM8LOCAL'] = '1'
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
print("Assertion - successfully found chrome driver")


# Get all scores from the livescores page
driver.get("https://www.livescores.com/")
time.sleep(2)
scores = driver.find_elements(by=By.CSS_SELECTOR, value=".gh")
match_time = driver.find_elements(by=By.CSS_SELECTOR, value=".lg")

json_path = os.path.join(os.path.dirname(__file__), "livescores.json")

scores_list = []
for index in range(len(scores)):
    temp_list = (scores[index].text.split("\n"))
    temp = {
        "home": temp_list[0],
        "away": temp_list[2],
        "home_score": temp_list[1].split(" - ")[0],
        "away_score": temp_list[1].split(" - ")[1],
        "time": match_time[index].text
    }
    scores_list.append(temp)

time.sleep(3)
driver.close()

data = {
    "date": datetime.now().strftime("%d/%m/%Y"),
    "scores": scores_list
}

# Write to json file
with open(json_path, "w") as file:
    json.dump(data, file, indent=4)

print("Bot finished")
