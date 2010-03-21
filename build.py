import os
import sys
import unittest

class Build:
    def clean(self):
        print "[clean]"
        for entry in os.listdir('.'):
            if os.path.isfile(entry):
                (root, ext) = os.path.splitext(entry)
                if ext == ".pyc":
                    # print("About to delete: " + entry)
                    os.remove(entry)
        return True

    def compile(self):
        self.clean()
        print "[compile]"
        for entry in os.listdir('.'):
            if os.path.isfile(entry):
                (root, ext) = os.path.splitext(entry)
                if ext == ".py":
                    (parent, fileName) = os.path.split(root)
                    module = __import__(fileName)
        return True

    def test(self):
        self.compile()
        print "[test]"
        fixtures = [ ]
        for entry in os.listdir('.'):
            if os.path.isfile(entry):
                (root, ext) = os.path.splitext(entry)
                if ext == ".py" and root.endswith("_tests"):
                    (parent, fileName) = os.path.split(root)
                    fixtures.append(fileName)

        result = True
        for moduleName in fixtures:
            print(moduleName)
            loader = unittest.TestLoader()
            module = __import__(moduleName)
            tests = loader.loadTestsFromModule(module)
            runner = unittest.TextTestRunner()
            result = result and runner.run(tests).wasSuccessful()
            print("")

        return result

if __name__ == "__main__":
    b = Build()
    result = True
    for arg in sys.argv:
        if hasattr(b, arg):
            method = getattr(b, arg)
            result = result and method()
    print("BUILD SUCCEEDED" if result else "BUILD FAILED")
    sys.exit(not result)
