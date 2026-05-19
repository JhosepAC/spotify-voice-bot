class EntityMemory:

    def __init__(self):

        self.entities = {}

    def remember(
        self,
        key,
        value
    ):
        """
        Store entity memory.
        """

        self.entities[key] = value

    def recall(
        self,
        key
    ):
        """
        Recall entity.
        """

        return self.entities.get(key)

    def clear(self):
        """
        Clear memory.
        """

        self.entities = {}