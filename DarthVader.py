import requests


class StarWarsAPI:

    base_url = 'https://swapi.dev/api/'

    def __init__(self):
        resource_url = 'people/'
        get_url = f'{self.base_url}{resource_url}'
        result_get = requests.get(get_url)
        next_page = result_get.json()["next"]
        characters_name = [(int(p['url'].split('/')[-2]), p['name']) for p in result_get.json()['results']]

        while next_page is not None:
            result_get = requests.get(next_page)
            next_page = result_get.json()["next"]
            characters_name.extend([(int(p['url'].split('/')[-2]), p['name']) for p in result_get.json()['results']])

        self.characters_name = dict(characters_name)

    def get_index_character(self, character):
        index = list(self.characters_name.keys())[list(self.characters_name.values()).index(character)]
        return index

    def get_films_with_character(self, character):
        index_character = self.get_index_character(character)
        resource_url = f'people/{index_character}'
        get_url = f'{self.base_url}{resource_url}'
        json_result_character = requests.get(get_url).json()
        return (film_url for film_url in json_result_character['films'])

    def get_characters_into_film(self, film_url):
        result_characters_in_film = requests.get(film_url).json()['characters']
        index_name_characters = (int(index.split('/')[-2]) for index in result_characters_in_film)
        name_characters_into_film = (self.characters_name[index] for index in index_name_characters)
        return name_characters_into_film


ch = StarWarsAPI()
films = ch.get_films_with_character('Darth Vader')
result = set()
for film in films:
    result = result.union(set(ch.get_characters_into_film(film)))

print(result)
with open('person.txt', 'w', encoding='UTF-8') as file:
    pass

