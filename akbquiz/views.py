from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response("index.html")

def home(request):
    return render_to_response("home.html", context_instance = RequestContext(request))
    pass
