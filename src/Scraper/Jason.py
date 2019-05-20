import json


##########################
# Hard code way of creating an actor dictionary, then creating JSON format
actor1 = {
    "Bruce Willis": {
        "json_class": "Actor",
        "name": "Bruce Willis",
        "age": 61,
        "movies": [
            "The First Deadly Sin",
            "The Verdict",
        ]
    }
}


actor1_serialized = json.dumps(actor1)
# You probably need to save the json to a file
print("Here is the hard code data")
print(actor1_serialized)

##########################
# OOP way of creating actor class, and generating a JSON format from it


class Actor:
    def __init__(self, a_name, a_age, a_movies):
        self.name = a_name
        self.age = a_age
        self.movies = a_movies

    def toDict (self):
        dataDict = {
            # All Actors should have json_class of "Actor"
            "json_class": "Actor",
            "name": self.name,
            "age": self.age,
            "movies": self.movies,
        }
        return dataDict

    def getName(self):
        return self.name

    def toJsonString(self):
        return json.dumps(self.toDict())



BruceWillisActorObject = Actor("Bruce Willis", 61, ["The First Deadly Sin", "The Verdict",])
print
print
print("Here is the output from toJsonString")
print(BruceWillisActorObject.toJsonString())


# Overview of how to use this actor class:
"""
myWholeJsonDict = {}


For each piece of actor data that you mined:
    currActorObject = Actor(<put in the appropriate data>)

    myWholeJsonDict[currActorObject.getName()] = currActorObject.toDict()

# Write to file. Google for file.open()
file.write(json.dumps(myWholeJsonDict))

"""



'''

    #find_name('https://en.wikipedia.org/wiki/Chris_Hemsworth')
    # movie = get_movie_page_data('https://en.wikipedia.org/wiki/Avengers:_Infinity_War')
    # print(movie[0])
    # print(movie[1])


    # actors_to_process = []
    # scraped_movies = {}
    #
    # movie_url = 'https://en.wikipedia.org/wiki/Avengers:_Infinity_War'
    #
    # movie_page_data = get_movie_page_data(movie_url)  # to return list of actor name, age, movies
    # if (movie_page_data is not None):
    #     actors_to_process += movie_page_data[2]
    #     movie = Movie.Movie(movie_page_data[0], movie_url, movie_page_data[1])
    #     scraped_movies[movie.get_name()] = movie.to_json()
    #
    # print(movie_page_data[0])
    # print(movie_page_data[1])
    # print(movie_page_data[2])
    # print(scraped_movies)


    # movies_to_process = []
    # scraped_actors = {}
    # 
    # actor_url = '/wiki/Jesse_Eisenberg'
    # print(actor_url)
    # 
    # if ('https://' in actor_url):
    #     logging.warning("This is not a valid URL")
    # 
    # actor_page_data = get_actor_page_data('https://en.wikipedia.org' + actor_url)  # to return list of actor name, age, movies
    # if (actor_page_data is not None):
    #     movies_to_process += actor_page_data[2]
    #     actor = Actor.Actor(actor_page_data[0], actor_page_data[1])
    #     #scraped_actors.append(actor)
    #     scraped_actors[actor.get_name()] = actor.to_json()
    # 
    # print(actor_page_data[0])
    # print(actor_page_data[1])
    # print(actor_page_data[2])
    # print(scraped_actors)
    
    
    
    # movie = []
    # actor = []

    # movie['NameMovie1'] = Movie.Movie('Test movie name', 'Sampleurl.com', ['actor 1', 'actor 2']).to_dict()
    # actor["NameActor1"] = Actor.Actor("Test actor name", ["movie 1", "movie 2"]).to_dict()
    # movie.append(Movie.Movie('Test movie name', 'Sampleurl.com', ['actor 1', 'actor 2']))
    # actor.append(Actor.Actor("Test actor name", ["movie 1", "movie 2"]))
    #
    # all = {}
    # for m in movie:
    #     all[m.get_name()] = m.to_dict()
    #
    # for a in actor:
    #     all[a.get_name()] = a.to_dict()
    #
    # print(all)
    #
    # with open('data.json', 'w') as outfile:
    #     json.dump(all, outfile, indent=2)

    # dict = combine_dicts(movie, actor)
    # print(dict)
    # f = open("data.json", "a")
    # f.write(json.dumps(movie))
    #movie = json.dumps(movie)
    # f = open("dict.json", "w")
    # f.write(json.dumps(movie))
    # f.close()

    # with open('testdata.json', 'w') as outfile:
    #     json.dump(movie, outfile, indent=2)


'''