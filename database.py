import os
import pickle
from typing import Union, List

import core
import movie
import user

class Database:
    @staticmethod
    def load_or_create():
        if os.path.exists('database.pickle'):
            with open('database.pickle', 'rb') as f:
                return pickle.load(f)
        return Database()
    
    def __init__(self) -> None:
        self.__moveis = movie.MovieList()
        self.__actors = core.NamedObjectList()
        self.__directors = core.NamedObjectList()
        self.__users = user.UserList()
        
    def login(self, username: str, password: str) -> Union[user.User, None]:
        return self.__users.login(username, password)

    def check_username(self, username: str) -> bool:
        return self.__users.check_username(username)
    
    def add_user(self, username: str, password: str, user_type: str) -> user.User:
        return self.__users.add_user(username, password, user_type)
    
    def store(self):
        with open('database.pickle', 'wb') as f:
            return pickle.dump(self, f)
        
    def get_movies(self) -> movie.MovieList:
        return self.__moveis
        
    def get_actors(self) -> core.NamedObjectList:
        return self.__actors
        
    def get_directors(self) -> core.NamedObjectList:
        return self.__directors
        
    def get_movies_genre(self, genre: str) -> None:
        return self.__moveis.filter_by_genre(genre)
        
    def search_movie(self, movie_name: str) -> Union[movie.Movie, None]:
        try:
            i = self.__moveis.index(movie_name)
        except ValueError:
            return None
        
        return self.__moveis[i]
        
    def search_actor(self, actor_name: str, create: bool = False) -> Union[movie.Movie, None]:
        try:
            i = self.__actors.index(actor_name)
        except ValueError:
            if not create:
                return None
            self.__actors.append(movie.Actor(actor_name))
            i = -1
        
        return self.__actors[i]
        
    def search_director(self, director_name: str, create: bool = False) -> Union[movie.Movie, None]:
        try:
            i = self.__directors.index(director_name)
        except ValueError:
            if not create:
                return None
            self.__directors.append(movie.Director(director_name))
            i = -1
        return self.__directors[i]
    
    def add_movie(self, movie_name: str, genre: str, director: movie.Director, actors: List[movie.Actor]) -> None:
        movie = self.__moveis.add_movie(movie_name, genre, director, actors)
        director.add_movie(movie)
        for actor in actors:
            actor.add_movie(movie)
        