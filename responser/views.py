from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response

@csrf_exempt
def weixin(request, istest = False):
    from responser.wxresponser import WxResponser
    if istest :
        para = dict(request.GET.iteritems())
        res = WxResponser(para,istest = True)
        return HttpResponse(res.response())
    else:
        res = WxResponser(dict(request.GET.iteritems()), request.raw_post_data)
        if res['MsgType'] == 'text':
            return render_to_response('text.xml',res.response())
        elif res['MsgType'] == 'news':
            return render_to_response('news.xml',res.response())

        pass

