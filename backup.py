
import json
import datetime


dateFormat = "%Y_%m_%d_%H_%M_%S"


def write_note(filename, dateString):
    with open(filename, "w") as notefile:
        json.dump({"dateString" : dateString, "version": 1}, notefile)
        
def read_note_time(filename):
    date = datetime.datetime.strptime(read_note_date(filename), dateFormat)
    return date.timestamp()
    
def read_note_date(filename):
    with open(filename, "r") as notefile:
        return json.load(notefile)["dateString"]
