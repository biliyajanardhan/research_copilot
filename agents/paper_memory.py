class PaperMemory:
    def __init__(self):
        self.saved = []

    def add(self, paper):
        if paper not in self.saved:
            self.saved.append(paper)

    def list(self):
        return self.saved
