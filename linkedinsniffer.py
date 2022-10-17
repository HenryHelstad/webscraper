import requests
from bs4 import BeautifulSoup
searchURL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Network%20Security&location=United%20States&locationId=&geoId=103644278&f_TPR=&f_JT=F&f_E=2&position=1&pageNum=0&start="
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
        if cards == [] or i >= 100:
            return(links)
            
        for card in cards:
            links.append(card['href'])
        i += 25


def extractJobInfo(jobList):
    for i in jobList:
        page = requests.get(i)
        soup = BeautifulSoup(page.content, "html.parser")
        print(soup.find_all("div", {"class", "show-more-less-html__markup"}))
        

extractJobInfo(getjoblinks(searchURL)[:5])
