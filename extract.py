import os

def extract():
    with open(os.path.join("/Users/gimminsang/work/practice/data", "skp.log"), "r") as fp:
        f = open("/Users/gimminsang/work/practice/data/temp.log","w")
        while(True):
            line = fp.readline()
            if not line: break
            if "172.19.106.242" in line:
                f.write(line)
