"""
Copyright 2010 Olivier Dagenais

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
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
            result = runner.run(tests).wasSuccessful() and result
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
