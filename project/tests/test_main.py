# test_main.py
import unittest
from unittest.mock import patch
from src import main

class TestEmailDrafting(unittest.TestCase):
    @patch('src.main.openai_client')
    @patch('src.main.build')
    def test_fetch_and_draft_emails(self, mock_build, mock_openai_client):
        # Setup mocks
        mock_service = mock_build.return_value
        mock_messages_list = mock_service.users().messages().list.return_value
        mock_messages_list.execute.return_value = {'messages': [{'id': 'test-id', 'threadId': 'test-thread-id'}]}
        mock_get = mock_service.users().messages().get.return_value
        mock_get.execute.return_value = {'snippet': 'Test email body', 'payload': {'headers': [{'name': 'From', 'value': 'test@example.com'}, {'name': 'Subject', 'value': 'Test Subject'}]}}
        mock_openai_client.chat.completions.create.return_value = {'choices': [{'message': {'content': 'Test response'}}]}

        # Call the function
        main.fetch_and_draft_emails()

        # Assertions
        mock_openai_client.chat.completions.create.assert_called_once()
        mock_service.users().drafts().create.assert_called_once()

if __name__ == '__main__':
    unittest.main()
