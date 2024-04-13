from .youtube import Youtube
from .lyrics_search import GetLyricsOutsideYT
from .lyrics_search2 import GetLyricsOutsideYT2

def process_song(link: str) -> str:
    """
    Processes a song given its YouTube link to retrieve its lyrics.

    Parameters:
        link (str): The YouTube link of the song.

    Returns:
        str: The lyrics of the song if found, or an appropriate error message.
    """
    try:
        yt = Youtube()
        yt_html = yt.get_data(link)
        if not yt_html:
            return "Failed to fetch YouTube data"

        title = yt.get_title()
        if not title:
            return "Failed to fetch title from YouTube"

        video_id = yt.get_video_id(link)
        if not video_id:
            return "Failed to extract video ID from YouTube link"

        print("Processing YouTube transcript...")
        youtube_transcript = yt.get_lyrics(video_id)
        if youtube_transcript:
            return youtube_transcript.lower()

        print("Trying external sources for lyrics...")
        try:
            external_lyrics = GetLyricsOutsideYT()
            lyrics = external_lyrics.search_lyrics_yahoo(title)
        except:
            pass
        if lyrics:
            print("Lyrics retrieved from external source - google")
            return lyrics.lower()
        else:
            external_lyrics = GetLyricsOutsideYT2()
            lyrics = external_lyrics.search_lyrics_yahoo(title)
            if lyrics:
                print("Lyrics retrieved from external source - yahoo")
                return lyrics.lower()
        return "Lyrics not found"
    except Exception as e:
        return "An error occurred while processing the song"
