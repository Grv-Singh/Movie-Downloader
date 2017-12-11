#Software Developed by the developer to Download Movies released in India from fmovies.ac
import os
import sys
os.environ["LANG"] = "en_US.UTF-8"
from bs4 import BeautifulSoup
import bs4
import re
from operator import itemgetter
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 

print("\t\t\tMovies released in India: (latest first)\n\n\t Please wait until list updates\n")

browser = webdriver.Chrome("chromedriver.exe")

index=1

mov_list = []
down_link = []

print("\nAvailable titles: (input 'exit' to EXIT)\n")

for pg_count in range(1,9):
        browser.get('http://www.fmovies.ac/country/india.html?p='+str(pg_count))
        soup = BeautifulSoup(browser.page_source,"html5lib")
        names = soup.find_all("a", class_="ml-mask jt")
        for name in names:
             mov_list.append(name.get("oldtitle"))
             print(str(index)+". "+name.get("oldtitle")+"\n")
             index=index+1

while 1:
        inp = input("\n\tList Updated.\n\nWhich Movie to download? (Input Number)\n")
        if inp != 'exit':
                num = int(inp)
                print("\n\t\""+str(mov_list[(num-1)])+"\" Selected\n\nWorking on it..\n")
                browser.get('http://www.fmovies.ac/country/india.html?p='+str(int(num/32)+1))
                soup = BeautifulSoup(browser.page_source,"html5lib")
                btn = soup.find("a",attrs={"class":"ml-mask jt", "oldtitle":str(mov_list[(num-1)])})
                btn_href = btn.get("href")
                browser.get(str(btn_href))
                soupi = BeautifulSoup(browser.page_source,"html5lib")
                frames = soupi.find_all("iframe", attrs={"height":500})
                for frame in frames:
                        mov_link = "https://www.9xbuddy.com/process?url=https%3A"+frame.get("src").replace("/","%2F")
                        browser.get(mov_link)
                        try:
                                WebDriverWait(browser, 10).until(lambda x: 'Completed' in browser.title)
                        except TimeoutException as e:
                                pass
                        soupii = BeautifulSoup(browser.page_source,"lxml")
                        listset = soupii("li","link-download")
                        print("\nFetching movie..\n")
                        for list in listset:
                                down_link += [a['href'] for a in list.findAll('a',{'href':True})]
                        browser.get(down_link[0])
                        print("\nDownload in process..\n")
                        ans = input("\nAny other?(y/n)")
                        if ans == 'y':
                                continue
                        else:
                                print("\nExiting..\n")
                                sys.exit()
        else:
                print("\nExiting..\n")
                sys.exit()
