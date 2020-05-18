from time import time
from unittest.runner import TextTestResult
from unittest import TextTestRunner, TestLoader


class TimedTextTestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        super(TimedTextTestResult, self).__init__(*args, **kwargs)
        self.clocks = dict()
        self.showAll = True

    def startTest(self, test):
        self.clocks[test] = time()
        super(TextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()

    def addSuccess(self, test):
        super(TextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("time spent: %.6fs" % (time() - self.clocks[test]))
        elif self.dots:
            self.stream.write(".")
            self.stream.flush()


if __name__ == '__main__':
    testsuite = TestLoader().discover('.')
    TextTestRunner(resultclass=TimedTextTestResult).run(testsuite)
