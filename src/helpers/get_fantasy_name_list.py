import time

from bs4 import BeautifulSoup
import requests
from src.managers import SeleniumManager
import time

def double_name(race):
    first_names = []
    last_names = []
    with SeleniumManager(".","fantasy") as client:
        while(len(first_names) < 500):
            client.refresh_page()
            nam = client.driver.find_element_by_xpath("//*[@id='result']").text
            for n in nam.split("\n"):
                first_names.append(n)
                print(n)

        while (len(last_names) < 500):
            client.refresh_page()
            nam = client.driver.find_element_by_xpath("//*[@id='result']").text
            for n in nam.split("\n"):
                last_names.append(n)
                print(n)


    with open("..\\configs\\names.yaml", "a") as f:
        f.write("{}:\n".format(race))
        for fn,ln in zip(first_names,last_names):
            f.write("\t- '{} {}'\n".format(fn,ln))


def single_name(race):
    first_names = []
    with SeleniumManager(".", "fantasy") as client:
        while (len(first_names) < 500):
            client.refresh_page()
            nam = client.driver.find_element_by_xpath("//*[@id='result']").text
            for n in nam.split("\n"):
                first_names.append(n)
                print(n)


    with open("..\\configs\\names.yaml", "a") as f:
        f.write("{}:\n".format(race))
        for fn in first_names:
            f.write("\t- '{}'\n".format(fn))

double_name("Tiefling")