import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Data Cleaning
data = pd.read_csv("sample.csv")
data["Country"] = ["INDIA", "FR", "US", "CZ", "RU"]

#date forwarded a month because past dates are invalid
data["Validity Begins"][0] = data["Validity Begins"][0][:4]+"6"+data["Validity Begins"][0][5:]
data["Validity Begins"][4] = data["Validity Begins"][4][:4]+"6"+data["Validity Begins"][4][5:]

#date changed to proper format
data["Validity Begins"] = [v[:6]+"20"+v[6:] for v in data["Validity Begins"]]
data["Powered by"] = data["Powered by"].replace(np.nan, False)

# selenium driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# website
driver.get("https://edalnice.cz/en/bulk-purchase/index.html")

#close pop-up
time.sleep(5)
refuse = driver.find_element_by_xpath("/html/body/footer/div[2]/div/div/div[2]/div/button[2]")
refuse.click()

#base path for entry form-1
form_path = "/html/body/main/div/div/div/div/div/div/form/div/div/"

for i in range(5):
    c, d, l, p, v = data.iloc[i].values
    if i == 0:
        item_path = "div"
    else:
        item_path = f"div[{i+1}]"

    country = driver.find_element_by_xpath(form_path + item_path + "/div[2]/div/div/div/div/div[2]/input")
    country.send_keys(c)
    time.sleep(5)
    country.send_keys(Keys.RETURN)

    # "/html/body/main/div/div/div/div/div/div/form/div/div/div/div[2]/div[2]/div/div/input"
    date = driver.find_element_by_xpath(form_path + item_path + "/div[2]/div[2]/div/div/input")
    date.send_keys(d)
    date.send_keys(Keys.RETURN)

    licence = driver.find_element_by_xpath(form_path + item_path + "/div[3]/div/div/div/input")
    licence.send_keys(l)
    licence.send_keys(Keys.RETURN)

    if p is not False:
        lpg = driver.find_element_by_xpath(form_path + item_path + "/div[4]/div/div")
        lpg.click()
        if p == "Natural Gas":
            powered_by = driver.find_element_by_xpath(form_path + item_path + "/div[4]/div/div[2]/div/div/div")
            powered_by.click()
        elif p == "Biomethane":
            powered_by = driver.find_element_by_xpath(form_path + item_path + "/div[4]/div/div[2]/div/div[2]/div")
            powered_by.click()

    if v == "Annual":
        vignette = driver.find_element_by_xpath(form_path + item_path + "/fieldset/div/div/div/div[1]/div/div")
        vignette.click()
    elif v == "30-day":
        vignette = driver.find_element_by_xpath(form_path + item_path + "/fieldset/div/div/div/div[2]/div/div")
        vignette.click()
    elif v == "10-day":
        vignette = driver.find_element_by_xpath(form_path + item_path + "/fieldset/div/div/div/div[3]/div/div")
        vignette.click()

    if i != 4:
        new_batch = driver.find_element_by_xpath(form_path + item_path + "/div[5]/button")
        new_batch.click()

continue_to_page2 = driver.find_element_by_xpath("/html/body/main/div/div/div/div/div/div/form/div/div[2]/div/div[8]/div/button")
continue_to_page2.click()
time.sleep(3)

continue_to_page3 = driver.find_element_by_xpath("/html/body/main/div/div/div/div/div/div/div/div/div[2]/div/div[8]/div/button")
continue_to_page3.click()

email_id = "sample@gmail.com"
email = driver.find_element_by_id("email-input")
email.send_keys(email_id)
email_confirm = driver.find_element_by_id("email-confirmation-input")
email_confirm.send_keys(email_id)

payment_card = driver.find_element_by_id("card_payment_radio_array_option")
payment_card.click()

terms = driver.find_element_by_id("_termsAgreement-true")
terms.click()

pay_btn = driver.find_element_by_xpath("/html/body/main/div/div/div/div/div/div/form/div/div[2]/div/div[10]/div/button")
pay_btn.click()

CARD_NUMBER = '5422000180911025'
CARD_VALIDITY = '05/25'
CARD_CVV = '913'

time.sleep(15)
card_no = driver.find_element_by_id("cardnumber")
card_no.send_keys(CARD_NUMBER)

card_val = driver.find_element_by_id("expiry")
card_val.send_keys(CARD_VALIDITY)

card_cvv = driver.find_element_by_id("cvc")
card_cvv.send_keys(CARD_CVV)

pay_submit = driver.find_element_by_id("pay-submit")
pay_submit.click()

time.sleep(25)

driver.quit()