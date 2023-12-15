from pwinput import pwinput
from typing import Union, Callable, Tuple, List

import database
import movie
import user

    
class Program:
    def __init__(self) -> None:
        self.__database = database.Database.load_or_create()    
        self.__current_user :user.User = None
    
    def __input_user_type(self):
        while True:
            user_type = input("Enter user type: (n=normal user/r=reviewer)").lower()
            if user_type == 'n':
                return 'normal'
            if user_type == 'r':
                return 'reviewer'
            
            print("Can't recognize user type!")
    
    def __input_genre(self) -> str:
        while True:
            self.__print_genres()
            genre = input('Enter genre')
            if genre.isdigit():
                genre = int(genre)
                if 0 <= genre < len(movie.Movie.supported_genres):
                    return movie.Movie.supported_genres[genre] 
                
            print("Can't recognize genre!")
    
    def __input_new_movie(self) -> Tuple[str, str, List[str]]:
        movie_name = input("Enter movie name:")
        while True:
            movie_genre = input(f"Enter movie genre {movie.Movie.supported_genres}:").lower()
            if movie_genre in movie.Movie.supported_genres:
                break
            print(f"genre must be one of {movie.Movie.supported_genres}.")
        director = input("Enter director name:")
        while True:
            n_actors = input("Enter number of actors:")
            if n_actors.isdigit():
                n_actors = int(n_actors)
                break
            print('Number of actors must be a number!')
        actors = [input(f"Enter actor name ({i}):") for i in range(n_actors)]
        return movie_name, movie_genre, director, actors
    
    def __print_menu(self) -> None:
        if self.__current_user.get_access_level("list_movies"):
            print('1. List all Movies.')
        if self.__current_user.get_access_level("list_actors"):
            print('2. List all Actors.')
        if self.__current_user.get_access_level("list_directors"):
            print('3. List all Directors.')
        if self.__current_user.get_access_level("list_movie_with_genre"):
            print('4. List all Movies with specific Genre.')
        if self.__current_user.get_access_level("search_movie"):
            print('5. Search one Movies with name.')
        if self.__current_user.get_access_level("search_actor"):
            print('6. Search one Actor with name.')
        if self.__current_user.get_access_level("search_director"):
            print('7. Search one Director with name.')
        if self.__current_user.get_access_level("add_movie"):
            print('8. Add new Movie.')
        print('0. Exit.')
        
    def __print_genres(self):
        for i, genre in enumerate(movie.Movie.supported_genres):
            print(f'{i}. {genre}.')
    
    def __create_new_user(self, username: str, password: str) -> Union[user.User, None]:
        print("Username does not exists!")
        while True:
            create_user = input("Do you want to create new user? (Y/n)").lower()
            if create_user == '' or create_user == 'y':
                user_type = self.__input_user_type()
                return self.__database.add_user(username, password, user_type)
            if create_user == 'n':
                return None
            print("Can't recognize command!")
        
    def __authenticate(self) -> None:
        while True:
            username = input("Username:")
            password = pwinput(mask='*')
            
            if username == '0' and password == '0':
                self.__database.store()
                exit()
            
            user = self.__database.login(username, password)
            if user is not None:
                print("Login successful.")
                self.__current_user = user
                return
            if self.__database.check_username(username):
                print("Wrong password! try again!")
                continue
            
            user = self.__create_new_user(username, password)
            if user is not None:
                print("User created.")
                self.__current_user = user
                return
    
    def __list_movies(self) -> None:
        print(self.__database.get_movies())
        
    def __list_actors(self) -> None:
        print(self.__database.get_actors())
        
    def __list_directors(self) -> None:
        print(self.__database.get_directors())
        
    def __list_movies_genre(self) -> None:
        genre = self.__input_genre()
        print(self.__database.get_movies_genre(genre))
        
    def __score_movie(self, movie: movie.Movie) -> None:
        while True:
            command = input("Do you want to score this movie? (Y/n):").lower()
            
            if command == 'n':
                return
            
            if command != '' and command != 'y':
                print("Can't recognize command!")
                continue
            
            raiting = input("Enter your score from 1 to 5:")
            if not raiting.isdigit():
                print("your score should be a number!")
                continue
            
            raiting = int(raiting)
            if not (0 < raiting <= 5):
                print("your score should be a number!")
                continue
            
            if self.__current_user.get_type() == 'normal':
                movie.add_user_raiting(raiting)
                break
            elif self.__current_user.get_type() == 'reviewer':
                movie.add_reviewer_raiting(raiting)
                break
            else:
                raise NotImplemented("User type not implemented!")
                
        
    def __search_movie(self) -> None:
        movie_name = input('Enter movie name:')
        movie = self.__database.search_movie(movie_name)
        if movie is None:
            print("Movie not found!")
            return
        print(movie)
        self.__score_movie(movie)
        
        
    def __search_actor(self) -> None:
        actor_name = input('Enter actor name:')
        actor = self.__database.search_actor(actor_name)
        if actor is None:
            print("Actor not found!")
        print(actor)
        
    def __search_director(self) -> None:
        director_name = input('Enter director name:')
        director = self.__database.search_director(director_name)
        if director is None:
            print("Director not found!")
        print(director)
    
    def __add_movie(self) -> None:
        movie_name, genre, director_name, actor_names = self.__input_new_movie()
        movie = self.__database.search_movie(movie_name)
        if movie is not None:
            print("This movie exists!")
            print(movie)
            return
        director = self.__database.search_director(director_name, create=True)
        actors = [self.__database.search_actor(actor_name, create=True) for actor_name in actor_names]
        movie = self.__database.add_movie(movie_name, genre, director, actors)
    
    def __get_action_function(self) -> Union[Callable, None]:
        while True:
            action = input('Enter a row number:')
            if action == '1' and self.__current_user.get_access_level("list_movies"):
                return self.__list_movies
            if action == '2' and self.__current_user.get_access_level("list_actors"):
                return self.__list_actors
            if action == '3' and self.__current_user.get_access_level("list_directors"):
                return self.__list_directors
            if action == '4' and self.__current_user.get_access_level("list_movie_with_genre"):
                return self.__list_movies_genre
            if action == '5' and self.__current_user.get_access_level("search_movie"):
                return self.__search_movie
            if action == '6' and self.__current_user.get_access_level("search_actor"):
                return self.__search_actor
            if action == '7' and self.__current_user.get_access_level("search_director"):
                return self.__search_director
            if action == '8' and self.__current_user.get_access_level("add_movie"):
                return self.__add_movie
            if action == '0':
                self.__current_user = None
                return None
            print("Can't recognize command!")
        
    
    def __program_loop(self):
        while True:
            self.__print_menu()
            action = self.__get_action_function()
            if action is None:
                break
            action()
    
    def run(self):
        while True:
            self.__authenticate()
            self.__program_loop()
