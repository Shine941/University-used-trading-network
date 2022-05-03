from django.shortcuts import render


# Create your views here.
class ChatCenterView(View):
    def chat(request):
        grop_num = request.GET.get('group')
        return render(request, 'chatting.html', {"group_num": grop_num})
