class ShoppingList:
    """
    This class has only one responsability: manage the entries.
    The class does more than one thing: store entries and delete them.
    Despite the class does mutiple things, it has only one responsability.
    """
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]
        self.count -= 1

    def __str__(self):
        return "\n".join(self.entries)


class ShoppingListWrong:
    """
    This class has two responsabilities: manage information and export it.
    Solution: create a class for persistence
    """
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]
        self.count -= 1

    def __str__(self):
        return "\n".join(self.entries)

    # Break SRP.
    def save(self, filename):
        file = open(filename, "w")
        file.write(str(self))
        file.close()



class PersistenceManager:
    """
    This class can grow with checks about file permissions, etc.
    without making the ShoppingList class bigger and bigger.
    """
    @staticmethod
    def save_to_file(journal, filename):
        file = open(filename, "w")
        file.write(str(journal))
        file.close()


if __name__ == "__main__":
    shopping_list = ShoppingList()
    shopping_list.add_entry("bread")
    shopping_list.add_entry("phone")
    print(f"Shopping List entries:\n{shopping_list}\n")

    p = PersistenceManager()
    file = "/tmp/shopping-list.txt"
    p.save_to_file(shopping_list, file)
    # Verify.
    with open(file) as fh:
        print(fh.read())