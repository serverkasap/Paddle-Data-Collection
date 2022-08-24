import time

from utils.scraper import PaddleScraper, Scraper

if __name__ == "__main__":
    # bot = Scraper()

    # time.sleep(3)

    # bot.accept_cookies()

    # bot.maximize_window()

    # time.sleep(3)

    # bot.click_element('//a[@title="Jugadores"]')

    # time.sleep(3)

    # bot.quit()

    bot = PaddleScraper()

    # bot.search_all_players()

    bot.search_player("Candido Jorge Alfaro")

    candido_data = bot.get_info()

    time.sleep(3)

    print(candido_data)

    bot.quit()
