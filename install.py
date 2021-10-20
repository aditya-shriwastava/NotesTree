#!/usr/bin/python3
import os, sys

def main():
    home = os.path.expanduser("~")
    local_bin = home + "/.local/bin"
    bashrc = home + "/.bashrc"

    if not os.path.exists(local_bin):
        os.mkdir(local_bin)

    paths = os.environ['PATH'].split(":")
    if local_bin not in paths:
        bashrc_fd = open(bashrc, "a")
        bashrc_fd.write(f"export PATH=\"{local_bin}:$PATH\"\n")
        bashrc_fd.close()

    if("--skip" not in sys.argv):
        print("Installing Dependencies...")
        os.system("sudo pip3 install -r requirements.txt")

    os.system(f"cp ./src/notestree.py {local_bin}/notestree")
    print(f"NotesTree installed in {local_bin}")

if __name__ == "__main__":
    main()
