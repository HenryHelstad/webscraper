import sys
import requests
import re
from bs4 import BeautifulSoup
#searchURL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Soc%2Banalyst&location=United%20States&position=1&currentJobId=&start="

SEARCHMAX = 2000

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
        data = str(soup.find_all("div", {"class", "show-more-less-html__markup"}))
        a = search(data)
        if a >= 0:
            print(a)
            print(i)

with open(sys.argv[1]) as f:
    searches = [l.rstrip() for l in f]

print(searches)
for url in searches:
    extractJobInfo(getjoblinks(url))