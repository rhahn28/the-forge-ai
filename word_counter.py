# Word Counter Program

# Function to count words in a file
def count_words_in_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    words = text.split()
    return len(words)

# Example usage
if __name__ == '__main__':
    file_path = 'sample.txt'  # replace with your file path
    word_count = count_words_in_file(file_path)
    print(f'The file contains {word_count} words.')
