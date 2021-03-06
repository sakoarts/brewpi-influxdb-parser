#!/usr/bin/env python

import argparse
import json
import os
import datetime
import time

#Reads json file, parses it to lineprotocol, and returns list of lineprotocol strings
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

#Reads list of lineprotocol strings and writes them to file
def writeListToFile(list, filename):
    newfile = filename + "_lineprotocol.txt"
    for x in list:
        x = str(x) + "\n"
        print(x),
        writeLineToFile(newfile, x)
    return newfile

#Inserts \ in front of specal characters to escape them form lineprotocol interpeter
def escapeChar(value):
    value = str(value)
    value = value.replace(" ", "\ ")
    value = value.replace(",", "\,")
    value = value.replace("=", "\=")
    return value

#Writes one line to a file
def writeLineToFile(newfile, line):
    with open(newfile, "ab") as text_file:
        text_file.write(line)

#Parses json datetime format to unixtimestamp, in case of none it retruns 0
def parseDatetime(s):
    value = datetime.datetime.strptime(s, "Date(%Y,%m,%d,%H,%M,%S)")
    return value

#Parses json number format to float, in case of none it retruns 0
def parseNumber(s):
    if "." not in str(s):
        s = str(s) + ".0"
    return s

#Parses json string format to lineprotocol compatible string, in case of none it retruns "null"
def parseString(s):
    value = '"' + escapeChar(s) + '"'
    return value

#Parses json value to lineprotocol compatible value
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

#Parses list representing a datapoint to a string compatible with lineprotocol
def parseFromList(list, cols):
    print(cols)
    datapoint = ""
    j = 0
    for v in list:
        id = cols[j]["id"]
        type = cols[j]["type"]
        j += 1
        if id == "Time":
            timestamp = parseDatetime(v["v"])
        else:
            try:
                value = parseValue(type, v["v"])
            except TypeError:
                continue
            datapoint += (str(id) + "=" + str(value) + str(","))
    return datapoint[:-1] + " " + str(time.mktime(timestamp.timetuple()))[:-2] + "000000000"

#Adds one line to influx database
def addLineToDB(db, line):
    os.system("curl -i -XPOST 'http://localhost:8086/write?db=" + db + "' --data-binary '" + line + "'")

#Adds file to influx database
def addFileToDB(db, file):
    os.system("curl -i -XPOST 'http://localhost:8086/write?db=" + db + "' --data-binary '@" + file + "'")

#Adds each line in list to influx database
def addListToDB(db, list):
    for x in list:
        addLineToDB(db, x)

#Main function
if __name__ == '__main__':
    # addListToDB('brewpi', readFromFile("mashtest-26-11-2015-2015-11-26.json"))
    writeListToFile(readFromFile("mashtest-26-11-2015-2015-11-26.json"), 'brewpi')
