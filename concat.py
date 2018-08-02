import os

field = []
def concat():
    with open(os.path.join("/Users/gimminsang/work/practice/data", "temp.log"), "r") as fp:
        f = open("/Users/gimminsang/work/practice/data/field.log","w")
        while(True):
            line = fp.readline()
            if not line: break
            line2 = line.split("?")
            line3 = line2[1].split("&")
            exist = False
            for l in line3:
                temp = l.split("=")
                exist = False
                for t in field:
                    if t == temp[0]:
                        exist = True
                        break
                if exist == False:
                    field.append(temp[0])
        for m in field:
            f.write(m+"\n")


                        
def getValue():
    with open(os.path.join("/Users/gimminsang/work/practice/data", "temp.log"), "r") as fp:
        f = open("/Users/gimminsang/work/practice/data/result.log","w")
        dic = {}
        for i in field:
            dic[i] = ""
        while(True):
            line = fp.readline()
            if not line: break
            line2 = line.split("?")
            line3 = line2[1].split("&")
            for i in line3:
                line4 = i.split("=")
                prop = line4[0]
                value = line4[1]
                if ")" in value:
                    value = value.split(")")
                    value = value[0]
                dic[prop] = value
                f.write(prop+":")
                f.write(value+"\n")
