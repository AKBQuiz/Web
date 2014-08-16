from quiz.models import Quiz
from memberinfo.models import Group,Team,MemberInfo
import string, random

class QuizGetter(object):
    """docstring for Getter"""

    __template_quistion_c = 'Where is %s comefrom?'
    __template_quistion_b = 'What day is the birthday of %s?'
    __template_quistion_t = 'Which team is %s in?'
    __datefmt = '%Y-%m-%d'

    n = 20
    correlation = None
    difficulty = None
    category = None
    coding = 'utf-8'
    format = 'json'

    def setNumber(self, s):
        try:
            self.n = string.atoi(s)
        except:
            self.n = 20
        if self.n > 100:
            self.n = 100

    def setCorrelation(self, s):
        grouplist = s.split(',')
        l = []
        for g in grouplist:
            l.append(Group.objects.get(groupname = g.upper()))
        self.correlation = tuple(l)

    def setDifficulty(self, min_ = 1, max_ = 10):
        if 1 <= min_ <= max_ <= 10:
            self.difficulty = (min_, max_)
        else:
            self.difficulty = (1, 10)

    def setCategory(self, s):
        l = s.split(',')
        cat = {'f':1,'c':1,'b':1,'t':1,}

        for a in l:
            i = 0;
            if a[0] == 'u':
                n = 0
                i = i + 1
            else:
                n = 1

                if len(a) > i+1:
                    try:
                        n = string.atoi(a[i+1:]);
                    except:
                        pass

            if a[i] == 'i':
                cat['c'] = n
                cat['b'] = n
                cat['t'] = n
            else:
                cat[a[i]] = n
        self.category = cat

    def setCoding(self, s):
        c = s.lower()
        if c in ('utf-8'):
            self.coding = c

    def setFormat(self, s):
        f = s.lower()
        if f in ('json','xml'):
            self.format = f

    def getFList(self,n):
        if n == 0 :
            return []
        quizset = Quiz.objects.filter(state__gt = 0)
        if self.correlation:
            quizset = quizset.filter(correlation__in = self.correlation)
            pass

        if self.difficulty:
            quizset = quizset.filter(difficulty__lte = self.difficulty[1], difficulty__gte = self.difficulty[0])
            pass

        quizset = quizset.order_by('?').all()[:n]


        quizlist = []
        for item in quizset:
            quizItem = {"id":item.id,"q":item.question,"a":[item.answer,item.wrong_1,item.wrong_2,item.wrong_3]}
            self.shuffleAnswer(quizItem)
            quizlist.append(quizItem);
            pass
        return quizlist

    def getIList(self, comefrom , birthday , team):

        n = comefrom + birthday + team
        if n <= 0 :
            return

        import datetime
        infoset = MemberInfo.objects\
        .filter(state__gt = 0, birthday__gt = datetime.date(1980,1,1), comefrom__gt = 0)\
        .exclude(team__teamname = 'Unknown');

        if self.correlation:
            infoset = infoset.filter(team__group__in = self.correlation)
            pass

        # if self.difficulty:
        #     infoset = infoset.filter(difficulty__lte = self.difficulty[1], difficulty__gte = self.difficulty[0])
        #     pass

        infoset = infoset.order_by('?').all()[:n]


        quizList = []
        if comefrom > 0:
            from memberinfo.divisions import Division
            d = Division()
            dlist = range(1,48)

            for i in infoset[:comefrom]:
                w = random.sample(dlist,4)
                a = [d.get('id',i.comefrom)]
                a.extend([d.get('id',x) for x in w if x != i.comefrom])
                a = a [:4]
                c = random.randint(0,3)
                a[0],a[c] = a[c],a[0]
                quizList.append({"id":0,"q":self.__template_quistion_c % (i.name),"a":a, "c":c})

        if birthday > 0:
            from django.db.models import Count
            opnum = 4
            if birthday < 4:
                opnum = birthday * 4
            elif birthday <= 6:
                opnum = birthday * 3
            elif birthday <= 10:
                opnum = birthday * 2

            blist = MemberInfo.objects.values('birthday') \
            .annotate(bcount=Count('birthday')) \
            .order_by('?') \
            .all()[:4*opnum]

            for i in infoset[comefrom : comefrom + birthday]:
                a = [i.birthday.strftime(self.__datefmt)]
                w = random.sample(blist,4)
                w = [b['birthday'].strftime(self.__datefmt) for b in w]
                if a[0] in w:
                    w.remove(a[0])
                a.extend(w[:3])
                c = random.randint(0,3)
                a[0],a[c] = a[c],a[0]
                quizList.append({"id":0,"q":self.__template_quistion_b % (i.name),"a":a, "c":c})
                pass

            pass

        if team > 0:
            teamset = Team.objects.exclude(teamname = 'Unknown')
            teamlist = [i.__unicode__() for i in teamset]
            for i in infoset[comefrom + birthday :]:
                a = [i.team.__unicode__()]
                w = random.sample(teamlist,4)
                if a[0] in w:
                    w.remove(a[0])
                a.extend(w[:3])
                c = random.randint(0,3)
                a[0],a[c] = a[c],a[0]
                quizList.append({"id":0,"q":self.__template_quistion_t % (i.name),"a":a, "c":c})
            pass

        return quizList

    def shuffleAnswer(self,quizItem):
        w = quizItem['a'][1:]
        random.shuffle(w)
        for i in xrange(0,3):
            quizItem['a'][i+1] = w[i]
            pass
        c = random.randint(0,3)
        quizItem['c'] = c
        quizItem['a'][0], quizItem['a'][c] = quizItem['a'][c], quizItem['a'][0]

    def getList(self):
        quizlist = []
        if self.category:
            #############
            # total = 0
            # for k in self.category.keys():
            #     total = total + self.category[k]
            # factor = self.n / total
            # remainder = self.n % total
            # amount = {}
            # for k in self.category.keys():
            #     mutl = self.category[k]
            #     amount[k] = mutl * factor
            #     if remainder:
            #         if mutl > remainder:
            #             mutl = remainder
            #         amount[k] = amount[k] + mutl
            #         remainder = remainder - mutl
            ########

            total = sum(self.category.values())
            score = [random.randint(1,total) for i in xrange(self.n)]
            score.sort()

            amount = {}
            i = 0
            v = 0
            for k in self.category.keys():
                c = 0
                v = v + self.category[k]
                while score[i] <= v:
                    c = c + 1
                    i = i + 1
                amount[k] = c
                pass

            quizlist = self.getFList(amount['f'])
            quizlist.extend(self.getIList(amount['c'],amount['b'],amount['t']))
        else:
            quizlist = self.getFList(self.n)
        random.shuffle(quizlist)
        return quizlist
        pass

    def requestHandler(self, get):
        if 'group' in get:
            self.setCorrelation(get['group'])

        if 'n' in get:
            self.setNumber(get['n'])

        if 'category' in get:
            self.setCategory(get['category'].lower())

        # if 'difficulty' in get:
        #     d = get['difficulty'].split(',')
        #     try:
        #         min_ = string.atoi(d[0])
        #         max_ = string.atoi(d[1])
        #     except:
        #         min_ = 1
        #         max_ = 10
        #     self.setDifficulty(min_, max_)

        if 'coding' in get:
            self.setCoding(get['coding'])

        if 'format' in get:
            self.setFormat(get['format'])

    def getQuizStr(self):
        qlist = self.getList()
        if self.format == 'xml':
            from lxml import etree
            rootarray = etree.Element('array')
            for i in qlist:
                item = etree.SubElement(rootarray, 'item')
                id_ = etree.SubElement(item, 'id')
                id_.text = unicode(i['id'])
                q = etree.SubElement(item, 'question')
                q.text = i['q']
                c = etree.SubElement(item, 'correctindex')
                c.text = unicode(i['c'])
                alist = etree.SubElement(item, 'array')
                for a in i['a']:
                    ans = etree.SubElement(alist, 'answer')
                    ans.text = a
            return etree.tostring(rootarray,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            doctype='<!DOCTYPE array >')

            pass
        import json
        return json.dumps(qlist,indent=2)

    def getMimetype(self):
        if self.format == 'json':
            return 'application/json'
        elif self == 'xml':
            return 'application/xml'
        pass
