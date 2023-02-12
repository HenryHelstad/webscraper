import json
import sys
import requests
import re
from bs4 import BeautifulSoup
from termcolor import colored
#searchURL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Soc%2Banalyst&location=United%20States&position=1&currentJobId=&start="

SEARCHMAX = int(sys.argv[1])


#change this regex to suit your search note: if a true regex is found it is given a point 
#if a false regex is found remove it from the running 
#It's currently set to 1 point minimum to even be returned 
regex = [(re.compile(r'(comp\stia|comptia)?\s(security\+|sec\+)', re.IGNORECASE),True), 
        (re.compile(r'IAT Level 2',re.IGNORECASE),True),
        (re.compile(r'soc\s1', re.IGNORECASE),True),
        (re.compile(r'\(?[1-9]\)?\+?\syear',re.IGNORECASE),False),
        (re.compile(r'CLEARANCE REQUIRED', re.IGNORECASE),False),
        (re.compile(r'Bachelor|degree', re.IGNORECASE),True),
        (re.compile(r'(one|two|three|four|five|six|seven|eight|nine|ten) plus years', re.IGNORECASE),False),
        (re.compile(r'Prior experiencing working in', re.IGNORECASE),False),
        (re.compile(r'Clearance Level', re.IGNORECASE),False),
        (re.compile(r'python', re.IGNORECASE),True),
         ]

listOfJobs = []

class job:
    title = ""
    date = None
    applicants_number = None
    score = 0
    link = ""

class jobEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

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

with open(sys.argv[2]) as links:
    searches = [l.rstrip() for l in links]

print(searches)
for url in searches:
    extractJobInfo(getjoblinks(url))
'''
for a in listOfJobs:
    print(a.score, a.title, a.date, a.applicants_number, a.link)
'''
with open( sys.argv[3], 'w+') as out:
     for a in listOfJobs:
         json.dump(a,out, indent=4, cls=jobEncoder)

