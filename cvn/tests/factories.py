import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'juan{0}'.format(n))
    first_name = 'Juan'
    last_name = 'Doe'

class AdminFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'admin{0}'.format(n))
    is_superuser = True
    is_staff = True
