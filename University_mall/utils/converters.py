from django.urls import converters


class UsernameConverter:
    regex = '[a-zA-Z0-9_-]{2,20}'

    def to_python(self, value):
        return value


class MobileConverter:
    regex = '(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}'

    def to_python(self, value):
        return value


class StuidConverter:
    regex = '[0-9]{12}'

    def to_python(self, value):
        return value


class StunameConverter:
    regex = '[\u4E00-\u9FA5A-Za-z0-9]{2,20}'

    def to_python(self, value):
        return value
class UseridConverter:
    regex ='^[0-9]*'
    def to_python(self, value):
        return value
