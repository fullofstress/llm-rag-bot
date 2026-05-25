class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        words = text.split()

        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size

            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append(chunk_text)

            start += self.chunk_size - self.overlap

        return chunks