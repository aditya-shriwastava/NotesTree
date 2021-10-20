"""
MIT License

Copyright (c) 2021 aditya-shriwastava

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import yaml

class Layout:
    def __init__(self, file_path):
        try:
            fd = open(file_path, "r")
            layout = yaml.load(fd.read())
            self.ordered = layout["Ordered"]
            self.order = layout["Order"]
            fd.close()
        except FileNotFoundError:
            self.ordered = True
            self.order = []
        self.file_path = file_path
    def Add(self, child):
        if child in self.order:
            return False
        else:
            self.order.append(child)
            return True
    def Del(self, child):
        if child in self.order:
            self.order.remove(child)
            return True
        else:
            return False
    def UpdateFile(self):
        fd = open(self.file_path, "w")
        layout = {"Ordered": self.ordered, "Order": self.order}
        fd.write( yaml.dump(layout, default_flow_style=False) )

        fd.close()
