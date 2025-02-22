import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def make_csv(columns, tools_and_its_features_list):
    dataframe = pd.DataFrame(columns=columns)
    for tool in tools_and_its_features_list:
        features = sorted(tool.keys())
        features.remove("name")
        features = ["name"] + features
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

    dataframe.to_csv("tools.csv")


def parse_one_tool(description, set_of_features):
    try:
        tool_features = {}
        text = description.text.splitlines()
        tool_features["name"] = text[0]

        index_of_string_to_start = 1

        if re.search(r"^\d+$", text[1]) is None:
            tool_features["description"] = text[1]
            index_of_string_to_start += 1

        if re.search(r"^\d+$", text[2]) is not None:
            tool_features["amount_of_reviews"] = text[2]
            index_of_string_to_start += 1

        if re.search(r"^\d+$", text[1]) is not None:
            tool_features["amount_of_reviews"] = text[1]
            index_of_string_to_start += 1

        for index in range(index_of_string_to_start, len(text)):
            feature, value = text[index].split(": ", 1)
            set_of_features.add(feature)
            tool_features[feature] = value

        return tool_features

    except:
        return {}


def parse_site(driver):
    time.sleep(2.5)
    try:
        pages = driver.find_elements(By.CLASS_NAME, "number")
        amount_of_pages = int(pages[-1].text)

    except:
        print("Could not find amount of pages")
        exit(0)

    set_of_features = set()
    set_of_features.add("description")
    set_of_features.add("amount_of_reviews")
    tools_and_its_features_list = []

    for i in range(amount_of_pages):
        time.sleep(1)
        tools_descriptions = driver.find_elements(
            By.XPATH, "//*[contains(@class,'E-Geio')]"
        )

        set_of_features.add("description")
        set_of_features.add("amount_of_reviews")

        for description in tools_descriptions:
            current_tool_and_its_feature = parse_one_tool(description, set_of_features)
            tools_and_its_features_list.append(current_tool_and_its_feature)

        if i != amount_of_pages - 1:
            driver.find_element(
                By.XPATH, "//*[@id='product-listing-top']/div[3]/div/div[2]/a"
            ).click()

    columns = ["name"] + sorted(list(set_of_features))
    return columns, tools_and_its_features_list


def open_connection():
    chrome_options = Options()
    service = webdriver.ChromeService(
        executable_path="/usr/bin/chromedriver/chromedriver"
    )
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.vseinstrumenti.ru/category/shurupoverty-1774/page1")
    return driver


def main():
    driver = open_connection()
    parse_result = parse_site(driver)
    columns, tools_and_its_features_list = parse_result[0], parse_result[1]
    make_csv(columns, tools_and_its_features_list)
    driver.quit()


main()
