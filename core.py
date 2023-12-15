from typing import List

class NamedObject:
    def __init__(self, name: str) -> None:
        assert isinstance(name, str), f"NamedObject can only take string names, {type(name)} was passed!"
        self.__name = name
        
    def get_name(self) -> str:
        return self.__name
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self.__name == value
        if isinstance(value, NamedObject):
            return self.__name == value.__name
        else:
            raise NotImplemented(f'NamedObject equality with {type(value)} is not implemented!')

    def __str__(self) -> str:
        return f'Name: {self.__name}'
    
    def __repr__(self) -> str:
        return f'NamedObject({str(self)})'
    

class NamedObjectList(list):
    def __init__(self, named_objects: List[NamedObject] = []) -> None:
        assert all(isinstance(named_object, NamedObject) for named_object in named_objects), f"NamedObjectList can only take Named_objects as internal list!"
        super().__init__(named_objects)

    def append(self, new_element: NamedObject):
        assert isinstance(new_element, NamedObject), f"NamedObjectList can only take Named_objects as internal list!"
        super().append(new_element)

    def __str__(self) -> str:
        if len(self) == 0:
            return "None"
        return "\t- " + "\n\t- ".join(map(lambda x: x.get_name(), self))
    
    def __repr__(self) -> str:
        return f'[{", ".join(map(lambda x: x.get_name(), self))}]'
    

class RatingManager:
    def __init__(self) -> None:
        self.__raitings = []

    def add_raiting(self, score: int) -> None:
        assert isinstance(score, int), "RatingManager can only take int as score!"
        self.__raitings.append(score)

    def get_average_raiting(self) -> float:
        if len(self.__raitings) == 0:
            return 0
        return sum(self.__raitings) / len(self.__raitings)
