from django.shortcuts import render

def front_view(request):
    return render(request, template_name="index.html")
