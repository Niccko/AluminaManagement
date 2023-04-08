class Event:
    def __init__(self) -> None:
        self.subscribers = []

    def invoke(self, **kwargs):
        for sub in self.subscribers:
            sub(**kwargs)

    def subscribe(self, handler):
        self.subscribers.append(handler)