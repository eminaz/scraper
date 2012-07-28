from xlwt.Workbook import *
from xlwt.Style import *

from xlutils.copy import copy #http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook #http://pypi.python.org/pypi/xlrd
from xlwt import easyxf #http://pypi.python.org/pypi/xlwt

START_ROW = 0 #0 based (subtract 1 from excel row number

rb = open_workbook('10-K Mark.xls',formatting_info=True)
r_sheet = rb.sheet_by_index(0) #read only copy to introspect the file
#wb = copy(rb) #a writable copy (I can't read values out of this, only write to it)
#w_sheet = wb.get_sheet(0) #the sheet to write to within the writable copy

wb = Workbook()
ws0 = wb.add_sheet('0')

inneri=1;
for i in range(START_ROW,r_sheet.nrows):
    texts = r_sheet.cell(i,5).value
    if texts != "":
        inneri+=1
        #print r_sheet.row(i)
        colnum=0;
        for item in r_sheet.row(i):
            if(colnum,item.value):
                ws0.write(inneri,colnum,item.value)
                colnum+=1
#        print "reach"
#        name=r_sheet.cell(i,0).value
#        date=r_sheet.cell(i,1).value
#        sic=r_sheet.cell(i,2).value
#        webcik=r_sheet.cell(i,3).value
#        ws0.write(i, 0, name)
#        ws0.write(i, 1, date)
#        ws0.write(i, 2, sic)
#        ws0.write(i, 3, webcik)
#        ws0.write(i, 4, texts)

#        ws0.write(i, columnNumber, texts)

wb.save('big-16Mb-2.xls')




#wb = Workbook()
#ws0 = wb.add_sheet('0')


#ws0.write(i, 0, name)
#ws0.write(i, 1, date)
#ws0.write(i, 2, sic)
#ws0.write(i, 3, filenumber)
#ws0.write(i, 4, webcik)
#ws0.write(i, rowNumber, texts)
#
#
#wb.save('CleanData.xls')
