#coding=utf-8
from urllib import urlencode
from time import sleep
from random import randint
import sqlite3,cookielib,time,re,os
import urllib2,shutil

add_num = 0
class RenrenRobot:
    def __init__(self):
        print '*********************************'
        print '*Hi,This is Hark\'s Robot For RR*'
        print '*********************************'
        print 'Contact With me: my.cheng@msn.com'
        print 'Version: 0.1'
        print ''
        self.allCount = 0
        self.newCount = 0
        #Create Dir
        self.strSpiderBasePath = r'd:\leehark_spider'
        
        if os.path.exists(self.strSpiderBasePath) == False:
            os.mkdir(self.strSpiderBasePath)
        
    def Download(self,id):
        # Fetching Your Friend's Recent Updated Pictures' URL whose id is '@param = id'
        self.strBaseFilePath = (r'd:\leehark_spider\id_%s' % id)
        if os.path.exists(self.strBaseFilePath) == False:
            os.mkdir(self.strBaseFilePath)
        strFriendURL = ('http://photo.renren.com/photo/%s/album/relatives' % id)
        res = urllib2.urlopen(strFriendURL)
        print res.geturl()
        print res.getcode()
        print res.info()
        str = res.read()
        
        strPattern = r'<li>.<a href="(http://photo.renren.com/photo/[^<>]*?)" class="picture">'
        r = re.findall(strPattern,str,re.S|re.I)
        if r == None:
            return
        fout = open('d:\\spider\\tmp.txt','wb')
        for item in r:
            photoURL = item
            print 'Picture\'s URL: ' , photoURL
            ret = urllib2.urlopen(photoURL)
            strPicURLContent = ret.read()
            strPicPattern = r'<img id="photo" src="(http://.*?)" title=".*?" style=".*?">'
            rPic = re.findall(strPicPattern,strPicURLContent,re.S|re.I)
            for subItem in rPic:
                self.allCount+=1
                # Construct FilePath
                strItem = subItem.replace('/','_')
                strItem = strItem.replace(':','_')
                strItem = strItem.replace('&','_')
                strItem = strItem.replace('\\','_')
                strFilePath = self.strBaseFilePath+'\\'+strItem
                
                if os.path.exists(strFilePath):
                    # Hit the Old one
                    print 'Fetched Already : ',subItem
                    continue

                # This is New Image,Fetch it
                self.newCount+=1
                print 'Fetching New Image :'
                print subItem,' --> ',strFilePath
                ret = urllib2.urlopen(subItem)

                # Get Image Size
                headers = ret.info().headers
                length = 0
                for header in headers:
                    if header.find('Length') != -1:
                        length = header.split(':')[-1].strip()
                        length = int(length)
                print 'Image length = ',length

                # Copy Content To Disk
                fd = open(strFilePath, 'wb') 
                shutil.copyfileobj(ret,fd,0x10000) 
                fd.close() 
                ret.close()

                # Do not overload download
                time.sleep(1)
                
    def WalkFriends(self):
        strFriendURL=r"http://friend.renren.com/myfriendlistx.do"
        try:
            res = urllib2.urlopen(strFriendURL)
        except :
            print '******',"visit MY FRIEND LIST *",'BIG ERROR ******'
        else:
            strFriendURLContent = res.read()
            #print strFriendURLContent
            strFriendPattern = r'{"id":([0-9]*?),"vip":'
            rFriend = re.findall(strFriendPattern,strFriendURLContent,re.S|re.I)
            for subItem in rFriend:
                print 'Fetching : ',subItem
                #self.Download(subItem)
                strFriendURL = ('http://www.renren.com/%s/profile/?portal=homeFootprint&ref=home_footprint' % subItem)
                print strFriendURL
                res = urllib2.urlopen(strFriendURL)
                #print res.geturl()
                #print res.getcode()
                #print res.info()
                #str = res.read()
                
    def Login(self,username,pwd):
        # Set Cookie Jar
        cookie = cookielib.CookieJar()
        cookie_file = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(cookie_file)
        urllib2.install_opener(opener)

        # Construct Post Data
        data = {
            'email':username,
            'password':pwd,
            'origURL':'',
            'domain':'renren.com',
            'formName':'',
            'method':'',
            'isplogin':'true',
            'submit':'登陆'
            }
        web_data = urlencode(data)
        print 'web_data : ',web_data
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'}
        req=urllib2.Request(url='http://www.renren.com/PLogin.do',
                    data = web_data,
                    headers = header)
        try:
            result = urllib2.urlopen(req)
        except :
            print '******',username,'BIG ERROR ******'
            return
        else:
            print result.geturl()
            print result.getcode()
            print result.info()
            print 'Go to YOURPAGE'
            self.WalkFriends()
        print 'Picture Count : ',self.allCount
        print 'New Count : ',self.newCount
            
            
def main():
    robot = RenrenRobot()
    robot.Login('iam.cooler@yahoo.com.cn','mengxiang@')
if __name__ == '__main__':
    main()
