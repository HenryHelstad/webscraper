import jsonpickle
import sys

class job:
    title = ""
    date = None
    applicants_number = None
    score = 0
    link = ""

fileRead = open(sys.argv[1], "r")
pickled = fileRead.read()
fileRead.close()
listJobs = jsonpickle.decode(pickled)


