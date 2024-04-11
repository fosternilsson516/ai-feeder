class DocumentStorage:
    def __init__(self):
        # Initialize a string to store concatenated document texts
        self.cumulative_text = ""

    def store_doc(self, text):
        # Concatenate the new text with the existing cumulative text
        # You might want to add a space or newline for separation
        self.cumulative_text += "\n" + text

    def get_all_text(self):
        # Retrieve the cumulative text containing all stored document texts
        return self.cumulative_text

    def split_text_into_word_chunks(self, document, chunk_size=250):
        # Split the text into words
        words = document.split()
        
        # Split words into chunks of `chunk_size`
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        
        return chunks      