from BeautifulSoup import BeautifulSoup
import os,sys,string,re
import subprocess

import urllib2
URLPREFIX="http://www.youtube.com/watch?feature=player_embedded&v="
'''
kangxiurl=urllib2.urlopen("http://www.maplestage.com/show/%E5%BA%B7%E7%86%99%E4%BE%86%E4%BA%86/")
kangxicontent=kangxiurl.read()
kangxisoup = BeautifulSoup(kangxicontent)
episodes= kangxisoup.findAll(attrs={"class":"shows"})
if len(episodes)!=1:
    print "Error! Found multiple tags"
    sys.exit(1)
print len(episodes[0].contents)
print episodes[0].contents[0]
print episodes[0].contents[1]
print episodes[0].contents[800]
#episodessoup = BeautifulSoup(episodes[0].contents)
#episodes=episodesoup.findAll(attrs={"class":"show"})
#print len(episodes)

'''
url = urllib2.urlopen("http://www.maplesi.com/node/81949/%E5%BA%B7%E7%86%99%E4%BE%86%E4%BA%86-20130619-%E9%BB%83%E7%BE%A9%E9%81%94-%E9%84%A7%E7%A6%8F%E5%A6%82-%E4%B8%81%E5%99%B9-%E5%AE%B6%E5%AE%B6-mp%E9%AD%94%E5%B9%BB%E5%8A%9B%E9%87%8F-%E9%BB%83%E5%9C%8B%E5%80%AB-%E9%82%A3%E4%BA%9B%E5%B9%B4%E6%88%91%E5%80%91%E6%B5%81%E8%A1%8C%E7%9A%84%E7%B6%93%E5%85%B8%E6%AD%8C%E6%9B%B2/")

content = url.read()

soup = BeautifulSoup(content)

links = soup.findAll(attrs={"class":"video_ids"})

#for link in links:
for i in range(0,len(links)):
    link = links[i]
    print "Found video_ids set %d:"%(i+1)
    ids=link.contents[0]
    #print ids
    ids=string.split(ids,",")
    for j in range(0,len(ids)):
        print "    Part %d: %s"%(j+1,ids[j])
#ids=['a','b','c','d','e']
#if 1:
    print "Which parts would u like to download?"
    print "Starting input, e.g. 1-5(inclusive) or 2,3,4?"
    parts=string.strip(raw_input())
    print parts
    pstr1="[1-9]\d*-[1-9]\d*"
    pattern1=re.compile(pstr1)
    pstr2="[1-9]\d*(,[1-9]\d*)*[,]*"
    pattern2=re.compile(pstr2)
    res=pattern1.search(parts)
    urlstr=""
    if res!= None:
        parts_index=string.split(res.group(0),'-')
        ibegin=int(parts_index[0])
        iend=int(parts_index[1])
        if ibegin<1 :
            print "Begin from Part 1 since %d is negative"%ibegin
            ibegin = 1

        if iend > len(ids):
            print "End at Part %d since %d is too big"%(len(ids),iend)
            iend = len(ids)
        urlstr="%s%s"%(URLPREFIX,ids[ibegin-1])
        for i in range(ibegin,iend):
            urlstr=urlstr+" %s%s"%(URLPREFIX,ids[i])
    else:
        res=pattern2.search(parts)
        if res!= None:
            strres=res.group(0)
            if strres[len(strres)-1]==',':
                strres=strres[0:len(strres)-1]
            parts_index=string.split(strres,',')
            print parts_index
            added=[]
            for one_index in parts_index:

                one_index=int(one_index)
                if one_index <1 or one_index > len(ids):
                    print "Part %d ignored since it is invalid"%one_index
                else:
                    if not one_index in added:
                        urlstr=urlstr+" %s%s"%(URLPREFIX,ids[one_index-1])
                        added.append(one_index)
                    else:
                        print "Part %d ignored since it is repetive"%one_index
                    urlstr=string.lstrip(urlstr)
    print urlstr
    cmd=['.\\youtube-dl.exe']+string.split(urlstr)
    print cmd
    subprocess.call(cmd)






