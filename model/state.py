from dataclasses import dataclass, field

@dataclass()
class State:
    id: str
    name: str
    capital: str
    lat: float
    lng: float
    area: float
    population: int
    neighbors: list= field(default_factory=list) #è una lista che corrisponde a quello specifico oggetto stato

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)
