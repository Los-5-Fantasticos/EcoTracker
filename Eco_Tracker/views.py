from django.shortcuts import render

def index(request):
    return render(request, "ecotracker/index.html")
#Renderizar los hmtl, es decir que se vea la página xd 