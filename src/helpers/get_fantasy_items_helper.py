import time

import bs4
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

def replace_None(s):
    if s is None or not s:
        return "--"
    else:
        return s

def format_title(s):
    s = s.replace(":", "")
    s = s.replace("'", "")
    s = s.replace("`", "")
    s = s.replace('"', "")
    s = s.replace(",","")
    s = s.replace(".", "")
    return s

with open("..\\configs\\items.yaml", "a",encoding="utf-8") as f:
    weapons = []
    armor = []
    for n in range(1, 13):
        with SeleniumManager(".", site="",directurl='https://www.dndbeyond.com/equipment?page={}'.format(n),headless=True) as client:

                time.sleep(5)
                #client.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div/table/tfoot/tr/td/div/div[2]").click()
                #client.driver.find_element_by_xpath("/html/body/div[4]/div[3]/ul/li[3]").click()
                print("getting page {}".format(n))
                time.sleep(3)
                rows = client.driver.find_element_by_class_name('listing-igear').find_elements_by_tag_name("li")
                for row in rows:
                    special = dict()
                    gp = row.find_element_by_class_name("list-row-col-cost").text
                    type = row.find_element_by_class_name("list-row-name-secondary-text").text
                    name = row.find_element_by_class_name("list-row-name-primary-text").text
                    weight = row.find_element_by_class_name("list-row-weight-primary-text").text
                    damage_type = row.find_element_by_class_name("list-row-damage-primary-text").text
                    uses = row.find_element_by_class_name("list-row-notes-primary-text").text

                    gp = replace_None(gp)
                    type = replace_None(type)
                    name = replace_None(name)
                    weight = replace_None(weight)
                    damage_type = replace_None(damage_type)
                    uses = replace_None(uses)
                    link = row.find_element_by_class_name(
                        "list-row-name-primary-text").find_element_by_class_name("link").get_attribute("href")
                    desc = ""
                    print("{} | {} | {} | {} | {} | {}".format(name, type, gp, weight, damage_type, uses))

                    with SeleniumManager(".", site="", directurl=link, headless=True) as client2:
                        elements = client2.driver.find_elements_by_class_name("details-container-content-description-text")
                        for ind,elems in enumerate(elements):
                            try:
                                desc = elems.find_element_by_tag_name("p").text
                                print("its",ind)
                            except:
                                pass
                        if "Warding" in uses:
                            armor.append(format_title(name))
                            for ind, elems in enumerate(elements):
                                try:
                                    table = elems.find_element_by_tag_name("table").text
                                    print("its", ind)
                                except:
                                    pass
                            print("table:",table)
                        elif "Combat" in uses and type != "Ammunition":
                            weapons.append(format_title(name))
                            if client2.does_element_exist_by_tag_name("table"):
                                for ind, elems in enumerate(elements):
                                    try:
                                        table = elems.find_element_by_tag_name("table").text
                                        print("its", ind)
                                    except:
                                        pass
                                try:
                                    print("table:", table)
                                except:
                                    pass


                        print(desc)
                        print("-"*50)







