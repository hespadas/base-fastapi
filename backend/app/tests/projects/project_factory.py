import factory
from app.models.project import Project


class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Project {n}")
    description = factory.Faker("text")
    github_url = factory.Faker("url")
    project_url = factory.Faker("url")
    user_id = 1
