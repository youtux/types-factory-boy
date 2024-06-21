from dataclasses import dataclass
from typing import cast

from factory import Factory, Faker, SubFactory
from factory.builder import BuildStep, DeclarationSet, Resolver


@dataclass
class Author:
    name: str


r: Resolver[Author] = Resolver(
    declarations=cast(DeclarationSet, {}),
    step=cast(BuildStep[Author], None),
    sequence=None,
)

r.name = 3  # should raise error
# reveal_type(r.doesnotexist)
# reveal_type(r.name)


@dataclass
class Article:
    title: str
    content: str

    author: Author


# class AuthorFactory(Factory):
#     class Meta:
#         model = Author
#
#     name = Faker("name")
#
#
# class ArticleFactory(Factory):
#     class Meta:
#         model = Article
#
#     title = Faker("sentence")
#     content = Faker("text")
#     author = SubFactory(AuthorFactory)
#
#
# article = ArticleFactory.create()
#
# author = AuthorFactory.create()
#
# reveal_type(article)
# reveal_type(author)
#
# article.title.split()
# article.content.split()
# article.author.name.split()
