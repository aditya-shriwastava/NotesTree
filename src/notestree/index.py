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

import os
import yaml

class Index:
    def __init__(self, path):
        self.path = path
        self.ordered, self.order = self.ParseLayout()
        self.references = self.ParseReferences()
        self.appendices = self.ParseAppendices()
        self.markdown_notes = self.ParseMarkdownNotes()
        self.hand_written_notes = self.ParseHandWrittenNotes()
    def ParseLayout(self):
        fd = open(self.path + "/.layout", "r")
        layout = yaml.load(fd.read())
        ordered = layout["Ordered"]
        order = layout["Order"]
        fd.close()
        return ordered, order
    def ParseAppendices(self):
        files = os.listdir(self.path + "/Appendices")
        appendices = files
        appendices.sort()
        return appendices
    def ParseReferences(self):
        fd = open(self.path + "/.reference", "r")
        references = fd.read().splitlines()
        fd.close()
        return references
    def ParseMarkdownNotes(self):
        try:
            fd = open(self.path + "/Notes.md", "r")
            markdown_notes = fd.read()
            fd.close()
            return markdown_notes
        except FileNotFoundError:
            return ""
    def ParseHandWrittenNotes(self):
        files = os.listdir(self.path)
        hand_written_notes = []
        for f in files:
            file_name = "".join(f.split(".")[0:-1])
            file_type = f.split(".")[-1]
            if(file_type == "jpg"):
                try:
                    hand_written_notes.append(int(file_name))
                except ValueError:
                    pass
        hand_written_notes.sort()
        return hand_written_notes
    def UpdateFile(self):
        node_name = self.path.split("/")[-1]
        fd = open(self.path + "/index.md", "w")

        fd.write(f"# {node_name}\n")
        for i in range(len(self.order)):
            child_i = self.order[i]
            child_i_md = "%20".join(child_i.split(" "))
            if(self.ordered == True):
                fd.write(f"{i+1}. [{child_i}](./{child_i_md}/index.md)\n")
            else:
                fd.write(f"* [{child_i}](./{child_i_md}/index.md)\n")
    
        if self.appendices:
            fd.write("\n## Appendices\n")
            for appendix in self.appendices:
                appendix_md = "%20".join(appendix.split(" "))
                fd.write(f"* [{appendix}](./Appendices/{appendix_md}/index.md)\n")

        if self.references:
            fd.write("\n## References\n")
            for reference in self.references:
                fd.write(f"* {reference}\n")

        if self.markdown_notes:
            fd.write("\n")
            fd.write(self.markdown_notes)

        if self.hand_written_notes:
            fd.write("\n# HandWritten Notes\n")
            fd.write("<p align=\"center\">\n")
            for i in range(len(self.hand_written_notes)):
                hwn_i = self.hand_written_notes[i]
                fd.write(f"<img src=\"./{hwn_i}.jpg\" alt=\"Page {i+1}\"/>\n")
            fd.write("<p\>\n")
        fd.close()
