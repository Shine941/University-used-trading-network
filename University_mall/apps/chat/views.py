from django.shortcuts import render
from django.views import View
# Create your views here.
class ChatCenterView(View):
    def get(self,request):
        grop_num = request.get('group')
        return render(request, 'chatting.html', {"group_num": grop_num})
