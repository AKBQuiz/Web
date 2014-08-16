from lxml import etree
import json,datetime

def warp(data,format = None):
    if format:
        if format == 'json':
            return json.dumps(data,indent=2,cls=DatetimeEncoder)
        elif format == 'xml':
            root = etree.Element('root')
            if isinstance(data, dict):
                xmldict(data,root)
            elif isinstance(data, (list, tuple)):
                xmllist(data,root)
            else:
                root.text = unicode(data)
            return etree.tostring(root,
                pretty_print=True,
                xml_declaration=True,
                encoding='UTF-8',
                doctype='<!DOCTYPE root >')
        else:
            return None
    else:
        return unicode(data)

def xmllist(data, parent):
    for k in data:
        e = etree.SubElement(parent, 'item')
        if isinstance(k, dict):
            xmldict(k,e)
        elif isinstance(k, (list, tuple)):
            xmllist(k,e)
        else:
            e.text = unicode(data[k])
    pass

def xmldict(data, parent):
    for k in data:
        e = etree.SubElement(parent, k)
        if isinstance(data[k], dict):
            xmldict(data[k],e)
        elif isinstance(data[k], list) or isinstance(data[k], tuple):
            xmllist(data[k],e)
        else:
            e.text = unicode(data[k])
    pass

def member2dic(m):
    import divisions as div
    return {
        "mid":m.mid,
        "group":m.team.group.groupname,
        "team":m.team.teamname,
        "name":m.name,
        "nick":m.nick,
        "avatar":m.avatar,
        "generation": "%s %s" % (m.grade_group,  m.grade_num) if m.grade_group else None,
        "hometown":div.get(m.comefrom),
        "hometown_id":m.comefrom,
        "birthday":m.birthday,
        "graduate":m.graduate,
        "description":m.description,
        "bothin": "%s Team %s" % (m.bothin.group.groupname, m.bothin.teamname) if m.bothin else None,
        "createtime":m.createtime,
        "edittime":m.edittime,
        "state":m.state,
        "url":"/database/member_%s/" % m.mid
    }

def members2list(ml):
    import divisions as div
    return [{
        "mid":m.mid,
        "group":m.team.group.groupname,
        "team":m.team.teamname,
        "name":m.name,
        "nick":m.nick,
        "avatar":m.avatar,
        "generation": "%s %s" % (m.grade_group,  m.grade_num) if m.grade_group else None,
        "hometown":div.get(m.comefrom),
        "hometown_id":m.comefrom,
        "birthday":m.birthday,
        "graduate":m.graduate,
        "description":m.description,
        "bothin": "%s Team %s" % (m.bothin.group.groupname, m.bothin.teamname) if m.bothin else None,
        "state":m.state,
        "url":"/database/member_%s/" % m.mid
    }for m in ml]


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
