import datetime
import math
from django.shortcuts import render
from django.http import HttpResponse
from law.models import Results
from search import dosearch
import sys
from time import clock
# Create your views here.

PAGE_SIZE=10

def home(request):
    now=datetime.datetime.now()
    return render(request,'temp.html',{'current_time':now})

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if 'page' in request.GET:
            page = unicode(request.GET['page'])
        else:
            page = unicode(1)
        start = clock()
        
        #this list is used to obtain the total_hits,only total_hits[0] is used.
        total_hits = []
        results = dosearch(q,page,total_hits)
        end = clock()
        return render(request,'res1.html', {'results' : results,
                                                    'query':q,
                                                    'count':total_hits[0],
                                                    'time':end-start,
                                                    'page':page,
                                                    'total_page':int(math.ceil(total_hits[0]/float(PAGE_SIZE))),
                                                    'host':request.META['SERVER_NAME'],
                                                    'port':request.META['SERVER_PORT'],
                                                    'nextpage':int(page)+1,
                                                    'pastpage':int(page)-1})
    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)
