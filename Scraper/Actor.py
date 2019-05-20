import json

class Actor:
    def __init__(self, name, movies):
        self.name = name
        self.movies = movies

    def to_dict(self):
        actor_as_dict = {
            # All Actors should have json_class of "Actor"
            "json_class": "Actor",
            "name": self.name,
            "movies": self.movies,
        }
        return actor_as_dict

    def get_name(self):
        return self.name

    def to_json(self):
        return json.dumps(self.actor_to_dict())
