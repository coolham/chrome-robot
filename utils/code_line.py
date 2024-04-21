import os
import sys

exclude_files = ['resources_rc.py',]

def count_lines(path):
    count = 0
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename in exclude_files:
                    continue
                if filename.endswith(".py"):
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                count += 1
    else:
        print("Invalid path:", path)
    return count

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()
    count = count_lines(path)
    print("The number of lines of Python code in %s is: %d" % (path, count))
    