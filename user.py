import hashlib
from typing import List, Union


class User:
    def __init__(self, username: str, password: str) -> None:
        assert isinstance(username, str), f"User can only take username as string, {type(username)} was passed!"
        assert isinstance(password, str), f"User can only take username as string, {type(password)} was passed!"
        self.__username = username
        self.__password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self._access_level = {}
        
    def get_access_level(self, level: str) -> bool:
        assert isinstance(level, str), "Access level must be string!"
        return self._access_level.get(level, False)
    
    def login(self, username: str, password: str) -> bool:
        assert isinstance(username, str), "username must be string!"
        assert isinstance(password, str), "password must be string!"
        if self.__username == username and self.__password == hashlib.md5(password.encode('utf-8')).hexdigest():
            return True
        else:
            return False

    def check_username(self, username) -> bool:
        assert isinstance(username, str), "username must be string!"
        if self.__username == username:
            return True
        else:
            return False

    def get_type(self):
        raise NotImplemented("Base user has no type!")
    
    def __str__(self) -> str:
        return f"User (username={self.__username})"
    
    def __repr__(self) -> str:
        return self.__str__()


class NormalUser(User):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password)
        self._access_level = {"list_movies": True, "list_actors": True, "list_directors": True,
                               "list_movie_with_genre": True,
                               "search_movie": True, "search_actor": True, "search_director": True,
                               'score': True, 'add_movie': False}
        
    def get_type(self) -> str:
        return "normal"
    

class ReviewerUser(User):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password)
        self._access_level = {"list_movies": True, "list_actors": True, "list_directors": True,
                               "list_movie_with_genre": True,
                               "search_movie": True, "search_actor": True, "search_director": True,
                               'score': True, 'add_movie': True}
        
    def get_type(self) -> str:
        return "reviewer"


class UserFactory:
    @staticmethod
    def make_new_user(username: str, password: str, user_type: str):
        assert isinstance(user_type, str), 'User type must be string!'
        if user_type == 'normal':
            return NormalUser(username, password)
        if user_type == 'reviewer':
            return ReviewerUser(username, password)
        raise NotImplemented(f"User type {user_type} is not implemented!")


class UserList(list):
    def __init__(self, users: List[User] = []) -> None:
        assert all(isinstance(users, User) for user in users), f"UserList can only take User as internal list!"
        super().__init__(users)

    def append(self, new_element: User):
        assert isinstance(new_element, User), f"UserList can only take User as internal list!"
        super().append(new_element)

    def add_user(self, username: str, password: str, user_type: str) -> User:
        new_user = UserFactory.make_new_user(username, password, user_type)
        self.append(new_user)
        return new_user

    def check_username(self, username: str) -> bool:
        return any([user.check_username(username) for user in self])
    
    def login(self, username: str, password: str) -> Union[User, None]:
        correct_users = list(filter(lambda x: x.login(username, password), self))
        if len(correct_users) == 0:
            return None
        if len(correct_users) == 1:
            return correct_users[0]
        raise Exception("Duplicated username and password!")
