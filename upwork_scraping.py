import lxml
from lxml import html
import requests
import time
session_request=requests.session()
login_url="https://www.upwork.com/Login"
result=session_request.get(login_url)
tree=html.fromstring(result.text)
authenticity_token=list(set(tree.xpath("//input[@name='login[_token]']/@value")))[0]

payload = {
  "login[username]":"shrutiawake@gmail.com",
  "login[password]":"creativity15",
  "login[_token]":authenticity_token
}
#print("payload:",payload)
result=session_request.post(
  login_url,
  data=payload,
  headers=dict(referer=login_url)
)
lastJobArticlesArray={}
while(1):
  #scrape content from QA and Testing section
  url='https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/?sc=qa-testing,scripts-utilities&sort=create_time%2Bdesc'
  result=session_request.get(
    url,
    headers=dict(referrer=url)
  )
  tree=html.fromstring(result.content)
  jobArticles=tree.xpath('//article[@itemtype="https://schema.org/JobPosting"]/div[2]/div[1]/header/h2/a/text()')
  c=0
  changeTill=0
  if(len(lastJobArticlesArray)==0):
    print("First loop")
    #print("jobArticles:")
    #print(jobArticles)
  elif(len(lastJobArticlesArray)!=0):
    #print("Not the first loop")
    for jobArticle in jobArticles:
      #print("jobArticle {}. : {}".format(c+1,jobArticle))
      if(c==0 and lastJobArticlesArray[c]==jobArticles[c]):
        print("no change")
        break
      elif(lastJobArticlesArray[0]==jobArticles[c]):
        print("change detected")
        changeTill=c
        break
      c=c+1
    c=0
    while(c<changeTill):
      print("new Job Article: {}".format(jobArticles[c]))
      c=c+1
  lastJobArticlesArray=jobArticles
  #print("lastJobArticlesArray:")
  #print(lastJobArticlesArray)  
  time.sleep(300)

