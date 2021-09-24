from django.utils.text import slugify


def generate_username(firstname, lastname):
    firstname = slugify(firstname)
    lastname = slugify(lastname)
    username = '%s.%s' % (firstname, lastname)
    return username


def generate_email(username, domain):
    email = '%s@%s' % (username, domain)
    return email
