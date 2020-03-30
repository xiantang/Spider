from WindPy import *
import datetime
import xlwt

# 股票当天收盘价 -  对应合约的收盘 wsd取日数据 基差

# 合约
start_time='2018-03-14' #开始时间

end_time='2018-03-20'#结束时间
tdays=w.tdays(start_time,end_time)
husheng300=['000300','IF']
zhongzheng500=['000905','IC']
shangzheng50=['000016','IH']
rb=xlwt.Workbook()

def wsd(name,method,start,end):
    Share_close = w.wsd(name,method , start, end, "TradingCalendar=SZSE;PriceAdj=F")
    return  Share_close.Data[0]
def calculate(name,sheet):
    Share_code=name[0]
    agreement=name[1]
    daylist = []
    row=1
    write_title_to_excel(sheet)
    for i in w.tdays(start_time,end_time).Data[0]: #创建一个新的列表将时间格式转换下 转换为正常的日期
        # print(i.strftime("%Y-%m-%d"))
        daylist.append(i.strftime("%Y-%m-%d"))
    # print(daylist)
    # Share_close=w.wsd("{}.SH".format(Share_code), "close",start_time , end_time, "TradingCalendar=SZSE;PriceAdj=F") #股票的价格
    Share_close=wsd("{}.SH".format(Share_code),"close",start_time , end_time) #股票收盘价
    Contract_price = wsd("{}.CFE".format(agreement), "settle", start_time, end_time)  # 对应合约的收盘价格
    Contract_price_00 = wsd("{}00.CFE".format(agreement), "settle", start_time, end_time,)  # 对应合约的收盘价格
    Contract_price_01 = wsd("{}01.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的收盘价格
    Contract_price_02 = wsd("{}02.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的收盘价格
    Contract_price_03 = wsd("{}03.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的收盘价格
    Contract_volume = wsd("{}.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的成交价格
    Contract_volume_00 = wsd("{}.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的成交价格
    Contract_volume_01 = wsd("{}01.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的成交价格
    Contract_volume_02 = wsd("{}02.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的成交价格
    Contract_volume_03 = wsd("{}03.CFE".format(agreement), "settle", start_time, end_time, )  # 对应合约的成交价格

    for day,Share,Contract,Contract_00,Contract_01,Contract_02,Contract_03,volume,volume_00 ,volume_01,volume_02,volume_03 in zip(daylist,Share_close,Contract_price,
                                                                       Contract_price_00,Contract_price_01,
                                                                       Contract_price_02,Contract_price_03,
                                                                        Contract_volume,Contract_volume_00,
                                                                        Contract_volume_01,Contract_volume_02,
                                                                        Contract_volume_03
                                                                       ):
        Basis=Contract - Share #主基差
        #各个合约的基差
        Basis00 = Contract_00 - Share
        Basis01 = Contract_01 - Share
        Basis02 = Contract_02 - Share
        Basis03 = Contract_03 - Share
        Average_basis=(Basis+Basis01+Basis02+Basis00+Basis03)/5

        data=[day,Basis,Basis00,Basis01,Basis02,Basis03,volume,volume_00,volume_01,volume_02,volume_03,Share,Average_basis]
        write_to_excel(sheet,data,row)
        row+=1
def write_title_to_excel(sheet): #标题写入
    title=['日期','IF.CFE基差','IF00.CFE基差','IF01.CFE基差','IF02.CFE基差','IF03.CFE基差','IF.CFE成交量','IF00.CFE成交量','IF01.CFE成交量','IF02.CFE成交量','IF03.CFE成交量','沪深300','平均基差指数','加权平均指数','政策']
    for i in range(len(title)):
        sheet.write(0,i,title[i])

def write_to_excel(sheet,data,row): #内容写入

    for j in range(len(data)):
        sheet.write(row, j, data[j])

def mymain():
    w.start()
    # sheet = rb.sheet_by_index(1)
    sheet300 = rb.add_sheet("沪深300")
    calculate(husheng300,sheet300)
    print("沪深300写入成功")
    sheet500 = rb.add_sheet("中证500")
    calculate(zhongzheng500, sheet500)
    print("中证500写入成功")
    sheet50=rb.add_sheet("上证50")
    calculate(shangzheng50, sheet50)
    print("上证50写入成功")
    rb.save('wind.xls')

if __name__ == '__main__':
    mymain()