import ShopCfg
import ErrorCfg
import math
import Lobby
import Config
import datetime
import DBManage

def GetShopCfg(version):
    shoplist = []
    shop = ShopCfg.SHOP_LIST
    for id in shop:
        if id not in ShopCfg.SHOP_CFG:
           continue
        cfg = ShopCfg.SHOP_CFG[id]
        if version < cfg['version']:
            continue
        propdict = {
            'pid': cfg['pid'], 'ename': cfg['ename'], 'name': cfg['name'],
            'type': cfg['type'], 'pay':cfg['pay'],'money': cfg['money'], 'coin': cfg['coin'], 'rmb':cfg['rmb'],
            'paytype': cfg['paytype'], 'iconid': cfg['iconid'], 'version': cfg['version'],
            'discount': cfg['discount'], 'inventory': cfg['inventory'], 'buylimittype': cfg['buylimittype'],
            'buylimitnum': cfg['buylimitnum'], 'proplist': cfg['proplist'], 'initnum':cfg['initnum']
        }
        shoplist.append(propdict)
    return {'shoplist': shoplist, 'shopversion': ShopCfg.SHOP_VERSION}
def PresentProp(userid, propid, propnum, now):
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    proplist = ShopCfg.SHOP_CFG[propid]['proplist']
    propdict = {}
    dbproplist = []
    for prop in proplist:
        num = prop['num'] * propnum
        propdict[prop['pid']] = num
        dbproplist.append((num, now, userid, prop['pid']))
    propdict['freshtime'] = str(now)
    Config.grds.hset(strKey, mapping=propdict)
    DBManage.DBUpdatePackageInfo(dbproplist)



def ShopBuy(userid, propid, propnum, shopversion, version, paytype):
    # 检查商城版本号
    if shopversion < ShopCfg.SHOP_VERSION:
        return {'code': ErrorCfg.EC_SHOP_VERSION_LOW, 'reason': ErrorCfg.ER_SHOP_VERSION_LOW}

    # 判断道具是否存在
    if not propid in ShopCfg.SHOP_CFG:
        return {'code': ErrorCfg.EC_SHOP_NOT_EXIST, 'reason': ErrorCfg.ER_SHOP_NOT_EXIST}

    # 获取道具配置，验证客户端版本是否支持该道具
    cfg = ShopCfg.SHOP_CFG[propid]
    if version < cfg['version']:
        return {'code': ErrorCfg.EC_SHOP_CLIENT_VERSION_LOW, 'reason': ErrorCfg.ER_SHOP_CLIENT_VERSION_LOW}

    # 判断库存逻辑

    # 计算实际所需要的金额
    if paytype not in cfg['paytype']:
        return {'code': ErrorCfg.EC_SHOP_PAYTYPE_ERROR, 'reason': ErrorCfg.ER_SHOP_PAYTYPE_ERROR}
    
    needmoney = int(math.floor(cfg['pay'][paytype] * cfg['discount'] * propnum)) 

    # 判断余额是否充足
    money = Lobby.GetMoney(userid)
    if money < needmoney:
        return {'code':ErrorCfg.EC_SHOP_MONEY_NOT_ENONGH, 'reason':ErrorCfg.ER_SHOP_MONEY_NOT_ENONGH}

    # 扣款
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    money = Config.grds.hincrby(strKey, ShopCfg.ID_MONEY, -needmoney)
    if money < 0:
        Config.grds.hincrby(strKey, ShopCfg.ID_MONEY, needmoney)
        return {'code':ErrorCfg.EC_SHOP_MONEY_NOT_ENONGH, 'reason':ErrorCfg.ER_SHOP_MONEY_NOT_ENONGH}

    now = datetime.datetime.now()
    dbproplist = [(money, now, userid, ShopCfg.ID_MONEY)]
    DBManage.DBUpdatePackageInfo(dbproplist)
    # DBManage.DBUpdatePackageInfoByField(userid, ShopCfg.ID_MONEY, money, now)
    Config.grds.hset(strKey, 'freshtime', str(now))

    # 发货
    PresentProp(userid, propid, propnum, now)
    return {'code': 0, 'money': money}
