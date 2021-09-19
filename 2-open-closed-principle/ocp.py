from enum import Enum

# Note. This example uses the `Specification` enterprise pattern.

# We have colors and sizes properties for products.

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

# Wrong filter.

class ProductFilter:
    """
    Wrong because each filter criteria ads multiple methods to the class.

    This causes a state space explosion, example: filter by color, filter by
    size, filter by size and color, filter by size or color, etc.
    """
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color: yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size: yield p

    def filter_by_size_and_color(self, products, size, color):
        for p in products:
            if p.color == color and p.size == size:
                yield p

    # Etc...

# How to create a correct filter.

class Specification:
    """
    Base class.

    Class to determine if an item satifies a criteria.

    This class will be used for inheritance and be expanded.
    """
    def is_satisfied(self, item):
        pass

    # __and__ operator makes life easier than use AndSpecificationWorse.
    def __and__(self, other):
        return AndSpecification(self, other)


class Filter:
    """
    Base class.

    Class to get items that satisfy a criteria.

    This class will be used for inheritance and be expanded.
    """
    def filter(self, items, spec):
        """
        Args:
            items: items we want to filter.
            spec: specification. See `Specification` class.
        """
        pass


class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size


class NameSpecification(Specification):
    def __init__(self, name):
        self.name = name

    def is_satisfied(self, item):
        return item.name.lower() == self.name.lower()


class AndSpecificationWorse(Specification):
    """
    It's better to use __and__ (see the `Specification` class) to
    concatenate specifications using `&` than 
    passing them as arguments.

    Because it's easer to write:

        >>> large_blue_worse = large & ColorSpecification(Color.BLUE)

    than:

        >>> large_blue_worse = AndSpecificationWorse(large, ColorSpecification(Color.BLUE))

    For me, it looks clearer when 
    working with more than two specifications because
    this class seems to be able to work only with two specifications
    but it can be called more times to add more than two specifications.
    """

    def __init__(self, spec1, spec2):
        self.spec2 = spec2
        self.spec1 = spec1

    def is_satisfied(self, item):
        return self.spec1.is_satisfied(item) and \
               self.spec2.is_satisfied(item)


class AndSpecification(Specification):
    """
    This is a combinator to work with multiple Specifications.
    """
    def __init__(self, *args):
        """
        Args:
            args: the specifications.
        """
        self.args = args

    def is_satisfied(self, item):
        """
        Checks if all specifications are satisfied for an item.
        """
        return all(map(
            lambda spec: spec.is_satisfied(item), self.args))


class BetterFilter(Filter):
    """
    This class makes some assumptions about the type of elements to work with,
    for example, that we can use a for loop to iterate them.

    If we need another type of filter, instead of modify this class,
    we can create another class that inherits from `Filter` and expands the filter
    funcionality.
    """
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


if __name__ == "__main__":

    apple = Product('Apple', Color.GREEN, Size.SMALL)
    tree = Product('Tree', Color.GREEN, Size.LARGE)
    house = Product('House', Color.BLUE, Size.LARGE)
    
    products = [apple, tree, house]

    # Wrong filter.
    
    pf = ProductFilter()
    print('Green products (old):')
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f' - {p.name} is green')
    
    # Correct filter.

    bf = BetterFilter()
    
    print('Green products (new):')
    green = ColorSpecification(Color.GREEN)
    for p in bf.filter(products, green):
        print(f' - {p.name} is green')
    
    print('Large products:')
    large = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large):
        print(f' - {p.name} is large')
    
    print('Large blue items:')
    large_blue = large & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_blue):
        print(f' - {p.name} is large and blue')
    large_blue_worse = AndSpecificationWorse(large, ColorSpecification(Color.BLUE))
    for p in bf.filter(products, large_blue_worse):
        print(f' - {p.name} is large and blue (using worse Specification)')

    print('Large blue house items:')
    # We cannot use `and` we have to use `&`.
    large_blue_house = large_blue & NameSpecification("house")
    for p in bf.filter(products, large_blue):
        print(f' - {p.name} is large and blue house')
    # We can use more than two specifications with the worse class.
    # You can comment the `__and__` of the `Specification` class to be sure.
    large_blue_house_worse = AndSpecificationWorse(large_blue_worse, NameSpecification("house"))
    for p in bf.filter(products, large_blue_house_worse):
        print(f' - {p.name} is large and blue house (using worse Specification)')
