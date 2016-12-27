import re
import requests
from bs4 import BeautifulSoup
import time


def justtext(html):
    okay = re.compile('<.*?>')
    text = re.sub(okay, '', html)
    return text


def scrape(skills, location):
    s = skills
    s = s.replace(' ', '-')
    ss = location
    url = "http://www.shine.com/job-search/simple/" + s + "/" + ss
    # print(url)
    r = requests.request("GET", url)
    myjobs = []
    soup = BeautifulSoup(r.text, "lxml")
    all_jobs = soup.find_all("div", {"class": "search_listing"}, {"itemtype": "http://schema.org/JobPosting"})
    # print(all_jobs)
    if (len(all_jobs) == 0):
        if len(re.findall(r'Didyoumean.*data-keyword="(.*)\">.*<\/a>', r.text)) > 0:
            didyoumean = re.findall(r'Didyoumean.*data-keyword="(.*)\">.*<\/a>', r.text)[0]
            return ("Did you mean:" + str(didyoumean))
        else:
            return ("We couldnt find anything for your query")

    else:
        for jobs in all_jobs:
            temp = []
            title = re.findall(r'data-jobtitle="(.*)" data-jobtype', str(jobs))[0]
            # soup1 = BeautifulSoup(okay[0], "lxml")
            company = re.findall(r'data-jobcompany="(.*)" data-jobid', str(jobs))[0]
            link = re.findall(r'href="(.*)" target', str(jobs))[0]
            temp.append(title)
            temp.append(company)
            temp.append(link)
            myjobs.append(temp)
    return myjobs


def scrapepage(link):
    if link[0] == '/':
        link = "http://www.shine.com" + link
    r = requests.request("GET", link)
    soup = BeautifulSoup(r.text, "lxml")
    title = re.findall(r'<h1 itemprop="title">(.*)</h1>', r.text)[0]
    soup4 = BeautifulSoup(str(soup.find("span", {"itemprop": "experienceRequirements"})), "lxml")
    exp = soup4.get_text()
    soup2 = BeautifulSoup(str(soup.find("span", {"itemprop": "description"})), "lxml")
    job_description = soup2.get_text()
    soup3 = BeautifulSoup(str(soup.find("div", {"class": "ropen cls_rect_detail_div"})), "lxml")
    rec_info = soup3.get_text()
    print(title)
    print("Experience Required\n" + exp)
    print("Job Description\n" + job_description)
    print("Contact Information:\n" + rec_info)


if __name__ == '__main__':
    skills = input("Enter your skills seperated by space\n").replace(" ", "-")
    # print()
    location = input("Enter the location:")
    print("Choose from the following\n")
    scrapeData = scrape(skills, location)
    time.sleep(3)
    count = 1
    for items in scrapeData:
        print(str(count) + ". " + items[0] + " -" + items[1])
        count += 1
    number = int(input("\nEnter your choice:"))
    # print(scrapeData[(number-1)])
    scrapepage(scrapeData[number - 1][2])
