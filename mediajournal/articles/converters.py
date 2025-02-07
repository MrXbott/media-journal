

class CustomSlugConverter():
    regex = '[-a-zA-Z0-9_/]+'

    def to_python(self, value):
        slug = value.split('/')
        return slug
    
    def to_url(self, value):
        return value