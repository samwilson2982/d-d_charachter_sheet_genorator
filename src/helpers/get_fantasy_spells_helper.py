import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from src.managers import SeleniumManager
import re
import requests
from src.helpers import DirHelper

def strip_tags(s):
    s = s.replace(":","")
    s = s.replace("'", "")
    s = s.replace("`", "")
    s = s.replace('"', "")
    s = re.sub('<[^>]*>', '', s)
    return s

with SeleniumManager(".", site="",directurl="https://dndspellslist.com/spells/absorb-elements",headless=True) as client:
        time.sleep(5)
        #client.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div/table/tfoot/tr/td/div/div[2]").click()
        #client.driver.find_element_by_xpath("/html/body/div[4]/div[3]/ul/li[3]").click()
        with open("..\\configs\\spells.yaml", "a",encoding="utf-8") as f:
            f.write("Descriptions:\n")
            for n in range(9):
                spell_rows = client.driver.find_elements_by_xpath("//*[@id='root']/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div/table/tbody/tr[@class='MuiTableRow-root MuiTableRow-hover']")
                print(spell_rows)
                for row in spell_rows:
                    name_elm = row.find_elements_by_tag_name("td")[0]
                    spell_name = name_elm.text
                    name_elm.click()
                    desc = client.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div[2]/div/p[1]").text
                    higher_level = client.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div[2]/div/p[2]").text
                    print(spell_name)
                    f.write("\t{}:\n".format(strip_tags(spell_name)))
                    print(desc)
                    f.write("\t\tDescription: '{}'\n".format(strip_tags(desc)))
                    print(higher_level)
                    f.write("\t\tMore: '{}'\n".format(strip_tags(higher_level)))
                    print("-"*50)
                    f.write("\n")
                client.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div/table/tfoot/tr/td/div/div[3]/span[4]/button/span[1]").click()
                print("loading page {} of 9".format(n+1))
                time.sleep(2)



