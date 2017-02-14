import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
import db.mymongo as mymongo

def initconnect(self):
    print("init connection")
    self.kiwoom.connect(self.kiwoom, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)


def callTR(self, kiwoom):
    self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "039490")
    self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "Request1", "opt10001", 0, "0101")

    # item_codes = GetCodeListByMarket(self.kiwoom, 0)
    # print('%s' % item_codes)

def callCommRealData(self, kiwoom):
    print (' -- 조회 -- ')
    # code = '252.50'
    # month = '201612'
    # callcode = GetOptionCallCode(self, kiwoom, code, month)
    # print("%s %s %s" % (code, callcode, month))
    # RequestOpt50067(self, callcode, '1')

    # RequestOpt50021(self, kiwoom, "201701")
    # RequestOpt50022(self, kiwoom)

    # self.test = R50067()
    # self.test.set(kiwoom)
    # self.test.start()
    callTR(self, kiwoom)


def updateChartData(self, kiwoom, date):
    pricelist = GetActPriceList(self, kiwoom)
    prices = pricelist.split(';')
    self.rcodelist = []
    for price in prices:
        code =  price[:3] + '.' + price[3:]
        callcode = GetOptionCallCode(self, kiwoom, code, date)
        putcode = GetOptionPutCode(self, kiwoom, code, date)
        self.rcodelist.append(callcode)
        self.rcodelist.append(putcode)

    print ("price size: %d" % len(self.rcodelist))


    self.cur_idx = int(len(self.rcodelist)/2 -10)
    UpdateRecursive(self)

def UpdateRecursive(self):
    idx = self.cur_idx
    if idx > int(len(self.rcodelist)/2+10):
        print(' --------------- done --------------')
        return
    code = self.rcodelist[idx]
    time = "3"
    print("request idx %d, code: %s, time: %s" % (idx, code, time))
    mymongo.setTable(self, code)
    RequestOpt50067(self , code, time)
    self.cur_idx +=1

# call

def RequestOpt50067(self,  code, time):
    self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
    self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "시간단위", time)

    self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt50067", "opt50067", 0, "0630")
    # GetActPriceList(self, kiwoom);
    # GetOptionCode(self, kiwoom);
    # RequestOpt50021(self, kiwoom);


# def RequestOpt50067(self, kiwoom):
#     self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "201LC257")
#     self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "시간단위", "60")
#     mymongo.setCode(self, "201LC257", "60")
#
#     self.kiwoom.dynamicCall("CommRqData(QString, QString, QString, QString)", "opt50067", "opt50067", "0", "0630")


# 선물옵션현재가정보
def RequestOpt50001(self, kiwoom):
    self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "201LC260")
    self.kiwoom.dynamicCall("CommRqData(QString, QString, QString, QString)", "opt50001", "opt50001", "0", "0451")

# 콜종목결제월별시세
def RequestOpt50021(self, kiwoom, month):
    self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "만기년월", month)
    self.kiwoom.dynamicCall("CommRqData(QString, QString, QString, QString)", "opt50021", "opt50021", "0", "0460")

# 풋종목결제월별시세
def RequestOpt50022(self, kiwoom):
    self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "만기년월", "201612")
    self.kiwoom.dynamicCall("CommRqData(QString, QString, QString, QString)", "opt50022", "opt50022", "0", "0460")


# 행사가 리스트
def GetActPriceList(self, kiwoom):
    ret = self.kiwoom.dynamicCall("GetActPriceList()")
    print('RET: %s' % ret)
    return ret

# 옵션 코드 리턴
def GetOptionCode(self, kiwoom):
    ret = self.kiwoom.dynamicCall("GetOptionCode(\"252.50\", 2, \"201612\")");
    print('RET: %s' % ret)

    ret = self.kiwoom.dynamicCall("GetOptionCode(\"252.50\", 3, \"201612\")");
    print('RET: %s' % ret)

def GetOptionCallCode(self, kiwoom, code, date):
    ret = self.kiwoom.dynamicCall("GetOptionCode(\""+code+"\", 2, \""+date+"\")");
    return ret

def GetOptionPutCode(self, kiwoom, code, date):
    #ret = self.kiwoom.dynamicCall("GetOptionCode(\"252.50\", 3, \"201612\")");
    ret = self.kiwoom.dynamicCall("GetOptionCode(\"" + code + "\", 3, \"" + date + "\")");
    return ret

# ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrorCode, Message, SplmMsg
def receiveTR(self, *params):

    RQName = params[1]
    TrCode = params[2]
    if RQName == "Request1":
        name = getInfo(self, "종목명", *params);
        volume = getInfo(self, "거래량", *params);
        price = getInfo(self, "현재가", *params);
        high = getInfo(self, "고가", *params);

        self.text_edit.append("종목명: " + name.strip())
        self.text_edit.append("거래량: " + volume.strip())
        self.text_edit.append("현재가: " + price.strip())
        self.text_edit.append("고가: " + high.strip())
    if RQName == "RequestOption":
        ttt = getInfo(self, "현재가", *params);
        tt2 = getInfo(self, "거래량", *params);
    if RQName == "opt50001":
        sum = []
        for name in ["종목명", "현재가", "거래량", "시가", "고가", "저가"]:
            value =  getInfo(self, name, *params).strip();
            sum.append(value)
        print(sum )

    if RQName == "opt50021" or RQName == 'opt50022':

        sum = []

        for i in range(0, 100):
            fvalue = []
            for name in ["미결제약정", "누적거래량", "행사가", "지수환산", "현재가", "기준가" , "시가", "고가", "저가"]:
                value = getInfo2(self, name, i, *params).strip()
                if value == "":
                    break
                if "." in value:
                    fvalue.append(float(value))
                else:
                    fvalue.append(int(value))

            if len(fvalue) == 0:
                break
            sum.append(fvalue)
            print(' %s' % ( fvalue))

    if RQName == "opt50066":
        sum = []

        for i in range(0, 100):
            fvalue = []
            for name in ["현재가", "거래량", "체결시간", "시가", "고가", "저가" , "전일종가"]:
                value = getInfo2(self, name, i, *params).strip()
                if value == "":
                    break
                if "." in value:
                    fvalue.append(float(value))
                else:
                    fvalue.append(int(value))

            if len(fvalue) == 0:
                break
            sum.append(fvalue)
            print(fvalue)

    if RQName == "opt50067":
        sum = []

        print("RES: opt50067")

        self.test.process(params)

    if RQName == "opt50068":
        sum = []

        print("RES: opt50068")

        self.test.process(params)

def GetCodeListByMarket(self, sMarket):
    ret = self.dynamicCall("GetCodeListByMarket(QString)", sMarket)
    item_codes = ret.split(';')
    return item_codes


def showAccount(self):
    ### 4.GetLoginInfo (사용자 정보)

    print("show account")
    account_cnt = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCOUNT_CNT"])
    account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
    user_id = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["USER_ID"])
    user_name = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["USER_NAME"])
    keyboard = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["KEY_BSECGB"])
    fire = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["FIREW_SECGB"])

    print("show: " + account_cnt.strip() )
    self.text_edit.append("전체계좌수: " + account_cnt.strip())
    self.text_edit.append("계좌번호: " + account_num.rstrip(';'))
    self.text_edit.append("ID: " + user_id.strip())
    self.text_edit.append("사용자명: " + user_name.strip())
    self.text_edit.append("키보드보안: " + keyboard.strip())
    self.text_edit.append("방화벽 설정: " + fire.strip())


def getInfo(self, name, *params):
    RQName = params[1]
    TrCode = params[2]
    return self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", TrCode, "", RQName, 0, name)

def getInfo2(self, name, idx, *params):
    RQName = params[1]
    TrCode = params[2]
    return self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", TrCode, "", RQName, idx, name)
