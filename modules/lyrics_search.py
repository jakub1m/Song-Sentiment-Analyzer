from bs4 import BeautifulSoup
from typing import Optional
from .lyrics_scraper import Tekstowo,AZLyrics,Teksciory,Groove
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

class GetLyricsOutsideYT:
    """Class for searching and retrieving song lyrics from Google search results using Selenium."""

    def __init__(self) -> None:
        """
        Initializes a GetLyricsOutsideYT object.
        """
        pass

    def search_lyrics_yahoo(self,title: str) -> Optional[str]:
        """
        Searches for song lyrics using Google search results and retrieves them from external sources.

        Parameters:
            title (str): The title of the song.

        Returns:
            Optional[str]: The lyrics of the song if found, or None.
        """
        try:
            print("google")
            options = uc.ChromeOptions()
            options.headless = True
            options.add_argument("--headless")
            driver = uc.Chrome(options=options)
            driver.get(f"https://www.google.pl/search?q={title} lyrics".replace(" ", "%20"))
            try:
                sleep(3)
                response = driver.page_source
                soup = BeautifulSoup(response, 'html.parser')
                buttons = soup.find_all('button', text="Odrzuć wszystko")
                for button in buttons:
                    button_id = button.get('id')
                driver.find_element(By.ID, button_id).click()
                sleep(1.5)
            except:
                try:
                    sleep(2)
                    response = driver.page_source
                    soup = BeautifulSoup(response, 'html.parser')
                    buttons = soup.find_all('button', text="Odrzuć wszystko")
                    for button in buttons:
                        button_id = button.get('id')
                    driver.find_element(By.ID, button_id).click()
                    
                    sleep(2)
                except:
                    sleep(2)
                    response = driver.page_source
                    soup = BeautifulSoup(response, 'html.parser')
                    buttons = soup.find_all('button', text="Odrzuć wszystko")
                    for button in buttons:
                        button_id = button.get('id')
                    driver.find_element(By.ID, button_id).click()
                    sleep(2)
            try:
                response = driver.page_source
                driver.quit()
                soup = BeautifulSoup(response, 'html.parser')
                for link in soup.find_all('a', href=True):
                    link_d = link['href']
                    print(link_d)
                    if "https://www.tekstowo.pl/piosenka," in link_d:
                        tekstowo_scraper = Tekstowo()
                        tekstowo_scraper.get_data(link_d)
                        lyrics = tekstowo_scraper.get_lyrics()
                        print("tekstowo")
                        return lyrics
                    elif "https://www.groove.pl/" in link_d and "piosenka" in link_d:
                        groove_scraper = Groove()
                        groove_scraper.get_data(link_d)
                        lyrics = groove_scraper.get_lyrics()
                        print("groove")
                        return lyrics
                    elif "https://teksciory.interia.pl/" in link_d and "tekst-piosenki" in link_d:
                        teksciory_scraper = Teksciory()
                        teksciory_scraper.get_data(link_d)
                        lyrics = teksciory_scraper.get_lyrics()
                        print("teksciory")
                        return lyrics
                    elif "https://www.azlyrics.com/lyrics" in link_d:
                        AZLyrics_scraper = AZLyrics()
                        AZLyrics_scraper.get_data(link_d)
                        lyrics = AZLyrics_scraper.get_lyrics()
                        print("AZLyrics")
                        return lyrics
            except Exception as e:
                pass
            finally:
                driver.quit()
            return None
        except:
            try:
                driver.quit()
            except:
                pass
            return None
