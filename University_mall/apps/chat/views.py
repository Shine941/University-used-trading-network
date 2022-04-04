from django.shortcuts import render

# Create your views here.
def index(request):
    grop_num = request.GET.get('group')
    return render(request, 'index.html', {"group_num": grop_num})