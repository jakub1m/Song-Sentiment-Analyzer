# Song Sentiment Analysis

This project is designed to analyze the sentiment of song lyrics. It provides an API endpoint to analyze the sentiment of a song based on its lyrics. The sentiment analysis is performed using natural language processing (NLP) techniques.

## Features

- Analyzes the sentiment of song lyrics
- Supports multiple languages
- Utilizes external sources to retrieve lyrics if not available on YouTube

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/your_repository.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
## Usage
1.Start the Flask server:
```bash
python app.py
```
2. Send a POST request to the /sentiment endpoint with JSON data containing the URL of the YouTube video:
```json
{
    "URL": "https://www.youtube.com/watch?v=your_video_id"
}
```
3. Receive the sentiment analysis result as a JSON response
```json
{
    "sentiment": 0
}

```

## Authors
- Jakub Michalski
- Mateusz Snela

## License
This project is licensed under the [MIT License](LICENSE).





