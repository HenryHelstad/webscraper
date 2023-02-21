import sys
import requests
import re
from bs4 import BeautifulSoup
from termcolor import colored
import jsonpickle
#searchURL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Soc%2Banalyst&location=United%20States&position=1&currentJobId=&start="

SEARCHMAX = int(sys.argv[1])


#change this regex to suit your search note: if a true regex is found it is given a point 
#if a false regex is found remove it from the running 
#It's currently set to 1 point minimum to even be returned
regex = []
listOfJobs = []

class job:
    title = ""
    date = None
    applicants_number = None
    score = 0
    link = ""


def getjoblinks(jobSearchURL): 
    i = 0
    links = [] 
    while(True):

        page = requests.get(jobSearchURL + str(i))
        soup = BeautifulSoup(page.content, "html.parser")
        
        cards = soup.find_all("a", "base-card__full-link")
        if cards == [] or i >= SEARCHMAX:
            return(links)
            
        for card in cards:
            links.append(card['href'])
        i += 25

def search(content):
    i = 0
    for r in regex:
        t = r[0].search(content)
        #logic of scoring regex results
        if t != None and r[1]:  
            i+=1
        if t != None and not r[1]:
            i = -1
            break
    return i
    

def extractJobInfo(jobList):
    for i in jobList:
        page = requests.get(i)
        soup = BeautifulSoup(page.content, "html.parser")
        data = soup.find_all("div", {"class", "show-more-less-html__markup"})
        if data == []:
            print(colored("\nERROR:::::::::: empty page\n", 'red'), i)
            continue
        data = data[0].text
        title = soup.find_all("h1", {"class", "top-card-layout__title"})
        date = soup.find_all("span", {"class", "posted-time-ago__text topcard__flavor--metadata"})
        applicantNum = soup.find_all("span", {"num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"})
        a = search(data)
        if a >= 1: #change this if you want to change the minimum score to be in the output
            curr = job()
            curr.score = a
            curr.link = i
            if title != []:
                curr.title = title[0].text.strip()
            if date != []:
                curr.date = date[0].text.strip()
            if applicantNum != []:
                curr.applicants_number = applicantNum[0].text.strip()
            listOfJobs.append(curr)


        
        '''print(applicantNum)
        a = search(data)
        if a >= 0:
            print(a, title.strip("\n   "), date[0].text.strip("\n   "), i)
        elif a >= 0:
            print("****",a, title.strip("\n   "), i)'''


r = []
#reads in regex file
with open( sys.argv[3]) as regexFile:
    for i in [l.rstrip() for l in regexFile]:
        r.append(tuple(i.split('%')))

#compiles and interprets regex
for i in r:
    b = False
    reg = i[0]
    print(i)
    if i[1] == 'true':
        b = True
    if len(i) == 2:
        regex.append((re.compile(i[0],b)))
    elif len(i) == 3:
        regex.append((re.compile(i[0], re.IGNORECASE),b))

#reads in search links
with open(sys.argv[2]) as links:
    searches = [l.rstrip() for l in links]

#extracts data from urls and applys searches
for url in searches:
    print(url)
    extractJobInfo(getjoblinks(url))

pickled = jsonpickle.encode(listOfJobs)
fileWrite = open(sys.argv[4], "w")h


'''
print("\n",pickled)
fileWrite.write(pickled)
fileWrite.close()
fileRead = open("test.test", "r")
pickled = fileRead.read()
fileRead.close()
print("\n",pickled)
print("\n",jsonpickle.decode(pickled))
#dumps data to json file
with open( sys.argv[4], 'w+') as out:
     for a in listOfJobs:
         json.dump(a,out, indent=4, cls=jobEncoder)

'''
