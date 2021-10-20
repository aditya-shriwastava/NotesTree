#!/usr/bin/python3
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

import os, sys
import yaml
from send2trash import send2trash

def AddRoot(argv):
    def Usage():
        print("Usage:")
        print("notestree add-root <root_name>")

    if(len(argv) != 1):
        Usage()
        return False
    if( argv[0] == "--help"):
        Usage()
        return False

    root = argv[0]
    try:
        os.mkdir(root)
    except FileExistsError:
        print(f"{root} already exists!")
        return False

    os.mkdir(root + "/Appendices")

    fd_reference = open(root + "/.reference", "w")
    fd_reference.close()

    layout = Layout(root + "/.layout")
    layout.UpdateFile()

    Update([], os.getcwd() + "/" + root)
    return True

def AddChild(argv):
    def Usage():
        print("Usage:")
        print("notestree add-child <child_name>")

    if(len(argv) != 1):
        Usage()
        return False
    if( argv[0] == "--help"):
        Usage()
        return False

    if(AddRoot(argv)):
        AttachChild(argv)
        Update([])
        return True
    else:
        return False

def DeleteChild(argv):
    def Usage():
        print("Usage:")
        print("notestree delete-child <child_name>")

    if(len(argv) != 1):
        Usage()
        return False
    if( argv[0] == "--help"):
        Usage()
        return False
    
    child = argv[0]

    if(DetachChild(argv)):
        send2trash(child)
        Update([])
        return True
    else:
        return False

def RenameChild(argv):
    def Usage():
        print("Usage:")
        print("notestree rename-child <old_child_name> <new_child_name>")

    if(len(argv) != 2):
        Usage()
        return False
    if( argv[0] == "--help"):
        Usage()
        return False
    
    old_child_name = argv[0]
    new_child_name = argv[1]

    layout = Layout("./.layout")
    try:
        old_child_index = layout.order.index(old_child_name)
        layout.order[old_child_index] = new_child_name
        layout.UpdateFile()
        os.rename(old_child_name, new_child_name)
        Update([])
        Update([], os.getcwd() + "/" + new_child_name)
        return True
    except ValueError:
        print(f"{old_child_name} not found!")
        return False

def AttachChild(argv):
    def Usage():
        print("Usage:")
        print("notestree attach-child <child_name>")

    if(len(argv) != 1):
        Usage()
        return False
    if( argv[0] == "--help"):
        Usage()
        return False

    child = argv[0]
    if(os.path.exists(child)):
        layout = Layout("./.layout")
        layout.Add(child)
        layout.UpdateFile()
        Update([])
        return True
    else:
        print(f"{child} not found!")
        return False

def DetachChild(argv):
    def Usage():
        print("Usage:")
        print("notestree detach-child <child_name>")

    if(len(argv) != 1):
        Usage()
        return False
    if( argv[0] == "--help"):
        Usage()
        return False

    child = argv[0]

    layout = Layout("./.layout")
    if(layout.Del(child)):
        layout.UpdateFile()
        Update([])
        return True
    else:
        print(f"{child} not found!")
        return False

def Update(argv, path=os.getcwd()):
    def Usage():
        print("Usage:")
        print("notestree update")

    if(len(argv) > 0):
        Usage()
        return False

    index = Index(path)
    index.UpdateFile()

    appendices = os.listdir(path + "/Appendices")
    for appendix in appendices:
        RUpdate(argv, path + f"/Appendices/{appendix}")
    return True

def RUpdate(argv, path=os.getcwd()):
    def Usage():
        print("Usage:")
        print("notestree rupdate")

    if(len(argv) > 0):
        Usage()
        return False

    Update(argv, path)
    layout = Layout(path + "/.layout")
    for child in layout.order:
        RUpdate(argv, path + f"/{child}")
    return True

def InsertNotes(argv):
    def Usage():
        print("Usage:")
        print("notestree insert-notes <source-start-index> <source-end-index> <insert-position>")
        print("or")
        print("notestree insert-notes <source-start-index> <source-end-index>")
        print("or")
        print("notestree insert-notes <source-index>")
        print("or")
        print("notestree insert-notes -1")

    if(len(argv) not in [1, 2, 3]):
        Usage()
        return False
    if( argv[0] == "--help"):
        Usage()
        return False
    home = os.path.expanduser("~")
    source_path = f"{home}/Public"
    index = Index(os.getcwd())
    try:
        # i: <source-start-index>
        i = int(argv[0])
        if(i == -1):
            i = ParseSource(source_path)[0]
        # j: <source-end-index>
        if(len(argv) in [2,3]):
            j = int(argv[1])
        elif(len(argv) == 1):
            if(int(argv[0]) == -1):
                j = ParseSource(source_path)[-1]
            else:
                j = i
        # k: <insert-position-index>
        if len(argv) == 3:
            k = int(argv[2])
        else:
            if len(index.hand_written_notes) == 0:
                k = 1
            else:
                k = index.hand_written_notes[-1] + 1
    except ValueError:
        Usage()
        return False
    except IndexError:
        print("Index out of range!")
        return False

    source_list = ParseSource(source_path)
    i_index = source_list.index(i)
    j_index = source_list.index(j)
    target_list = source_list[i_index:j_index+1]
    if( len(target_list) != j-i+1 ):
        if(len(target_list) == 1):
            print("Failed: Image \"X_{i}.jpg\" not found!")
        else:
            print("Failed: All images \"X_{i}.jpg\" ... \"X_{j}.jpg\" not found!")
        return False

    # Shifting Images
    for image_index in range(len(index.hand_written_notes)-1, -1, -1):
        image_number = index.hand_written_notes[image_index]
        if(image_number>=k):
            os.system(f"mv ./{image_number}.jpg ./{image_number+j-i+1}.jpg")

    # Moving Images
    for r in range(j-i+1):
        os.system(f"mv {source_path}/X_{i+r}.jpg ./{k+r}.jpg")

    Update([])
    return True

def ParseSource(source_path):
    files = os.listdir(source_path)
    hand_written_notes = []
    for f in files:
        file_name = "".join(f.split(".")[0:-1])
        file_type = f.split(".")[-1]
        if(file_type == "jpg"):
            try:
                if(file_name[:2] == "X_"):
                    hand_written_notes.append(int(file_name[2:]))
            except ValueError:
                pass
    hand_written_notes.sort()
    return hand_written_notes

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

def main():
    fun_mapping = { "add-root":AddRoot,
                    "add-child":AddChild,
                    "delete-child":DeleteChild,
                    "rename-child":RenameChild,
                    "attach-child":AttachChild,
                    "detach-child":DetachChild,
                    "update":Update,
                    "rupdate":RUpdate,
                    "insert-notes":InsertNotes}
    def Usage():
        print("Usage:")
        funs = ", ".join(fun_mapping.keys())
        print(f"notebook.py [{funs}] <args>")

    if(len(sys.argv) < 2):
        Usage()
        return
    if(sys.argv[1] == "--help"):
        Usage()
        return

    try:
        fun_mapping[sys.argv[1]](sys.argv[2:])
    except KeyError:
        Usage()
        return

if __name__ == "__main__":
    main()
