from django.shortcuts import render_to_response
from django.http import Http404

def singleHandler(singleNo):
    singleList = [0,13,17,22,27,32,37]
    try:
        singleNo = int(singleNo)
    except e:
        raise Http404
    try:
        single = singleList.index(singleNo)
    except e:
        raise Http404
    return single

def election_single(request, singleNo):
    single = singleHandler(singleNo)
    
    pass

def election_group(request, groupName):
    pass

def election_map(request, singleNo):
    single = singleHandler(singleNo)
    pass


def election_rank(request, singleNo):
    single = singleHandler(singleNo)
    pass

def election_trend(request, trendOf):
    pass