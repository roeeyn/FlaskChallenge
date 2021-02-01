import factory
from src.models import GitHubUserOrm
from src.db import session


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GitHubUserOrm
        sqlalchemy_session = session  # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n + 1)  # from 1 to n
    username = factory.Faker("first_name")
    img_url = factory.Faker("domain_name", levels=2)
    profile_url = factory.Faker("domain_name", levels=2)
    user_type = factory.Faker("random_element", elements=["User", "Organization"])
