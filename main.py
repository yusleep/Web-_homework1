from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from elasticsearch import Elasticsearch
import time
import pandas as pd
import numpy as np

es = Elasticsearch([{'host':'127.0.0.1','port' :'9200'}])
df = pd.DataFrame()


browser = webdriver.Chrome()
for i in range(1, 600):
    url = "https://hecoinfo.com/txs?a=0x00efb96dbfe641246e961b472c0c3fc472f6a694&p="+str(i)
    browser.get(url)
    time.sleep(1)

    for j in range(1, 50):
        #link = browser.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div/div[2]/table/tbody/tr[q]/td[2]/span/a").get_attribute('href')
        links = browser.find_elements_by_xpath("/html/body/div[1]/main/div[2]/div/div/div[3]/table/tbody/tr/td[2]/span/a")
        link = links[j].get_attribute('href')
        browser.get(link)
        time.sleep(1)
        status = browser.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/span").text
        if status == "Fail":
            browser.back()
            continue
        try:
           usdt = browser.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div/div[7]/div[2]/ul/li[2]/div/span[6]/span").text
        except NoSuchElementException:
            browser.back()
            continue
        dizhi = browser.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div/div[7]/div[2]/ul/li[1]/div/span[4]/a/span").text
        name = browser.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div/div[7]/div[2]/ul/li[1]/div/a").text
        if dizhi == "0x8611a52e8ac5e10651df7c4b58f42536f0bd2e7e":
            if name == "BXHToken (BXH)":
                bxh = browser.find_element_by_xpath("/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div/div[7]/div[2]/ul/li[1]/div/span[6]").text
                usdt = [usdt]
                bxh = [bxh]
                dataframe = pd.DataFrame({'usdt':usdt,'bxh':bxh})
                df = df.append(dataframe,ignore_index=True)
                print(df)
                print("\n")
                df.to_csv("test.csv", index=False, sep=',')
        browser.back()






