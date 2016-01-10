import json
import datetime
import time

# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

#Reads json file, parses it to lineprotocol, and returns list of lineprotocol strings
def readFromFile(file):
    dataDict = {}
    with open(file) as json_file:
        data = json.load(json_file)
        i = 0
        for c in data["rows"]:
            datapoint = False
            dataDict.append(datapoint)
            i += 1
    return dataDict

#Main function
if __name__ == '__main__':
    # addListToDB('brewpi', readFromFile("mashtest-26-11-2015-2015-11-26.json"))
    print readFromFile("1_data_punt.json")
