from django.shortcuts import render
from .models import info
# Create your views here.

def index(request):
    obj=info.objects.all()
    com={
        "com":obj
    }

    return render(request,'index.html',com)