from django.shortcuts import render


def dashboard(request):
    return render(request, "parking/dashboard.html")
# Create your views here.
