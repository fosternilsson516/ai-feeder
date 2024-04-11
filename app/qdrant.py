from qdrant_client import QdrantClient
import spacy

class Qdrant:

    def __init__(self):
        self.client = QdrantClient(":memory:")
        self.nlp = spacy.load("en_core_web_sm")

    def sentence_seg(self, text):
        
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return sentences

    def qdrant_input(self, sentences):
        for sentence in sentences:
            docs = f"{sentence}"
            self.client.add(
                collection_name="mem_collection",
                documents=docs,
            )

    def qdrant_query(self, query):   

        search_result = self.client.query(
            collection_name="mem_collection",
            query_text=query,
            limit=5
        )
        print(search_result)
        return search_result
   