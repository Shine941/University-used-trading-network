from django.urls import path
from apps.verifications.views import ImageCodeView,SmsCodeView
# this.host + "/image_codes/" + this.image_code_id + "/";
urlpatterns=[
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<mobile>/', SmsCodeView.as_view()),

]