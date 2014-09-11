# -*- coding:utf-8 -*-

__author__ = "CuGBabyBeaR"
__contact__  = "fxxd3740@163.com"

import string
from responser.models import WxStatus

def makeMenu(menuID):
    if menuID == 0:
        return "[主菜单]\n 1. 开始问答\n 2. 成员信息\n 3. 成员生日"
    else:
        m = menuSetting['button'][menuID-1]
        res = ['[%s]' % m['name']]
        for i, opt in enumerate(m['sub_button']):
            res.append('%2d. %s' % (i+1, opt['name']))
        return '\n'.join(res)
    pass

def makeQuiz(status = None, user = None):
    if not status:
        try:
            status = WxStatus.objects.get(wxOpenID = user)
        except WxStatus.DoesNotExist:
            status = WxStatus.objects.create(wxOpenID = user)

    from quiz.getter import QuizGetter
    g = QuizGetter()
    g.setNumber(1)
    if status.gSetting:
        g.setCorrelation(status.gSetting)
        pass
    if status.qSetting:
        g.setCategory(status.qSetting)

    q = g.getList()[0]
    status.menuNav = 'abcd'[q['c']]
    status.save()

    return u'提问：\n%s\n A. %s\n B. %s\n C. %s\n D. %s' % (q['q'], q['a'][0], q['a'][1], q['a'][2], q['a'][3])
    pass

def queryBirthday(time):
    import datetime
    from memberinfo import query
    if time == 't':   # 今天生日的成员
        date = datetime.date.today()
        return query.wapper(query.byBirthDate(date.month, date.day))
    elif time == 'o': # 明天生日的成员
        date = datetime.date.today() + datetime.timedelta(days=1)
        return query.wapper(query.byBirthDate(date.month, date.day))
    elif time == '3': # 3天内生日的成员
        date = datetime.date.today()
        return query.wapper(query.byBirthDateRange(date.month, date.day, 3),'birthday')
    elif time == 'w': # 本周生日的成员
        date = datetime.date.today()
        date = date - datetime.timedelta(days=date.weekday())
        return query.wapper(query.byBirthDateRange(date.month, date.day, 7),'birthweekday')
    elif time == 'm': # 本月生日的成员
        date = datetime.date.today()
        return query.wapper(query.byBirthMonth(date.month),'birthday')
    else:
        return u'生日查询类型错误 b_%s' % time
        pass
    pass

def queryInfo(fType,data):
    from memberinfo import query
    if fType == 't':  # 按小队查询
        return query.wapper(query.byTeam(data),'team')
    if fType == 'n':  # 按名称查询
        return query.wapper(query.byName(data),'name')
    if fType == 'c':  # 按出身查询
        return query.wapper(query.byHometown(data),'comefrom')
    if fType == 'a':  # 按年龄查询
        data = int(data)
        if data < 10 or data > 30:
            return u'请输入正确的年龄范围 10 ~ 30'
        import datetime
        year = datetime.date.today().year - data
        return query.wapper(query.byBirthYear(year),'birthmonth')
    if fType == 'm':  # 按出生月查询
        data = int(data)
        if data < 1 or data > 12:
            return u'请输入正确的月份范围 1 ~ 12'
        return query.wapper(query.byBirthMonth(data),'birthday')
    else:
        return u'查询类型错误 i_%s' % fType
    pass

def setType(inputStr, status):
    status.qSetting = inputStr
    status.save()
    return u'设置成功！\n    将问题类型设置为%s。若出现问题的类型不符，请检查输入的字符串是否正确并重新设置'
    pass

def setGroup(inputStr, status):
    status.qSetting = inputStr
    status.save()
    return u'设置成功！\n    将相关的团体类型设置为%s。若出现问题的类型不符，请检查输入的字符串是否正确并重新设置'
    pass

def inputHandler(nav, inputStr, status):
    if nav == 'q_t':
        qType = setType (inputStr, status)
        if qType:
            return u'设置成功！\n%s' % qType
        else:
            return u'输入格式不正确！'
    elif nav == 'q_g':
        qGroup = setGroup (inputStr, status)
        if qGroup:
            return u'设置成功！\n%s' % qGroup
        else:
            return u'输入格式不正确！'
    elif nav in('i_t','i_n','i_c','i_a','i_m'):
        status.nav = '-1'
        status.save()
        return queryInfo(nav[-1],inputStr)
    else:
        status.nav == '-1'
        status.save()
        return u'查询类型不正确！ %s' % nav
    pass

def eventKeyHandler(key, status = None, user = None):
    if not status:
        try:
            status = WxStatus.objects.get(wxOpenID = user)
        except WxStatus.DoesNotExist:
            status = WxStatus.objects.create(wxOpenID = user)

    if key == 'q_n':
        return makeQuiz(status)
    elif key == 'q_h':
        status.menuNav = '-1'
        status.save()
        return u'[帮助]\n欢迎使用AKBQuiz微信公众平台\n\n“菜单” “menu” 显示主菜单\n“今天生日”  “today” 查询今天生日的成员\n“明天生日” “tomorrow” 查询明天生日的成员 \n“提问”  “quiz” 获取问题\n“帮助” “help” 显示使用帮助'
    elif key == 'q_c':
        status.menuNav = '-1'
        status.save()
        return u'[联系方式]\nAKBQuiz微信公众平台是AKBQuiz的一个子项目。AKBQuiz是一个个人项目，项目网站http://akbquiz.sinaapp.com \n我的主页 http://bears.sinaapp.com'
    elif key == 'q_t':
        status.menuNav = key
        status.save()
        return u'[设置问题类型]\n目前版本题库中可以生成的问题分类如下：\n  1. 网友出题 `f`\n  2. 成员信息 `i`\n      1) 出生地 `c`\n      2) 生日 `b`\n      3) 所属队伍\n\n例如：\n    `f6,i,ub`\n  表示网友出题和成员信息题的比例是6:1，但是不要问生日题。出生地和所属队伍的题目比例将是1:1'
    elif key == 'q_g':
        status.menuNav = key
        status.save()
        return u'[设置问题涉及的团队]\n     团体名英文缩写，可以设置多个，半角空格分隔不分大小写。\n可用团体名有：akb48 ske48 nmb48 hkt48 sdn48 ngzk48 jkt48 snh48 \n\n 例如：\n    \"akb48 ske48 ngzk48\" \n表示设置为只获得和AKB48 SKE48或NMB48相关的问题'
    elif key in ('i_t','i_n','i_c','i_a','i_m'):
        status.menuNav = key
        status.save()
        return u'输入查询关键字...'
    elif key in ('b_t','b_o','b_3','b_w','b_m'):
        status.menuNav = '-1'
        status.save()
        return queryBirthday(key[-1])
    else:
        return u'不支持的EventKey: %s ' % key

def menu(user,inputStr):
    try:
        status = WxStatus.objects.get(wxOpenID = user)
    except WxStatus.DoesNotExist:
        status = WxStatus.objects.create(wxOpenID = user)
    inputStr = inputStr.lower()
    if inputStr in (u'菜单','menu'):
        status.menuNav = '0'
        status.save();
        return makeMenu(0)
    elif inputStr in (u'今天生日', 'today'):
        status.menuNav = '-1'
        status.save();
        return queryBirthday('t')
    elif inputStr in (u'明天生日', 'tomorrow'):
        status.menuNav = '-1'
        status.save();
        return queryBirthday('o')
    elif inputStr in (u'提问', 'quiz'):
        return makeQuiz(status)
    elif inputStr in (u'帮助', 'help'):
        status.menuNav = '-1'
        status.save();
        return help()
    else:
        nav = status.menuNav
        if nav in ('', '-1', ' '):
            status.menuNav = '0'
            status.save()
            return makeMenu(0)
        elif nav in ('q_t','q_g','i_t','i_n','i_c','i_a','i_m'):
            return inputHandler(nav, inputStr, status)
        elif nav in 'abcd':
            if inputStr in 'abcd':
                status.menuNav = '-1'
                status.save()
                if inputStr == nav:
                    return u'回答正确！'
                else:
                    return u'回答错误！正确答案是%s' %  nav
            else:
                return u'请输入正确的选项'
            pass
        elif nav in string.digits:
            menuID = int(nav)
            if menuID == 0:
                if inputStr in string.digits:
                    optID = int(inputStr)
                    if 1 <= optID <= 3:
                        status.menuNav = inputStr
                        status.save()
                        return makeMenu(optID)
                return u'请输入正确的菜单选项'
            else:
                m = menuSetting['button'][menuID-1]['sub_button']
                if inputStr in string.digits:
                    optID = int(inputStr)
                    if 1 <= optID <= len(m):
                        key = m[optID-1]['key']
                        return eventKeyHandler(key,status)
                return u'请输入正确的菜单选项'



menuSetting = {
    'button':[
    {
        'name':'开始问答',
        'sub_button':[
            {'name':'开始游戏','type':'click','key' :'q_n',},
            {'name':'问题类型设置','type':'click','key' :'q_t',},
            {'name':'相关团体设置','type':'click','key' :'q_g',},
            {'name':'帮助','type':'click','key' :'q_h',},
            {'name':'联系方式','type':'click','key' :'q_c',},
        ]
    },
    {
        'name':'成员信息',
        'sub_button':[
            {'name':'按小队查询','type':'click','key' :'i_t',},
            {'name':'按姓名查询','type':'click','key' :'i_n',},
            {'name':'按出身地查询','type':'click','key' :'i_c',},
            {'name':'按年龄查询','type':'click','key' :'i_a',},
            {'name':'按出生月查询','type':'click','key' :'i_m',},
        ]
    },
    {
        'name':'成员生日',
        'sub_button':[
            {'name':'今天生日成员','type':'click','key' :'b_t',},
            {'name':'明天生日成员','type':'click','key' :'b_o',},
            {'name':'三天内生日的成员','type':'click','key' :'b_3',},
            {'name':'本周生日成员','type':'click','key' :'b_w',},
            {'name':'本月生日成员','type':'click','key' :'b_m',},
        ]
    },
    ]
}



# 状态机说明
#
#      |   -1    |    0   |    1     |    2     |    3      |   q_t     |    q_g    |    i_t    |    i_n    |    i_c    |    i_a    |    i_m    |   ans    |
# 菜单 |                                                          菜单0 / 0                                                                                |
# 生日 |                                                           生日 / -1                                                                               |
# 提问 |                                                           提问 / ans                                                                              |
# 帮助 |                                                           帮助 / -1                                                                               |
#    1 | 菜单0/0 | 菜单1/1| 提问/ans | 输入/i_t |今天生日/-1|  *        |   *       |    *      |    *      |    *      |    *      |    *      |    *     |
#    2 | 菜单0/0 | 菜单2/2| 类设置/0 | 输入/i_n |明天生日/-1|  *        |   *       |    *      |    *      |    *      |    *      |    *      |    *     |
#    3 | 菜单0/0 | 菜单3/3| 团设置/0 | 输入/i_c |三天生日/-1|  *        |   *       |    *      |    *      |    *      |    *      |    *      |    *     |
#    4 | 菜单0/0 | *      | *        | 输入/i_a |本周生日/-1|  *        |   *       |    *      |    *      |    *      |    *      |    *      |    *     |
#    5 | 菜单0/0 | *      | *        | 输入/i_m |本月生日/-1|  *        |   *       |    *      |    *      |    *      |    *      |    *      |    *     |
# 选项 | 菜单0/0 | *      | *        | *        |  *        |  *        |   *       |    *      |    *      |    *      |    *      |    *      |  结果/-1 |
# 其他 | 菜单0/0 | *      | *        | *        |  *        |类型解析/-1|团体解析/-1|输入查询/-1|输入查询/-1|输入查询/-1|输入查询/-1|输入查询/-1|    *     |
