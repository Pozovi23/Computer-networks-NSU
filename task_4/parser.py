import re
import time

from database import write_to_database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def parse_one_tool(description, set_of_features):
    try:
        tool_features = {}
        text = description.text.splitlines()
        tool_features["name"] = text[0][:50]

        index_of_string_to_start = 1

        if re.search(r"^\d+$", text[1]) is None:
            tool_features["description"] = text[1][:50]
            index_of_string_to_start += 1

        if re.search(r"^\d+$", text[2]) is not None:
            tool_features["amount_of_reviews"] = text[2][:50]
            index_of_string_to_start += 1

        if re.search(r"^\d+$", text[1]) is not None:
            tool_features["amount_of_reviews"] = text[1][:50]
            index_of_string_to_start += 1

        for index in range(index_of_string_to_start, len(text)):
            feature, value = text[index].split(": ", 1)
            set_of_features.add(feature)
            tool_features[feature] = value[:50]

        return tool_features

    except:
        return {}


def parse_site(driver):
    time.sleep(2.5)

    set_of_features = set()
    set_of_features.add("description")
    set_of_features.add("amount_of_reviews")
    tools_and_its_features_list = []

    time.sleep(1)
    tools_descriptions = driver.find_elements(
        By.XPATH, "//*[contains(@class,'E-Geio')]"
    )

    for description in tools_descriptions:
        current_tool_and_its_feature = parse_one_tool(description, set_of_features)
        tools_and_its_features_list.append(current_tool_and_its_feature)

    columns = ["name"] + sorted(list(set_of_features))
    return columns, tools_and_its_features_list


def open_connection(number_of_page):
    chrome_options = Options()
    service = webdriver.ChromeService(
        executable_path="/usr/bin/chromedriver/chromedriver"
    )
    driver = webdriver.Chrome(service=service)
    driver.get(
        "https://www.vseinstrumenti.ru/category/shurupoverty-1774/page"
        + str(number_of_page)
    )
    return driver


def parser(number_of_page):
    driver = open_connection(number_of_page)
    parse_result = parse_site(driver)
    columns, tools_and_its_features_list = parse_result[0], parse_result[1]
    write_to_database(tools_and_its_features_list)
    driver.quit()
