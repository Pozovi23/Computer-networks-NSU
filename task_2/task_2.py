from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

chrome_options = Options()
cService = webdriver.ChromeService(executable_path='/usr/bin/chromedriver/chromedriver')
driver = webdriver.Chrome(service=cService)


driver.get('https://www.vseinstrumenti.ru/category/shurupoverty-1774/page2')

time.sleep(2.5)
element = driver.find_elements(By.XPATH, "//*[contains(@class,'E-Geio')]")

set_of_features = set()

set_of_features.add('description')
set_of_features.add('amount_of_reviews')

tools = []

for el in element:
    tool_features = {}
    text = el.text.splitlines()
    # print(el.text)
    tool_features['name'] = text[0]
    # print(re.search(r"^\d+$", text[1]) is not None)

    index_of_string_to_start = 1

    if text[1].find(':') == -1 and (re.search(r"^\d+$", text[1]) is None):
        tool_features['description'] = text[1]
        index_of_string_to_start += 1

    if text[2].find(':') == -1 and (re.search(r"^\d+$", text[2]) is not None):
        tool_features['amount_of_reviews'] = text[2]
        index_of_string_to_start += 1

    if text[1].find(':') == -1 and (re.search(r"^\d+$", text[1]) is not None):
        tool_features['amount_of_reviews'] = text[1]
        index_of_string_to_start += 1

    for index in range(index_of_string_to_start, len(text)):
        feature, value = text[index].split(": ")
        set_of_features.add(feature)
        tool_features[feature] = value

    tools.append(tool_features)


columns = ['name'] + sorted(list(set_of_features))

dataframe = pd.DataFrame(columns=columns)
for tool in tools:
    features = sorted(tool.keys())
    features.remove("name")
    features = ['name'] + features
    row_values = []

    index_in_mas_of_features = 0
    for index_of_column_in_dataframe in range(len(columns)):
        if index_in_mas_of_features == len(features):
            break

        name_of_current_feature_of_tool = features[index_in_mas_of_features]

        if name_of_current_feature_of_tool == columns[index_of_column_in_dataframe]:
            row_values.append(tool[name_of_current_feature_of_tool])
            index_in_mas_of_features += 1
        else:
            row_values.append("")

    dataframe = pd.concat([dataframe, pd.DataFrame([tool])], ignore_index=True)


dataframe.to_csv('tools.csv')
driver.quit()
