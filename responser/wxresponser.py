# -*- coding:utf-8 -*-

__author__ = "CuGBabyBeaR"
__email__  = "fxxd3740@163.com"


import hashlib, time
from lxml import etree

class WxResponser(object):
    """docstring for WxResponser"""

    WEIXIN_NAME = "AKBQuiz"
    token = "akbquiz_weixin"
    def __init__(self, para, content = "" , istest = False):
        self.istest = istest
        self.para = para
        self.content = content
        if istest:
            self.msgIn = {
                "ToUserName":self.WEIXIN_NAME,
                "FromUserName":"tester",
                "CreateTime":1234567,
                "MsgType":"text",
                "Content":para.get("content", "none content"),
            }

    def checkSignature(self):
        tArr = [self.token, self.para["timestamp"], self.para["nonce"]]
        tArr.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,tArr)
        code = sha1.hexdigest()
        if code == self.para["signature"]:
            return True
        else:
            return False

    def unpackXml(self):
        xml = etree.fromstring(self.content)
        self.msgIn = {}
        for ele in xml :
            self.msgIn[ele.tag] = ele.text

    def packXml(self):
        res = ['<xml>']
        for k, v in self.msgOut.iteritems():
            res.append("<%s><![CDATA[%s]]></%s>" % (k,v,k))
        res.append('</xml>')
        print res
        return '\n'.join(res)

    def logic(self):

        self.msgOut = {}
        self.msgOut["ToUserName"] = self.msgIn.get("FromUserName", None)
        self.msgOut["FromUserName"] = self.msgIn.get("ToUserName", None)
        self.msgOut["MsgType"] = "text"
        self.msgOut["CreateTime"] = int(time.time())

        msgType = self.msgIn.get("MsgType")
        if  msgType == "text":
            from responser.wxmenu import menu
            self.msgOut["Content"] = menu(self.msgIn["FromUserName"], self.msgIn["Content"])

        elif msgType in ("image","voice","video","location","link"):
            self.msgOut["Content"] = u"不支持\"%s\"消息类型" % msgType

        elif msgType == "event":
            eventType = self.msgIn["eventType"]
            if eventType == "subscribe":
                self.msgOut["Content"] = u"欢迎使用AKBQuiz微信公众平台!\n在任何时候发送“菜单”或者“menu”显示主菜单，发送“帮助”或“help”获得使用方法。"
            elif eventType == "unsubscribe":
                self.msgOut["Content"] = u"感谢您的使用，请继续关注AKB48哦"
            elif eventType == "CLICK":
                from responser.wxmenu import eventKeyHandler
                self.msgOut["Content"] = eventKeyHandler(user = self.msgIn.get("FromUserName"))
            elif eventType in ("SCAN", "LOCATION", "VIEW"):
                self.msgOut["Content"] = u"不支持当前事件类型"
            else:
                self.msgOut["Content"] = u"事件类型错误"
        else:
            self.msgOut["Content"] = u"消息类型错误! \nmsgType : %s" % msgType

        pass

    def response(self):
        if self.istest:
            self.logic()
            return self.msgOut['Content']
            pass
        else:
            if not self.checkSignature():
                return ""
            if 'echostr' in self.para :
                return self.para["echostr"]
            self.unpackXml()
            self.logic()
            return self.msgOut


