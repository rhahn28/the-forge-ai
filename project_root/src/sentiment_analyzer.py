# sentiment_analyzer.py
import sys
from textblob import TextBlob


def analyze_sentiment(file_path: str) -> tuple:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            if not content.strip():
                raise ValueError('File is empty')

            blob = TextBlob(content)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            return polarity, subjectivity
    except FileNotFoundError:
        print(f'Error: {file_path} not found.')
    except ValueError as e:
        print(f'Error: {str(e)}')
    except Exception as e:
        print(f'Unexpected error: {str(e)}')


def main():
    if len(sys.argv) != 2:
        print('Usage: python sentiment_analyzer.py <file_path>')
        sys.exit(1)
    file_path = sys.argv[1]
    result = analyze_sentiment(file_path)
    if result:
        polarity, subjectivity = result
        print(f'File: {file_path}')
        print(f'Sentiment Polarity: {polarity}')
        print(f'Sentiment Subjectivity: {subjectivity}')


if __name__ == '__main__':
    main()
