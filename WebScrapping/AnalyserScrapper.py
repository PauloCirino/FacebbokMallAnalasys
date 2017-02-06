from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

import selenium.common.exceptions
import csv
import sys

baseURL = 'http://likealyzer.com/facebook/'

facebookIDs = open(sys.argv[1]).readlines()

driver = webdriver.PhantomJS()
driver.implicitly_wait(10)
driver.set_window_size(1280, 900)

resultsList = []

for facebookID in facebookIDs:
    facebookID = facebookID.strip()
    print 'Dado de ' + facebookID
    URL = baseURL + facebookID
    driver.get(URL)
    sleep(1)
    page = BeautifulSoup(driver.page_source, "html.parser")
    
    allPageInfos = page.find_all('div', class_='sidebarinfo')
    
    iter = 0
    while iter < 5 and len(allPageInfos) == 0:
        print 'iter = ' + iter
        driver.quit()
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(5)
        driver.set_window_size(1280, 900)
        iter = iter + 1
        driver.get(URL)
        sleep(5*iter)
        page = BeautifulSoup(driver.page_source, "html.parser")
    
    
    
    pageData = dict()
    pageData['ID'] = facebookID
    
    pageInfo = allPageInfos[0]
    pageData['PageName'] = pageInfo.find('span', class_='spanrub2').contents[1].strip().encode('utf-8')
    pageData['FacebookPage'] = pageInfo.find('span', class_='spanrub2').contents[2]['href'].strip().encode('utf-8')
    pageData['UserName'] = pageInfo.find(attrs={"name" : "slickbox_username"}).contents[1].strip().encode('utf-8')
    pageData['Website'] = pageInfo.find(attrs={"name" : "slickbox_webpage"}).contents[1].strip().encode('utf-8')
    pageData['MileStones'] = pageInfo.find(attrs={"name" : "slickbox_milestones"}).contents[1].strip().encode('utf-8')
    #pageData['PagesLiked'] = 
    
    pagePerformance = allPageInfos[1]
    pageData['Likes'] = pagePerformance.find(attrs={"name" : "slickbox_fans"}).contents[1].strip().encode('utf-8')
    pageData['LikesGrowth'] = pagePerformance.find(attrs={"name" : "slickbox_fans_growth"}).contents[1].strip().encode('utf-8')
    pageData['PTAT'] = pagePerformance.find(attrs={"name" : "slickbox_active"}).contents[1].strip().encode('utf-8')
    pageData['EngagementRate'] = pagePerformance.find(attrs={"name" : "slickbox_engagement"}).contents[1].strip().encode('utf-8')
    #pageData['Checkings'] = 
    
    pagePosts = allPageInfos[2]
    pageData['AvgPostsPerDay'] = pagePosts.find(attrs={"name" : "slickbox_postperday"}).contents[2].strip().encode('utf-8')
    pageData['AvgLikesCommentsSharesPerPosts'] = pagePosts.find(attrs={"name" : "slickbox_lcs"}).contents[1].strip().encode('utf-8')
    pageData['Timming'] = pagePosts.find(attrs={"name" : "slickbox_timing"}).contents[1].strip().encode('utf-8')
    pageData['LengthOfPosts'] = pagePosts.find(attrs={"name" : "slickbox_longpost"}).contents[1].strip().encode('utf-8')
    pageData['Hashtags'] = pagePosts.find(attrs={"name" : "slickbox_hashtag"}).contents[1].strip().encode('utf-8')
    
    resultsList.append(pageData)

print 'Saving Files'

with open("analyserData.csv", 'w') as csvfile:
    fieldNames = pageData.keys()
    writer = csv.DictWriter(csvfile, fieldnames = fieldNames)
    writer.writeheader()
    for data in resultsList:
        writer.writerow(data)

driver.quit()



