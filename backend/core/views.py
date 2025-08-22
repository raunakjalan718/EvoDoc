from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to EvoDoc</h1><p>The healthcare platform that evolves with patient feedback.</p>")
