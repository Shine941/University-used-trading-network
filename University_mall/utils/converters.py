from django.urls import converters


class USernameConverter:
    regex = '[a-zA-Z0-9_-]{2,20}'

    def to_python(self, value):
        return value
