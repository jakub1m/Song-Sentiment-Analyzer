from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Union
import logging

from modules.youtube import Youtube
from modules.text_analysis import TextAnalyzer
from modules.sentiment_analysis import SentimentAnalyzer
from modules.main import process_song

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='api_logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.getLogger('selenium').setLevel(logging.ERROR)

@app.route("/sentiment", methods=["POST"])
def analyze_sentiment() -> Dict[str, Union[float, str]]:
    """
    Analyzes the sentiment of a song based on its lyrics.

    Returns a sentiment score:
    - 0 for positive sentiment
    - 1 for neutral sentiment
    - 2 for negative sentiment

    If an error occurs during the process, returns an error message.

    Parameters:
        None

    Returns:
        Dict[str, Union[float, str]]: A dictionary containing the sentiment score or an error message.
    """
    try:
        data = request.json
        link = data.get("URL")
        logging.info(f"Received URL: {link}")

        youtube = Youtube()
        youtube.get_data(link)
        title = youtube.get_title()
        if not title:
            logging.info(f"Title include banned words")
            return jsonify({"sentiment": 2}), 200
        logging.info(f"Title extracted from YouTube: {title}")

        lyrics = process_song(link)
        if len(lyrics) <= 100:
            logging.info("Lyrics not extracted successfully")
            return jsonify({"sentiment": 1}), 200
        if lyrics:
            logging.info("Lyrics extracted successfully")

            cleaned_lyrics = TextAnalyzer().del_emoji(lyrics)

            vulgarity_check = TextAnalyzer().wulgaryzmy(cleaned_lyrics)
            logging.info(f"Vulgarity check result: {vulgarity_check}")

            if '6 swear words or less' in vulgarity_check or "Lyrics go to NLP model" in vulgarity_check:
                logging.info("Sentiment analysis initiated")
                sentiment_result = SentimentAnalyzer().analyze(cleaned_lyrics)
                logging.info(f"Sentiment result: {sentiment_result}")

                sentiment_score = None
                if sentiment_result["label"] == "POSITIVE":
                    sentiment_score = 0
                elif sentiment_result["label"] == "NEUTRAL":
                    sentiment_score = 1
                else:
                    sentiment_score = 2

                return jsonify({"sentiment": sentiment_score}), 200
            else:
                logging.info("Too many swear words detected, unable to analyze sentiment")
                return jsonify({"sentiment": 2}), 200
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"Error": str(e)}), 400

 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
