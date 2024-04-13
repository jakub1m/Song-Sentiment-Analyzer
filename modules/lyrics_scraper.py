import requests
import json
from bs4 import BeautifulSoup

class Tekstowo:
    """Class for scraping lyrics from the Tekstowo website."""
    def __init__(self) -> None:
        """
        Initializes a Tekstowo object.
        """
        self.data = None

    def get_data(self, url: str) -> None:
        """
        Retrieves HTML data from the specified URL.

        Parameters:
            url (str): The URL of the webpage.

        Returns:
            None
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.data = soup

    def get_lyrics(self) -> str:
        """
        Extracts lyrics from the HTML data.

        Returns:
            str: The lyrics of the song if found, or a message indicating that lyrics were not found.
        """
        lyrics_div = self.data.find('div', class_ = 'inner-text')
        if lyrics_div:
            tekst =  "\n".join(line.strip() for line in lyrics_div.get_text().split("\n") if line.strip())
            print(tekst)
            return tekst
        else:
            return "Lyrics not found on the webpage"

class AZLyrics():
    """Class for scraping lyrics from the AZLyrics website."""
    def __init__(self) -> None:
        """
        Initializes a AZLyrics object.
        """
        self.data = None

    def get_data(self, url: str) -> None:
        """
        Retrieves HTML data from the specified URL.

        Parameters:
            url (str): The URL of the webpage.

        Returns:
            None
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.data = soup

    def get_lyrics(self) -> str:
        """
        Extracts lyrics from the HTML data.

        Returns:
            str: The lyrics of the song if found, or a message indicating that lyrics were not found.
        """
        lyrics_div = self.data.find('div', class_ = 'col-xs-12 col-lg-8 text-center')
        if lyrics_div:
            tekst = "\n".join(line.strip() for line in lyrics_div.get_text().split("\n") if line.strip())
            print(tekst)
            return tekst
        else:
            return "Lyrics not found on the webpage"
        
class Teksciory():
    """Class for scraping lyrics from the Teksciory website."""
    def __init__(self) -> None:
        """
        Initializes a Teksciory object.
        """
        self.data = None

    def get_data(self, url: str) -> None:
        """
        Retrieves HTML data from the specified URL.

        Parameters:
            url (str): The URL of the webpage.

        Returns:
            None
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.data = soup

    def get_lyrics(self) -> str:
        """
        Extracts lyrics from the HTML data.

        Returns:
            str: The lyrics of the song if found, or a message indicating that lyrics were not found.
        """
        lyrics_div = self.data.find('div', class_='lyrics--text')
        if lyrics_div:
            lyrics = lyrics_div.get_text(separator='\n').strip()
            return lyrics
        else:
            return "Lyrics not found on the webpage"


class Groove:
    def __init__(self) -> None:
        """
        Initializes a Groove object.
        """
        self.data = None
    
    def get_data(self, url: str) -> None:
        """
        Retrieves HTML data from the specified URL.

        Parameters:
            url (str): The URL of the webpage.

        Returns:
            None
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.data = soup
        lyrics_div = soup.find('div', class_='mid-content-content song-description')

    def get_lyrics(self) -> str:
        """
        Extracts lyrics from the HTML data.

        Returns:
            str: The lyrics of the song if found, or a message indicating that lyrics were not found.
        """
        lyrics_div = self.data.find('div', class_='mid-content-content song-description')
        lyrics = lyrics_div.get_text(separator='\n').strip()
        return lyrics
    

tekstowo =Tekstowo()
tekstowo.get_data("https://www.tekstowo.pl/piosenka,atika_patum_,atikapatum.html")
print(tekstowo.get_lyrics())