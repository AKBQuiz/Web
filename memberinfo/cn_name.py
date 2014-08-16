from memberinfo.models import MemberInfo
from memberinfo.cn_jp import jp2cn,cn2jp

for m in MemberInfo.objects.filter(cn_name__isnull=False):
    l = []
    for c in m.cn_name:
        l.append(jp2cn(c))
    m.cn_name = ''.join(l)
    m.save()
