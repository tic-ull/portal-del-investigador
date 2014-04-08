import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'juan{0}'.format(n))
    first_name = 'Juan'
    last_name = 'Doe'
