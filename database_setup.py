import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Patrons(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    book_count = Column(Integer, nullable = False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'book_count': self.book_count,
        }

class Genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
        }

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key = True)
    title = Column(String(250), nullable = False)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship(Genres)
    summary = Column(String(500))
    author_id = Column(Integer, ForeignKey('authors.id'))
    authors = relationship(Authors)
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    patrons = relationship(Patrons)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'genre_id': self.genre_id,
            'summary': self.summary,
            'author_id': self.author_id,
            'patron_id': self.patron_id,
        }


engine = create_engine('sqlite:///librarycatalog.db')

Base.metadata.create_all(engine)

print "Database created"
