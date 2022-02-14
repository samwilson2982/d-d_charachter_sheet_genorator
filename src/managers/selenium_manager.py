import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from ..helpers import ConfigHelper
from ..helpers import DirHelper
from selenium.webdriver.firefox.options import Options
import time
import re


class SeleniumManager(object):
    def __init__(self, download_dir, site,directurl=False,headless=True):

        fp = webdriver.FirefoxProfile()
        options = Options()
        options.headless = headless
        fp.set_preference('browser.download.folderList', 2)
        fp.set_preference('browser.download.managers.showWhenStarting', False)
        fp.set_preference('browser.download.dir', download_dir)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                          'text/plain, application/vnd.ms-excel, '
                          + 'text/csv, text/comma-separated-values, '
                          + 'application/octet-stream, '
                          + 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        self.download_dir = download_dir
        self.driver = webdriver.Firefox(firefox_profile=fp, options=options)
        self.site = site
        if not directurl:
            if site:
                self.data = ConfigHelper.parse_config(DirHelper.local_path("../configs/logins.yaml"))["logins"][site]
                self.url = self.data["url"]
            else:
                self.url = "https://www.google.com/"
        else:
            self.url = directurl
            self.data = None
        if "{}" in self.url:
            month_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print("time_ranges", month_ago, "to", today)
            self.url = self.url.format(month_ago, today)
        print("pulling from url:", self.url)

    def __enter__(self):
        self.driver.get(self.url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver = None

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def load_new_url(self, new_url):
        time.sleep(0.5)
        self.driver.get(new_url)

    def login(self):
        try:
            username = self.driver.find_element_by_xpath(self.data["username_xpath"])
            username.send_keys(self.data["username"])
            password = self.driver.find_element_by_xpath(self.data["password_xpath"])
            password.send_keys(self.data["password"])
            password.send_keys(Keys.ENTER)
        except Exception as e:
            print("auth failed, may not be auth page, check error")
            print(str(e))

    def setup(self):

        setup_xpaths = self.data['setup']
        for xpath in setup_xpaths:
            time.sleep(2)
            elm = self.driver.find_element_by_xpath(xpath)
            self.driver.execute_script("arguments[0].click();", elm)
            time.sleep(1)

    def executue_xpaths(self):
        time.sleep(5)
        self.setup()
        xpaths = self.data["xpaths"]
        for key, value in xpaths.items():
            print("executing next phase: getting {}".format(key))
            action = ActionChains(self.driver)
            action.move_by_offset(500, 500)
            for xpath in value:
                try:
                    if self.check_exists_by_xpath('//*[@id="close-ad"]'):
                        elm = self.driver.find_element_by_xpath('//*[@id="close-ad"]')
                        self.driver.execute_script("arguments[0].click();", elm)
                    time.sleep(2)
                    elm = self.driver.find_element_by_xpath(xpath)
                    if xpath == '//*[@id="datefilter"]':
                        self.driver.execute_script("arguments[0].click();", elm)
                        time.sleep(1)
                        self.driver.execute_script(
                            "document.getElementsByClassName('ranges')[1].firstChild.children[1].click()")
                        time.sleep(1)


                    else:
                        self.driver.execute_script("arguments[0].click();", elm)
                    time.sleep(1)
                    title = self.driver.find_element_by_xpath(
                        "/html/body/div[8]/div[1]/div/div/div/div[2]/div[2]/div[1]").text.replace(" ", "_")
                except Exception as e:
                    print("whoops " + str(e))
            print("taking screenshot! {}".format(title))

            self.take_screenshot(title)

    def take_screenshot(self, title):
        title = title + "-" + self.site + ".png"
        self.driver.save_screenshot(title)

    def get_text_from_element(self,xpath):
        return self.driver.find_element_by_xpath(xpath).text

    def refresh_page(self):
        self.driver.refresh()
        time.sleep(1.786544)

    def does_element_exist_by_tag_name(self,tagname):
        if self.driver is not None:
            tags = self.driver.find_elements_by_tag_name(tagname)
            if len(tags):
                return True
            else:
                return False
        else:
            raise Exception("connection is null!, get a new url")

    def strip_tags(self,s):
        s = s.replace(":", "")
        s = s.replace("'", "")
        s = s.replace("`", "")
        s = s.replace('"', "")
        s = re.sub('<[^>]*>', '', s)
        return s

    def html_table2_list(self,html_table):
        table = []
        html_string = "".join(html_table.split("\n"))
        incidents = html_string.split("</tr>")
        for incident in incidents:
            if "</td>" in incident:
                cells = incident.split("</td>")
            if "</th>" in incident:
                cells = incident.split("</th>")


            print(cells)
            table.append([self.strip_tags(x) for x in cells])
            return table


