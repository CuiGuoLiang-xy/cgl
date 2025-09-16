import Error
import Config
import ShopCfg
import pymysql
import pymysql.cursors
import datetime
import Account
from proto.general_pb2 import Mail
import json
import base64
import service
# 保证缓存存在
@Error.DBCatchError
def GetMoney(userid, cursor:pymysql.cursors.DictCursor = None):
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    money = 0
    if Config.grds.exists(strKey):
        money = int(Config.grds.hget(strKey, ShopCfg.ID_MONEY))
    else:
        sqlStr = "select propnum from package where userid = %s and propid = %s"
        cursor.execute(sqlStr, (userid, ShopCfg.ID_MONEY))
        res = cursor.fetchone()
        money = int(res['propnum'])
        now = datetime.datetime.now()
        Account.InitPackage(userid, now)
    return money

def GetMonday(today):
    today = datetime.datetime.strptime(str(today), "%Y-%m-%d")
    return datetime.datetime.strftime(today - datetime.timedelta(today.weekday()), "%Y_%m_%d")


def SendMail(mailinfo):
    # 校验
    # 组合数据到proto中
    # 发送给C++邮件服务器
    mailproto = Mail()
    for userid in mailinfo['useridlist']:
        mailproto.userid.append(int(userid))
    mailproto.title = mailinfo['title']
    mailproto.context = mailinfo['context']
    mailproto.type = int(mailinfo['type'])
    attach = {}
    for propid, propnum in mailinfo['attach'].items():
        if int(propid) not in ShopCfg.SHOP_LIST:
            continue
        attach[int(propid)] = int(propnum)
    mailproto.attach = json.dumps(attach)
    mailproto.buttontext = base64.b64encode(mailinfo['buttontext'].encode('utf-8'))
    mailproto.fromuserid = int(mailinfo['fromuserid'])

    # 发送给C++邮件服务器
    service.SendSvrd(Config.MAIL_HOST, Config.MAIL_PORT, mailproto.SerializeToString())

def GetMailList(userid):
    # GetGlobalMail()
    strKeyList = Config.KEY_MAIL_LIST.format(userid = userid)
    mailidlist = Config.grds.lrange(strKeyList, 0, -1)
    mailinfolist = []
    for mailid in mailidlist:
        strKey = Config.KEY_MAIL_DETAIL.format(mailid = mailid)
        res = Config.grds.hgetall(strKey)
        if not res:
            Config.grds.lrem(strKeyList, 1, mailid)
            continue
        # 拼邮件信息
    return mailinfolist
