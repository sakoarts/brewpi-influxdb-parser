#!/usr/bin/env python

import argparse
import json
import os
import datetime
import time

def readFromFile(file):
    filename = file.split(".")[0]
    lineList = []

    with open(file) as json_file:
        data = json.load(json_file)

        i = 0
        for c in data["rows"]:

            datapoint = escapeChar(filename) + " " + parseFromList(c["c"], data["cols"])
            lineList.append(datapoint)
            i += 1
    return lineList

def writeListToFile(list, filename):
    newfile = filename + "_lineprotocol.txt"
    for x in list:
        x = str(x) + "\n"
        print(x),
        writeLineToFile(newfile, x)
    return newfile

def escapeChar(value):
    value = str(value)
    if " " in value:
        value = value.replace(" ", "\ ")
    if "," in value:
        value = value.replace(",", "\,")
    if "=" in value:
        value = value.replace("=", "\=")
    return value

def writeLineToFile(newfile, line):
    with open(newfile, "ab") as text_file:
        text_file.write(line)

def parseDatetime(s):
    if s is not "none":
        value = datetime.datetime.strptime(s, "Date(%Y,%m,%d,%H,%M,%S)")
    else:
        value = 0
    return value

def parseNumber(s):
    if s is not "none":
        value = s
        if "." not in str(value):
            value = str(value) + ".0"
    else:
        value = 0
    return value

def parseString(s):
    if s is not "none":
        value = '"' + escapeChar(s) + '"'
    else:
        value = '"' + 'null' + '"'
    return value

def parseValue(x, v):
    if x == 'number':
        value = parseNumber(v)
    elif x == 'string':
        value = parseString(v)
    elif x == 'datetime':
        value = parseDatetime(v)
    else:
        value = '"' + 'unknownType' + '"'
    return value

def parseFromList(list, cols):

    datapoint = ""
    j = 0
    for v in list:
        id = cols[j]["id"]
        type = cols[j]["type"]
        if id == "Time":
            timestamp = parseDatetime(v["v"])
        else:
            try:
                value = parseValue(type, v["v"])
            except TypeError:
                value = parseValue(type, "none")

            datapoint += (str(id) + "=" + str(value) + str(","))
        j += 1

    return(datapoint[:-1] + " " + str(time.mktime(timestamp.timetuple()))[:-2] + "000000000")

def addLineToDB(db, line):
    os.system("curl -i -XPOST 'http://localhost:8086/write?db=" + db + "' --data-binary '" + line + "'")

def addFileToDB(db, file):
    os.system("curl -i -XPOST 'http://localhost:8086/write?db=" + db + "' --data-binary '@" + file + "'")

def addListToDB(db, list):
    for x in list:
        addLineToDB(db, x)

if __name__ == '__main__':
    #readFromFile("mashtest-26-11-2015-2015-11-26.json")
    addFileToDB('brewpi', writeListToFile(readFromFile("mashtest-26-11-2015-2015-11-27.json"), "mashtest-26-11-2015-2015-11-27"))
