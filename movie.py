from typing import List

import core


class Movie:
    pass


class Artist(core.NamedObject):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.__movies = core.NamedObjectList()
    
    def add_movie(self, movie: Movie):
        assert isinstance(movie, Movie), f"Artist add_movie only takes Movie object, {type(movie)} was passed!"
        return self.__movies.append(movie)
    
    def __str__(self):
        return super().__str__() + f"\nMovies: \n{self.__movies}"

    def __repr__(self) -> str:
        return f'Artist({super().__str__()})'


class Actor(Artist):
    def __str__(self):
        return super().__str__().replace('Movies:', 'Acted in movies:', 1)
    
    def __repr__(self) -> str:
        return super().__repr__().replace('Artist', 'Actor', 1)


class Director(Artist):
    def __str__(self):
        return super().__str__().replace('Movies:', 'Directed movies:')
    
    def __repr__(self) -> str:
        return super().__repr__().replace('Artist', 'Director', 1)


class Movie(core.NamedObject):
    supported_genres = ['action', 'comedy', 'drama', 'horror', 'sci-fi']
    def __init__(self, name: str, genre: str, director: Artist, actors: List[Artist]) -> None:
        super().__init__(name)
        
        assert isinstance(genre, str), f"Movie can only take genre as string, {type(name)} was passed!"
        self.__genre = genre
        
        assert isinstance(director, Artist), f"Movie can only take Artist as director, {type(name)} was passed!"
        assert all(isinstance(actor, Artist) for actor in actors), f"Movie can only take Artist as director!"
        self.__director = director
        self.__actors = core.NamedObjectList(actors)

        self.__user_rating_manager = core.RatingManager()
        self.__reviewer_rating_manager = core.RatingManager()
        
    def get_genre(self) -> str:
        return self.__genre
    
    def is_genre(self, genre: str) -> bool:
        return self.__genre == genre
    
    def __str__(self) -> str:
        ret = super().__str__() + '\n'
        ret += f"Genre: {self.__genre}\n"
        ret += f"Director: {self.__director.get_name()}\n"
        ret += f"Actors:{self.__actors}\n"
        ret += f"Reviers raiting: {self.__reviewer_rating_manager.get_average_raiting()}\n"
        ret += f"Users raiting: {self.__user_rating_manager.get_average_raiting()}"
        return  ret
    
    def __repr__(self) -> str:
        return f'Movie({super().__str__()})'
    
    def add_user_raiting(self, score: float) -> None:
        self.__user_rating_manager.add_raiting(score)
        
    def get_user_average_raiting(self, score: float) -> None:
        self.__user_rating_manager.get_average_raiting()
        
    def add_reviewer_raiting(self, score: float) -> None:
        self.__reviewer_rating_manager.add_raiting(score)
        
    def get_reviewer_average_raiting(self, score: float) -> None:
        self.__reviewer_rating_manager.get_average_raiting()
    
    def __eq__(self, value: object) -> bool:
        return super().__eq__(value)
        
        
class MovieList(core.NamedObjectList):
    def add_movie(self, name: str, genre: str, director: Artist, actors: List[Artist]) -> Movie:
        new_movie = Movie(name, genre, director, actors)
        self.append(new_movie)
        return new_movie

    def filter_by_genre(self, genre: str):
        assert isinstance(genre, str), "Genre must be string!"
        assert genre in Movie.supported_genres, 'Genre is not supported'
        return MovieList([movie for movie in self if movie.is_genre(genre)])
