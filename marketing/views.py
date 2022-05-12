from django.shortcuts import redirect, render
from .forms import *

# Create your views here.

def newsletter(request):
    
    if request.method == 'POSt':
        form = NewletterAdd(request.POST)
    else:
        form = NewletterAdd()

    return render(request,"main/index.html",{
        'form':form
    })

