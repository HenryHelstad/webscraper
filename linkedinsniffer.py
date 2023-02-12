import json
import sys
import requests
import re
from bs4 import BeautifulSoup
from termcolor import colored
#searchURL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Soc%2Banalyst&location=United%20States&position=1&currentJobId=&start="

SEARCHMAX = int(sys.argv[1])

regex = [(re.compile(r'(comp\stia|comptia)?\s(security\+|sec\+)', re.IGNORECASE),True), 
        (re.compile(r'IAT Level 2',re.IGNORECASE),True),
        (re.compile(r'soc\s1', re.IGNORECASE),True),
        (re.compile(r'\(?[1-9]\)?\+?\syear',re.IGNORECASE),False),
        (re.compile(r'CLEARANCE REQUIRED', re.IGNORECASE),False),
        (re.compile(r'Bachelor|degree', re.IGNORECASE),True)]

#"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Network%20Security&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_JT=F&f_E=2&position=1&pageNum=0&start="
#"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?currentJobId=3304792893&distance=25&f_E=3%2C4%2C6&geoId=90000070&keywords=soc%2Banalyst&start="


#URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?currentJobId=3304792893&distance=25&f_E=3%2C4%2C6&geoId=90000070&keywords=soc%2Banalyst&start=0&position=1&pageNum=6"

#takes in an api version of a linked in search url and returns 

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
        if a >= 1:
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

