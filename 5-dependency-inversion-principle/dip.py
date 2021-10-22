from abc import abstractmethod
from enum import Enum


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:
    def __init__(self, name):
        self.name = name


# Even though in Python an interface is not necessary to work,
# is good because other classes will know what to use to interact
# with the class.
class RelationshipBrowser:
    """
    Interface to avoid `Research` from being dependent on the
    concrete implementation `Relationships` and how info is stored.
    """
    @abstractmethod
    def find_all_children_of(self, name):
        pass


class Relationships(RelationshipBrowser):
    """Low-level as it manages how relationships are stored

    In this case, the relationships are stored in a list of tuples.
    """
    relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.PARENT, parent))
            
    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name == name and r[1] == Relationship.PARENT:
                yield r[2].name


class Research:
    """High-level: find John's children"""

    # def __init__(self, relationships):
    #     """Dependency on a low-level module directly
    #     bad because strongly dependent on e.g. storage type
    #     """
    #     relations = relationships.relations
    #     for r in relations:
    #         if r[0].name == 'John' and r[1] == Relationship.PARENT:
    #             print(f'John has a child called {r[2].name}.')
 
    def __init__(self, browser):
        for p in browser.find_all_children_of("John"):
            print(f'John has a child called {p}')


if __name__ == "__main__":

    # Parents and children.
    parent = Person('John')
    child1 = Person('Chris')
    child2 = Person('Matt')

    # Low-level modulel
    relationships = Relationships()
    relationships.add_parent_and_child(parent, child1)
    relationships.add_parent_and_child(parent, child2)

    # High-level module.
    Research(relationships)