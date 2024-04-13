import torch
from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification
from typing import Dict, List
from langdetect import detect

class SentimentAnalyzer:
    """Class for analyzing the sentiment of text in different languages."""

    def __init__(self):
        """
        Initializes a SentimentAnalyzer object.

        Parameters:
            None

        Returns:
            None
        """
        self.nlp_en = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.nlp_pl = pipeline("sentiment-analysis", model="bardsai/twitter-sentiment-pl-base")

    def analyze(self, text: str) -> Dict:
        """
        Analyzes the sentiment of the given text.

        Parameters:
            text (str): The input text.

        Returns:
            Dict: A dictionary containing the sentiment analysis results.
        """
        lang = detect(text)
        if lang == 'en':
            return self._analyze_en(text)
        elif lang == 'pl':
            return self._analyze_pl(text)
        else:
            raise ValueError("Unsupported language")

    def _analyze_en(self, text: str) -> Dict:
        """
        Analyzes the sentiment of English text.

        Parameters:
            text (str): The input text.

        Returns:
            Dict: A dictionary containing the sentiment analysis results.
        """
        fragments = self._split_text_into_fragments(text)
        scores = self._get_sentiment_scores(fragments, self.nlp_en)
        return self._aggregate_scores(scores)

    def _analyze_pl(self, text: str) -> Dict:
        """
        Analyzes the sentiment of Polish text.

        Parameters:
            text (str): The input text.

        Returns:
            Dict: A dictionary containing the sentiment analysis results.
        """
        fragments = self._split_text_into_fragments(text)
        scores = self._get_sentiment_scores(fragments, self.nlp_pl)
        return self._aggregate_scores(scores)

    def _split_text_into_fragments(self, text: str) -> List[str]:
        """
        Splits the text into fragments of suitable length for sentiment analysis.

        Parameters:
            text (str): The input text.

        Returns:
            List[str]: A list of text fragments.
        """
        fragments = []
        current_fragment = ""
        fragment_length = 0

        for word in text.split(' '):
            if fragment_length + len(current_fragment) + len(word) > 256 or word.endswith('.'):
                fragments.append(current_fragment.strip())
                current_fragment = word
                fragment_length = len(word)
            else:
                current_fragment += ' ' + word
                fragment_length += len(word) + 1

        if current_fragment:
            fragments.append(current_fragment.strip())

        return fragments

    def _get_sentiment_scores(self, fragments, nlp) -> List[Dict]:
        """
        Gets sentiment scores for each text fragment.

        Parameters:
            fragments (List[str]): A list of text fragments.
            nlp: The sentiment analysis pipeline.

        Returns:
            List[Dict]: A list of dictionaries containing sentiment analysis scores.
        """
        scores = []
        for fragment in fragments:
            sentyment = nlp(fragment)
            scores.append({'label': sentyment[0]['label'], 'score': sentyment[0]['score']})
        return scores

    def _aggregate_scores(self, scores):
        """
        Aggregates sentiment scores to get an overall sentiment analysis result.

        Parameters:
            scores (List[Dict]): A list of dictionaries containing sentiment analysis scores.

        Returns:
            Dict: A dictionary containing the overall sentiment analysis result.
        """
        overall_result = {'label': 'neutral', 'score': 0}
        labels_count = {'positive': 0, 'negative': 0, 'neutral': 0}  

        for score in scores:
            label = score['label'].lower()  
            overall_result['score'] += score['score']
            labels_count[label] += 1
            print(score)
        dominant_label = max(labels_count, key=labels_count.get)
        if labels_count[dominant_label] / len(scores) < 0.5: 
            overall_result['label'] = 'negative'
        else:
            overall_result['label'] = dominant_label.upper() 
        overall_result['score'] /= len(scores)
        print("Końcowy wynik",overall_result)
        return overall_result