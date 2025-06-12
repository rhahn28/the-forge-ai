# test_sentiment_analyzer.py
import pytest
from src.sentiment_analyzer import analyze_sentiment


def test_positive_sentiment():
    assert analyze_sentiment('positive.txt') == (0.5, 0.6)


def test_negative_sentiment():
    assert analyze_sentiment('negative.txt') == (-0.5, 0.6)


def test_neutral_sentiment():
    assert analyze_sentiment('neutral.txt') == (0.0, 0.0)
