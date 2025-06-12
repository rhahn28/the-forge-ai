import datetime

class ChatLogger:
    def __init__(self, filename):
        self.filename = filename

    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.filename, 'a') as file:
            file.write(f'{timestamp} - {message}\n')

if __name__ == '__main__':
    logger = ChatLogger('chat_log.txt')
    logger.log_message('This is a test message!')