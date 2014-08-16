# from crawler.models import OfficialInfo
# for m in OfficialInfo.objects.filter(mid__isnull=False):
#     m.mid.name = m.name
#     m.mid.save()

from memberinfo.cn_jp import cn2jp

from memberinfo.models import MemberInfo

for m in MemberInfo.objects.exclude(officialinfo__mid__isnull=False):
    l = []
    for c in m.name:
        l.append(cn2jp(c))
    m.name = ''.join(l)
    m.save()
