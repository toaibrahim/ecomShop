from django.utils.text import slugify
import string
import random

def random_string_generator(N):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits,k=N))

    return res

def generate_slug(text):
    new_slug = slugify(text)
    from main.models import Item

    if Item.objects.filter(slug=new_slug).first():
        return generate_slug(text + random_string_generator(5))
    return new_slug