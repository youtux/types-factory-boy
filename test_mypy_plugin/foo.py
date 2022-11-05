from dataclasses import dataclass

from factory import Factory, Faker, SubFactory


@dataclass
class Author:
    name: str


@dataclass
class Article:
    title: str
    content: str

    author: Author


class AuthorFactory(Factory):
    class Meta:
        model = Author

    name = Faker("name")


class ArticleFactory(Factory):
    class Meta:
        model = Article

    title = Faker("sentence")
    content = Faker("text")
    author = SubFactory(AuthorFactory)


a = ArticleFactory.create()

reveal_type(a)

a.title.split()
a.content.split()
a.author.name.split()
