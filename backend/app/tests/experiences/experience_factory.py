import factory
from app.models.experience import Experience


class ExperienceFactory(factory.Factory):
    class Meta:
        model = Experience

    title = factory.Sequence(lambda n: f"Experience {n}")
    description = factory.Faker("text")
    start_date = factory.Faker("date_time_this_decade")
    end_date = factory.Faker("date_time_this_decade")
    company = factory.Faker("company")
    user_id = 1
