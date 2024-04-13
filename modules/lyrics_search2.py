import re
import requests
import urllib
from bs4 import BeautifulSoup
from typing import Optional
from .lyrics_scraper import Tekstowo,AZLyrics,Groove,Teksciory


class GetLyricsOutsideYT2:
    """Class for retrieving lyrics from various external sources via Yahoo search."""

    def __init__(self) -> None:
        """
        Initializes a GetLyricsOutsideYT2 object.
        """
        pass

    def search_lyrics_yahoo(self,title: str) -> Optional[str]:
        """
        Searches for lyrics of a song using Yahoo search and retrieves them from external sources.

        Parameters:
            title (str): The title of the song.

        Returns:
            Optional[str]: The lyrics of the song if found, or None.
        """
        url = f"https://search.yahoo.com/search?q={title} lyrics tekstowo groove teksciory AZLyrics".replace(" ", "%20")
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            url = link.get('href')
            fields = url.split('/')
            for part in fields:
                try:
                    if part.startswith('RU='):
                        link_d = urllib.parse.unquote(str(part).split('=')[1])
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
                    return None
            
        return None