"""
_summary_
"""
import time
from typing import List, Optional

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:
    """
    _summary_
    """

    def __init__(self, url: str = "https://www.worldpadeltour.com/"):
        """
        _summary_

        Args:
            url (_type_, optional): _description_. Defaults to "https://www.worldpadeltour.com/".
        """
        # chrome_options = Options()

        # chrome_options.add_argument("--ignore-certificate-errors")
        # chrome_options.add_argument("--allow-running-insecure-content")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--window-size=1980,1020")
        # chrome_options.add_argument(
        #     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        # )

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)

    def quit(self):
        """
        _summary_
        """
        self.driver.quit()

    def maximize_window(self) -> None:
        """
        _summary_
        """
        self.driver.maximize_window()

    def goto_link(self, link: str) -> None:
        """
        _summary_

        Args:
            link (str): _description_
        """
        self.driver.get(link)

    def click_element(self, xpath: str, delay: int = 5) -> Optional[WebElement]:
        """
        _summary_

        Args:
            xpath (str): _description_
            delay (int): _description_

        Returns:
            Optional[WebElement]: _description_
        """
        try:
            element = WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

            element.click()

            return element
        except TimeoutException as exc:
            print("Click element took too much time to load!", exc)
            return None

    def get_link(self, driver: WebElement, delay: int = 5) -> Optional[str]:
        """
        _summary_

        Args:
            driver (WebElement): _description_
            delay (int, optional): _description_. Defaults to 5.

        Returns:
            Optional[str]: _description_
        """
        try:
            element = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )

            link = element.get_attribute("href")

            return link
        except TimeoutException as exc:
            print("Link element took too much time to load!", exc)
            return None

    def accept_cookies(self, xpath: str = '//*[@id="c-p-bn"]', delay: int = 5) -> None:
        """
        _summary_

        Args:
            xpath (str, optional): _description_. Defaults to '//*[@id="c-p-bn"]'.
            delay (int, optional): _description_. Defaults to 5.
        """
        self.click_element(xpath, delay)

    def look_for_search(
        self, xpath: str = '//input[@id="player-search"]', delay: int = 5
    ) -> Optional[WebElement]:
        """
        _summary_

        Args:
            xpath (str, optional): _description_. Defaults to '//input[@id="player-search"]'.
            delay (int, optional): _description_. Defaults to 5.

        Returns:
            Optional[WebElement]: _description_
        """
        search_bar = self.click_element(xpath, delay)

        return search_bar

    def find_elements_in_container(
        self,
        xpath_container: str,
        xpath_elements: str,
    ) -> List[WebElement]:
        """
        _summary_

        Args:
            xpath_container (str): _description_
            xpath_container_elements (str): _description_

        Returns:
            list: _description_
        """
        container = self.driver.find_element(By.XPATH, xpath_container)
        elements_in_container = container.find_elements(By.XPATH, xpath_elements)

        return elements_in_container

    def find_elements_in_container_by_tag(
        self, driver: WebElement, xpath_container: str, tag: str
    ) -> List[WebElement]:
        """
        _summary_

        Args:
            driver (WebElement): _description_
            xpath_container (str): _description_
            tag (str): _description_

        Returns:
            list: _description_
        """
        container = driver.find_element(By.XPATH, xpath_container)
        elements_in_container = container.find_elements(By.TAG_NAME, tag)

        return elements_in_container


class PaddleScraper(Scraper):
    """
    _summary_

    Args:
        Scraper (_type_): _description_
    """

    def search_player(
        self, player: str, xpath_search_bar: str = '//input[@id="player-search"]'
    ) -> None:
        """
        _summary_

        Args:
            xpath_search_bar (str): _description_
            player (str): _description_
        """
        self.accept_cookies()
        time.sleep(1)

        self.maximize_window()

        self.click_element('//a[@title="Jugadores"]')

        search_bar = self.look_for_search(xpath_search_bar)
        time.sleep(1)

        if search_bar:
            search_bar.send_keys(player)

            time.sleep(1)
        else:
            raise Exception("Search unsuccessful!")

        # self.click_element('//div[@class="c-ranking__block c-ranking__block--search"]')

        player_card = self.driver.find_element(
            By.XPATH, '//div[@class="c-ranking__block c-ranking__block--search"]'
        )
        player_a_tag = player_card.find_element(By.XPATH, ".//a")

        player_a_tag.click()

    def search_all_players(self) -> List[str]:
        """
        _summary_

        Returns:
            list: _description_
        """
        self.accept_cookies()
        time.sleep(1)

        self.maximize_window()

        self.click_element('//a[@title="Jugadores"]')

        containers = self.find_elements_in_container(
            '//div[@class="c-ranking c-ranking--half"]',
            './div[@class="c-ranking__block"]',
        )

        male_players = self.find_elements_in_container_by_tag(
            containers[0], "./ul", "li"
        )
        female_players = self.find_elements_in_container_by_tag(
            containers[1], "./ul", "li"
        )
        time.sleep(1)

        links = []

        for player in male_players:
            link = self.get_link(player)
            links.append(link)

        for player in female_players:
            link = self.get_link(player)
            links.append(link)
        time.sleep(1)

        return links

    def get_info(self) -> pd.DataFrame:
        """
        _summary_

        Returns:
            dict: _description_
        """
        table = self.driver.find_element(
            By.XPATH,
            '//div[@class="c-flex-table c-flex-table--ranking c-flex-table--blue is-visible"]',
        )
        columns = table.find_elements(By.XPATH, "./div")

        tournament_list = self.retrieve_column_info(columns[0])
        date_list = self.retrieve_column_info(columns[2])
        points_list = self.retrieve_column_info(columns[3])

        data_dict = {
            "Tournament": tournament_list,
            "Date": date_list,
            "Points": points_list,
        }

        df_data = pd.DataFrame(data_dict)

        return df_data

    def retrieve_column_info(self, column: WebElement) -> List[str]:
        """
        _summary_

        Args:
            column (WebElement): _description_

        Returns:
            List[str]: _description_
        """
        rows = self.find_elements_in_container_by_tag(column, "./ul", "li")

        data_list = []

        for row in rows:
            data = row.text
            data_list.append(data)

        return data_list

        # try:
        #     price = self.driver.find_element(By.XPATH, '//p[@data-testid="price"]').text

        #     dict_prop["Price"].append(price)
        # except NoSuchElementException:
        #     dict_prop["Price"].append(None)
