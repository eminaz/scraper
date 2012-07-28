import lxml.html as lh
from lxml import etree
import lxml.etree
from time import *
from xlwt.Workbook import *
from xlwt.Style import *

i = -1
#result = array();
str2=""
paragraphs=""

wb = Workbook()
ws0 = wb.add_sheet('0')
 
web="http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=10-k&CIK=";

k1="hedg"
#k1="price"
k2="swap"
k3="derivative"
k4="notional"
k5="SFAS no. 119"
k6="futures"
k7="risk management"
k8="SFAS 133"
k9="SFAS 119"
k10="FASB 119"
k11="SFAS no. 133"
#change this
#                                k12="price"
k12="forward"

#the string for xpath selection
selectionText='[contains(text(),"'+k1+'") or contains(text(),"'+k2+'") or contains(text(),"'+k3+'") or contains(text(),"'+k4+'")or contains(text(),"'+k5+'") or contains(text(),"'+k6+'") or contains(text(),"'+k7+'") or contains(text(),"'+k8+'")  or contains(text(),"'+k9+'") or contains(text(),"'+k10+'") or contains(text(),"'+k11+'") or (contains(text(),"'+k12+'") and (not (contains(text(),"carryforward") or contains(text(),"carry forward") or contains(text(),"carry-forward") or contains(text(),"forward-looking") or contains(text(),"forward looking"))))]'                          
selectionRaw='//*'+selectionText
selectionTen='//div/div'+selectionText+' | //prev'+selectionText+' | //p'+selectionText+' | //p/font'+selectionText;
count=1;
#need to change this to (0,2)

#count=count+1
#cik="000"+str(d0)+str(d1)+str(d2)+str(d3)+str(d4)+str(d5)+str(d6)
#webcik=web+cik
#need to change this
#webcik="http://www.sec.gov/cgi-bin/browse-edgar?CIK=0000945265&action=getcompany"
#webcik="http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=10-k&CIK=0001000050"

bigcount=0
for sic in range(2000,2999):
    if(bigcount>2000):
        print "finish"
        print sic
        break
    searchWeb="http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=&filenum=&State=&Country=&type=10-k&Find=Find+Companies&action=getcompany&type=10-k&SIC="+str(sic)
    tree=lh.parse(searchWeb)
    nodes=tree.xpath("//a/@href")
    arr=[]
    smallcount=0;
    
    for node in nodes:
        if("CIK" in node): #only get the links that direct us to the place we want
            node="http://www.sec.gov"+node
            arr.append(node)
    for arr1 in arr:
        bigcount+=1

        if(smallcount<30):
            smallcount+=1;

            #print arr1
        #    searchResult="http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000053453&owner=include&count=40&hidefilings=0"
            searchResult=arr1
            searchResult+="&type=10-k"
            webcik=searchResult
        
            
            
            #           print webcik
            # $nodes = $xpath->query("//a[@id='documentsbutton']/@href");
            
            tree=lh.parse(webcik)
            nodes=tree.xpath("//a[@id='documentsbutton']/@href")
            
            #if(nodes):
            nodenum=-1;
            if(nodes):
             name=tree.xpath("//span[@class='companyName']")[0].text
             filenumber=tree.xpath("//td/a")[2].text
            
            for node in nodes:
             nodenum=nodenum+1;
             date=tree.xpath("//td")[10+5*nodenum].text
            
             link="http://www.sec.gov"+node
            #                                print link
            #                                print name
            #                                print date
            #                                print cik
            #                                print filenumber.encode('gbk','ignore')
             
             tree2=lh.parse(link)
             #ten=tree2.xpath("//div/table/tr[td='10-K']/td/a/@href")
             ten=tree2.xpath("//div/table/tr[td[contains(text(),'10-K')]]/td/a/@href")
            
             #summary=tree.xpath("//div/table/tr[td='Complete submission text file']/td/a/@href")
             useten=False
            
             if(ten):
                 if(ten[0].__len__()>30):  #if the link to the 1o-k file is valid
                     useten=True   #use the 10-k file
                     # print ten
             texts=""
             columnNumber=5;

            
             if(not useten):  #use the summary file instead   
            #                      print "not using ten" 
                 summary=tree2.xpath("//div/table/tr[td='Complete submission text file']/td/a/@href")
                 #code for summary
                 link2="http://www.sec.gov"+summary[0]
                 tree3 = lh.parse(link2)
            #                                    selectionText='[contains(text(),"price")]'
                 elements3=tree3.xpath(selectionRaw)
            #                                    elements3=tree3.xpath('//*[contains(text(),"price")]')
                 for e in elements3:
                     if(e.text!=None):
                         paras=e.text.split("\n\n")
                         for para in paras:
                             if(para.find("-----")==-1 and (para.find(k1)!=-1 or para.find(k2)!=-1 or para.find(k3)!=-1 or para.find(k4)!=-1 or para.find(k5)!=-1 or para.find(k6)!=-1 or para.find(k7)!=-1 or para.find(k8)!=-1 or para.find(k9)!=-1 or para.find(k10)!=-1 or para.find(k11)!=-1 or para.find(k12)!=-1)):
            #                     texts+=para.replace('\n', ' ').replace('\r', ' ')+"\n\n";
                                    texts=para.replace('\n', ' ').replace('\r', ' ')+"\n\n";
                                    if(texts):
                                         i=i+1
                                         ws0.write(i, 0, name)
                                         ws0.write(i, 1, date)
                                         ws0.write(i, 2, sic)
                                         ws0.write(i, 3, filenumber)
                                         ws0.write(i, 4, webcik)
                                         if(texts.__len__()<32766):
                                             ws0.write(i, 5, texts)
                                         else:
                                             ws0.write(i, 5, texts[0:32766])
                                             ws0.write(i, 6, "too many words")

                                     
             if(useten):
                 link2="http://www.sec.gov"+ten[0]
            #                    print link2
                 tree3 = lh.parse(link2)                          
            #                                    elements2=tree3.xpath('//div/div[contains(text(),"'+k1+'") or contains(text(),"'+k2+'") or contains(text(),"'+k3+'") or contains(text(),"'+k4+'") or contains(text(),"'+k5+'") or contains(text(),"'+k6+'") or contains(text(),"'+k7+'") or contains(text(),"'+k8+'") or contains(text(),"'+k9+'") or contains(text(),"'+k10+'") or contains(text(),"'+k11+'") or contains(text(),"'+k12+'")] | //prev[contains(text(),"'+k1+'") or contains(text(),"'+k2+'") or contains(text(),"'+k3+'") or contains(text(),"'+k4+'") or contains(text(),"'+k5+'") or contains(text(),"'+k6+'") or contains(text(),"'+k7+'") or contains(text(),"'+k8+'") or contains(text(),"'+k9+'") or contains(text(),"'+k10+'") or contains(text(),"'+k11+'") or contains(text(),"'+k12+'")] | //p[contains(text(),"'+k1+'") or contains(text(),"'+k2+'") or contains(text(),"'+k3+'") or contains(text(),"'+k4+'") or contains(text(),"'+k5+'") or contains(text(),"'+k6+'") or contains(text(),"'+k7+'") or contains(text(),"'+k8+'") or contains(text(),"'+k9+'") or contains(text(),"'+k10+'") or contains(text(),"'+k11+'") or contains(text(),"'+k12+'")] | //p/font[contains(text(),"'+k1+'") or contains(text(),"'+k2+'") or contains(text(),"'+k3+'") or contains(text(),"'+k4+'") or contains(text(),"'+k5+'") or contains(text(),"'+k6+'") or contains(text(),"'+k7+'") or contains(text(),"'+k8+'") or contains(text(),"'+k9+'") or contains(text(),"'+k10+'") or contains(text(),"'+k11+'") or contains(text(),"'+k12+'")]')    
                 elements2=tree3.xpath(selectionTen);
                 #  print elements2
                 if(elements2):
            #         print "not raw"
                     for element in elements2:
                         # print element.text.encode('gbk', 'ignore')
                         if(element.text):
            #                 texts+=element.text.replace('\n', ' ').replace('\r', ' ')+"\n\n";
                             texts=element.text.replace('\n', ' ').replace('\r', ' ')+"\n\n";
                             if(texts):
                                 i=i+1
                                 ws0.write(i, 0, name)
                                 ws0.write(i, 1, date)
                                 ws0.write(i, 2, sic)
                                 ws0.write(i, 3, filenumber)
                                 ws0.write(i, 4, webcik)
                                 if(texts.__len__()<32766):
                                     ws0.write(i, 5, texts)
                                 else:
                                     ws0.write(i, 5, texts[0:32766])
                                     ws0.write(i, 6, "too many words")
            
                 else: #parse raw text
            #          print "using raw"
            #                                        elements3=tree3.xpath('//*[contains(text(),"'+k1+'") or contains(text(),"'+k2+'")]')
                     elements3=tree3.xpath(selectionRaw)
                     for e in elements3:
                         if(e.text!=None):
                             paras=e.text.split("\n\n")
                             for para in paras:
                                 if(para.find("-----")==-1 and (para.find(k1)!=-1 or para.find(k2)!=-1 or para.find(k3)!=-1 or para.find(k4)!=-1 or para.find(k5)!=-1 or para.find(k6)!=-1 or para.find(k7)!=-1 or para.find(k8)!=-1 or para.find(k9)!=-1 or para.find(k10)!=-1 or para.find(k11)!=-1 or para.find(k12)!=-1)):
            #                         texts+=para.replace('\n', ' ').replace('\r', ' ')+"\n\n";
                                    texts=para.replace('\n', ' ').replace('\r', ' ')+"\n\n";
                                    if(texts):
                                         i=i+1
                                         ws0.write(i, 0, name)
                                         ws0.write(i, 1, date)
                                         ws0.write(i, 2, sic)
                                         ws0.write(i, 3, filenumber)
                                         ws0.write(i, 4, webcik)                                        
                                         if(texts.__len__()<32766):
                                             ws0.write(i, 5, texts)
                                         else:
                                             ws0.write(i, 5, texts[0:32766])
                                             ws0.write(i, 6, "too many words")
      
             #     print texts
            #                 print useten
            # if(texts):
            
            #     if(texts.__len__()<32766):
            #         ws0.write(i, 4, texts)
            #     else:
            #         ws0.write(i, 4, texts[0:32766])
            #         ws0.write(i, 6, "too many words")
            
             wb.save('10-K Mark.xls')
             
             if(count%50==0):
                print webcik
        



                                    
#                                  


#wb = Workbook()
#ws0 = wb.add_sheet('0')

rowcount = 6000 + 1

t0 = time()
print "\nstart: %s" % ctime(t0)

print "Filling..."
#for row in xrange(rowcount):
    #ws0.write(row, col, "BIG(%d, %d)" % (row, col))
#    ws0.write(row, 1, texts)

t1 = time() - t0
print "\nsince starting elapsed %.2f s" % (t1)

print "Storing..."
wb.save('big-16Mb.xls')

t2 = time() - t0
print "since starting elapsed %.2f s" % (t2)




