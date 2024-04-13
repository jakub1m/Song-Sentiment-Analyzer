import re
import requests
from bs4 import BeautifulSoup
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi

class Youtube:
    """Class for fetching and processing YouTube video data."""
    def __init__(self) -> None:
        """
        Initializes a Youtube object.
        """
        self.data = None

    def get_data(self, url: str) -> Optional[BeautifulSoup]:
        """
        Retrieves HTML data from a given URL and returns it as a BeautifulSoup object.

        Parameters:
            url (str): The URL of the YouTube video.

        Returns:
            Optional[BeautifulSoup]: A BeautifulSoup object containing the HTML data, or None if an error occurs.
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            self.data = soup
            return soup
        except Exception as e:
            return None

    def get_title(self) -> Optional[str]:
        """
        Extracts the title of the YouTube video and performs modifications.

        Parameters:
            None

        Returns:
            Optional[str]: The modified title string, or None if an error occurs.
        """
        try:
            title = self.data.title.string
            modified_title = re.sub(r"\[.*?\]|\(.*?\)| - YouTube|&amp;", "", title.split('|')[0])

            with open('modules/wulgaryzmy_pl.txt', 'r', encoding='utf-8') as polish_file:
                polish_blacklist = [line.strip() for line in polish_file]

            with open('modules/wulgaryzmy_en.txt', 'r', encoding='utf-8') as english_file:
                english_blacklist = [line.strip() for line in english_file]

            combined_blacklist = polish_blacklist + english_blacklist
            for word in combined_blacklist:
                if re.search(rf'\b{re.escape(word)}\b', title, re.IGNORECASE):
                    return None

            return modified_title
        except Exception as e:
            return None
            
    def get_video_id(self, link: str) -> Optional[str]:
        """
        Extracts the video ID from a YouTube video link.

        Parameters:
            link (str): The YouTube video link.

        Returns:
            Optional[str]: The extracted video ID, or None if not found.
        """
        try:
            video_id = re.search(r"v=([a-zA-Z0-9_-]{11})", link)
            return video_id.group(1) if video_id else None
        except Exception as e:
            return None

    def get_lyrics(self, video_id: str) -> Optional[str]:
        """
        Retrieves the transcript (lyrics) of a YouTube video in either Polish or English.

        Parameters:
            video_id (str): The ID of the YouTube video.

        Returns:
            Optional[str]: The transcript (lyrics) of the video, or None if an error occurs.
        """
        try:
            if video_id:
                transcript_pl = YouTubeTranscriptApi.get_transcript(video_id, languages=['pl'])
                if transcript_pl:
                    text_pl = ' '.join([fragment['text'] for fragment in transcript_pl])
                    return text_pl

                transcript_en = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                if transcript_en:
                    text_en = ' '.join([fragment['text'] for fragment in transcript_en])
                    return text_en

            return None
        except Exception as e:
            return None
