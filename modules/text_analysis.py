import re
from typing import List, Dict
from langdetect import detect

class TextAnalyzer:
    """Class for analyzing and processing text data."""
    def __init__(self) -> None:
        """
        Initializes a TextAnalyzer object.

        Parameters:
            None

        Returns:
            None
        """
        pass

    def del_emoji(self, lyrics: str) -> str:
        """
        Removes emojis from the given text.

        Parameters:
            lyrics (str): The input text.

        Returns:
            str: The text with emojis removed.
        """
        pattern = re.compile("["
                             u"\U0001F600-\U0001F64F"
                             u"\U0001F300-\U0001F5FF"
                             u"\U0001F680-\U0001F6FF"
                             u"\U0001F1E0-\U0001F1FF"
                             u"\U00002500-\U00002BEF"
                             u"\U00002702-\U000027B0"
                             u"\U000024C2-\U0001F251"
                             u"\U0001f926-\U0001f937"
                             u"\U00010000-\U0010FFFF"
                             u"\u2640-\u2642"
                             u"\u2600-\u2B55"
                             u"\u200d"
                             u"\u23cf"
                             u"\u23e9"
                             u"\u231a"
                             u"\ufe0f"
                             u"\u3030"
                             "]+",
                             flags=re.UNICODE)
        return pattern.sub(r'', lyrics)

    def wulgaryzmy(self, text: str) -> str:
        """
        Detects and counts swear words in the given text.

        Parameters:
            text (str): The input text.

        Returns:
            str: A message indicating the presence of swear words or suggesting further action.
        """
        profanity_pl_list = self._load_words("modules/wulgaryzmy_pl.txt")
        profanity_en_list = self._load_words("modules/wulgaryzmy_en.txt")

        profanity_pl = self._count_occurrences(text, profanity_pl_list)
        profanity_en = self._count_occurrences(text, profanity_en_list)
        profanity_counter = sum(profanity_en.values())
        language = self._language_detection(text)
        combined_results = {**profanity_pl, **profanity_en}
        if combined_results and language in ['pl','en']:
            print('Swear words in text: ' + ', '.join(
                [f"{word} ({count})" for word, count in combined_results.items()]))
            language = self._language_detection(text)
            if language == 'pl':
                return "Too many swear words"  
            elif language == 'en' and profanity_counter <= 5:
                return '6 swear words or less'
            elif language == 'en' and profanity_counter > 5:
                return "Too many swear words"
        elif language not in ['pl','en']:
            return "Language not supported"
        else:
            return "Lyrics go to NLP model"
        
    def _count_occurrences(self,text: str, words: List[str]) -> Dict[str, int]:
        """
        Counts the occurrences of words in the given text.

        Parameters:
            text (str): The input text.
            words (List[str]): A list of words to count occurrences of.

        Returns:
            Dict[str, int]: A dictionary mapping words to their occurrences in the text.
        """
        return {word: text.lower().count(word) for word in words if re.search(r'\b' + word + r'\b', text.lower())}

    def _load_words(self,filename: str) -> List[str]:
        """
        Loads a list of words from a file.

        Parameters:
            filename (str): The name of the file to load words from.

        Returns:
            List[str]: A list of words read from the file.
        """
        with open(filename, "r", encoding='utf-8') as ignore_file:
            return [line.strip().lower() for line in ignore_file.readlines()]

    def _language_detection(self,text: str) -> str:
        """
        Detects the language of the given text.

        Parameters:
            text (str): The input text.

        Returns:
            str: The detected language.
        """
        jezyk = detect(text)
        return jezyk