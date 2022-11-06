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


article = ArticleFactory.create()

author = AuthorFactory.create()

reveal_type(article)
reveal_type(author)

article.title.split()
article.content.split()
article.author.name.split()
