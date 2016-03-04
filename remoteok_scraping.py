from lxml import html
import requests
import sys
import codecs
import os
import os.path
import difflib
from difflib import Differ as Differ
from pprint import pprint
# -*- coding: utf-8 -*

page = requests.get("https://remoteok.io")
tree = html.fromstring(page.content)

positions = tree.xpath('//tr[@itemtype="http://schema.org/JobPosting"]/td[3]/a[1]/h2/text()')
companies = tree.xpath('//tr[@itemtype="http://schema.org/JobPosting"]/td[3]/a[2]/h3/text()')
applyForJobTooltips = tree.xpath('//tr[@itemtype="http://schema.org/JobPosting"]/td[8]/a/@title')
tags = tree.findall('.//td[@class="tags"]')
#tags1=tree.xpath('//tr[@itemtype="http://schema.org/JobPosting"]/td[5]/a[1]/div/h3/text()')
#tags2=tree.xpath('//tr[@itemtype="http://schema.org/JobPosting"]/td[5]/a[2]/div/h3/text()')
#tags3=tree.xpath('//tr[@itemtype="http://schema.org/JobPosting"]/td[5]/a[3]/div/h3/text()')

#print("tags1 length: {}, tags2 length: {} , tags3 length: {} ".format(len(tags1),len(tags2),len(tags3)))
length = len(positions)
print("length of the list is: ",length)
#print('positions: ',positions)
oldFile='remoteok_old.txt'
newFile='remoteok_new.txt'
with open(newFile, 'w') as f:
  for i,position in enumerate(positions):
    position=positions[i].strip()
    company=companies[i].strip()
    applyForJobTooltip=applyForJobTooltips[i].strip()
    tag1=" "
    tag2=" "
    tag3=" "
    if len(tags[i])>0:
      tag1=tags[i][0][0][0].text.replace("3>"," ").strip()
    if len(tags[i])>1:
      tag2=tags[i][1][0][0].text.replace("3>"," ").strip()
    if len(tags[i])>2:
      tag3=tags[i][2][0][0].text.replace("3>"," ").strip()	
    f.write('Position: {}\tCompany: {}\tDirected: {}\tTags: {},{},{}\n'.format(position,company,applyForJobTooltip,tag1,tag2,tag3))

with open(oldFile,'r') as f:
  oldData=f.readlines()
  
with open(newFile,'r') as f:
  newData=f.readlines()
	
#diff = difflib.ndiff(oldData, newData)
#sys.stdout.writelines(diff)
#pprint(diff)
d = Differ()
result=list(d.compare(newData,oldData))
#pprint(result)

resultFile='newResults.txt'
remainingContent='remainingResults.txt'
with open(resultFile,'w') as f:
  with open(remainingContent,'w') as g:
    for i in result:
      if i.startswith('-'):
        f.write(i)
      else:
        g.write(i)
if os.path.isfile(oldFile):
  os.remove(oldFile)
  
os.rename(newFile,oldFile)

#Read result file
with open(resultFile,'r') as f:
  resultData=f.readlines()
  for i in resultData:
    fields=i.split("\t")
    #print("fields:",fields)
    for j in fields:
      pairs=j.split(":")
      #print("pairs:",pairs)
      #print("looping in pairs")
      if pairs[0]=="Tags":
        tags=pairs[1].split(",")
        for k in tags:
          tagsplit=k.split()
          tag=''.join(tagsplit)
          #print("tag:{}".format(tag))
          if( tag=="qa" or tag.find("quality")!=-1 or tag=="testing" or tag=="test" ):
            print("An opening for QA as:"+i)   		  
	

