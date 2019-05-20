import json

class Movie:

    def __init__(self, name, url, actors, box_office,year):
        self.name = name
        self.url = url
        self.actors = actors
        self.box_office = box_office
        self.year = year

    def to_dict (self):
        movie_as_dict = {
            # All Actors should have json_class of "Actor"
            "json_class": "Movie",
            "name": self.name,
            "url": self.url,
            "actors": self.actors,
            "box_office": self.box_office,
            "year": self.year,
        }
        return movie_as_dict

    def get_name(self):
        return self.name

    def to_json(self):
        return json.dumps(self.movie_to_dict())
