from datetime import datetime, timedelta, date
import re

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def test_compare_db1_share_prices():
    # Browser set up
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    # 1. Get to the Deutsche Boerse web page and check if correct page is loaded
    driver.get('https://deutsche-boerse.com/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jarallax-img")))
    if not "Gruppe Deutsche Börse - Gruppe Deutsche Börse" in driver.title:
        raise Exception("The loaded page is wrong or expected one is not available")

    # 1.1 Cookies box check and accept
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cookiescript_injected")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cookiescript_accept")))
    cookies_accept_button = driver.find_element(By.ID, "cookiescript_accept")
    cookies_accept_button.click()

    # 2. Locating elements at DB page and scroll into view
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(3))
    # driver.switch_to.frame(3)
    parent_element_db = driver.find_element(By.CLASS_NAME, "wrapper_t1")
    driver.execute_script("arguments[0].scrollIntoView();", parent_element_db)
    price_element_db = parent_element_db.find_element(By.CLASS_NAME, 'closing_price')
    date_time_parent_element_db = parent_element_db.find_element(By.CLASS_NAME, 'time_date')

    # 3. Get values from elements and save to variables
    price_from_db_web_string = price_element_db.text
    price_from_db_web = convert_currency_string_to_float(price_from_db_web_string)
    time_from_db_web = date_time_parent_element_db.find_element(By.CLASS_NAME, 'time').text
    time_from_db_web = time_from_db_web.replace(" ", "").replace("CEST", "")

    # 4. Visit yahoo.com and check if correct page is loaded
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://finance.yahoo.com/quote/DB1.DE")
    if not "Yahoo is part of the Yahoo family of brands" in driver.title:
        raise Exception("The loaded page is wrong or expected one is not available")

    # 4.1 Cookies box check and accept
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "consent-form")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='btn secondary accept-all ']")))
    accept_cookies_btn = driver.find_element(By.XPATH, "//*[@class='btn secondary accept-all ']")
    accept_cookies_btn.click()

    # 5. Locating elements
    parent_element_yh = driver.find_element(By.ID, 'quote-header-info')
    price_element_yh_web = parent_element_yh.find_element(By.XPATH, "//*[@data-test='qsp-price']")
    time_element_from_yh_web = parent_element_yh.find_element(By.ID, 'quote-market-notice')

    # 6. Get values from elements and save to variables
    time_string_yh_web = time_element_from_yh_web.text
    time_from_yh_web = extract_and_convert_time(time_string_yh_web)
    price_from_yh_web = price_element_yh_web.text
    price_from_yh_web = float(price_from_yh_web)

    # 7. Compare and display prices
    print_text_in_box('TEST RESULT')
    compare_share_data(price_from_db_web, time_from_db_web, price_from_yh_web, time_from_yh_web)

    # 8. End of test
    driver.quit()


def extract_and_convert_time(s):
    # Extract time from the input string
    time_pattern = r'(\d{1,2}:\d{2}(?:AM|PM))'
    match = re.search(time_pattern, s)

    if match:
        time_str = match.group(1)
        # Convert to 24-hour format
        time_obj = datetime.strptime(time_str, '%I:%M%p')
        time_24 = time_obj.strftime('%H:%M')
        return time_24
    else:
        raise Exception("Could not obtain the time of last share price update")


def convert_currency_string_to_float(currency_string):
    cleaned_string = currency_string.replace(",", ".").replace(" ", "").replace("€", "")
    return float(cleaned_string)


def compare_share_data(price1, time1, price2, time2):
    time_format = "%H:%M"
    today = date.today()
    today_date = today.strftime("%B %d, %Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("\nCurrent Date =", today_date)
    print("Current Time =", current_time, "CEST")

    datetime1 = datetime.strptime(time1, time_format)
    datetime2 = datetime.strptime(time2, time_format)

    print("\nDB1 Share price on Deutsche Boerse web page:")
    print(f"Price: {price1}€, Time: {time1} CEST")

    print("\nDB1 Share price on Yahoo web page:")
    print(f"Price: {price2}€, Time: {time2} CEST")

    price_difference = abs(price1 - price2)
    print(f"\nPrice Difference: {price_difference:.2f}")

    time_difference = datetime2 - datetime1
    if time_difference > timedelta(seconds=0):
        print(f"Time Difference: {time_difference} (Yahoo web page has more recent data)")
    elif time_difference < timedelta(seconds=0):
        print(f"Time Difference: {-time_difference} (Deutsche Boerse web page has more recent data)")
    else:
        print("Time Difference: 0 (Both resources have the same data time)")


def print_text_in_box(text):
    border = "+" + "-" * (len(text) + 2) + "+"
    empty_line = "|" + " " * (len(text) + 2) + "|"

    print('\n' + border)
    print(empty_line)
    print("| " + text + " |")
    print(empty_line)
    print(border)
