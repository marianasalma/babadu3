from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "login.html")

def landing(request):
    return render(request, "landing.html")