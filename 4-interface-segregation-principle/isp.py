from abc import abstractmethod


class Machine:
    def print(self, document):
        raise NotImplementedError()

    def fax(self, document):
        raise NotImplementedError()

    def scan(self, document):
        raise NotImplementedError()


# If we create a multifunction class, it can use the previous interface.
class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass


# But, other classes do not need all the previous interface methods.
class OldFashionedPrinter(Machine):
    def print(self, document):
        # ok - print stuff
        print("Start printing...")

    def fax(self, document):
        pass  # No error but do-nothing

    def scan(self, document):
        """Not supported!"""
        raise NotImplementedError("Printer cannot scan!")


# It's better to create a class for each action.
class Printer:
    @abstractmethod
    def print(self, document):
        pass


class Scanner:
    @abstractmethod
    def scan(self, document):
        pass


# Same for Fax, etc.


# Now, each derived class can inherit from the required interfaces,
# implementing only the methods to use.
class MyPrinter(Printer):
    def print(self, document):
        print(document)


class Photocopier(Printer, Scanner):
    def print(self, document):
        print(document)

    def scan(self, document):
        pass  # something meaningful


# If you need an interface that is a printer and a scanner
# you can create it using the previous classes.
class MultiFunctionDevice(Printer, Scanner):  # , Fax, etc
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass


class MultiFunctionMachine(MultiFunctionDevice):
    def __init__(self, printer, scanner):
        self.printer = printer
        self.scanner = scanner

    def print(self, document):
        self.printer.print(document)

    def scan(self, document):
        self.scanner.scan(document)


if __name__ == "__main__":
    printer = OldFashionedPrinter()
    printer.print(123)  # It works fine.
    printer.fax(123)  # It does not raise errors but does nothing.
    printer.scan(123)  # Error, because the class does not implement the scan method.
