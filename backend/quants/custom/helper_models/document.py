

class DocumentHelper:
    """
    Helper model to handle post-chain document processing.
    """

    @staticmethod
    def parse_snippets(sources, raw_snippets):
        """
        Convert and filter a list of LangChain documents into a list of Snippets.

        Args:
            sources: a string of the UUIDs of the source documents separated by commas
            raw_snippets: a list of LangChain Documents containing the extracts from source
                documents used for answering the question
        Returns:
            a list of Snippets that are only from the source documents with content from
            the Documents in raw_snippets
        """
        # parse the sources to a list of uuids
        src_uuids = set(map(lambda x: x.strip(), sources.split(',')))
        # only include the snippet if it is contained in the list of sources to prevent
        # hallucination from sources that don't exist
        snippets = [Snippet(doc) for doc in raw_snippets if str(Snippet(doc).uuid) in src_uuids]

        return snippets
        
class Snippet:
    """
    Simple wrapper for Langchain's Document class.
    """

    def __init__(self, document):
        self.uuid = document.metadata.get('source')
        self.content = document.page_content
    
    def __str__(self) -> str:
        return f'Snippet(id: {self.uuid}, content: "{self.content}")'
    