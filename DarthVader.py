import requests


class StarWarsAPI:

    base_url = 'https://swapi.dev/api/'

    def get_all_characters(self):
        resource_url = 'people/'
        get_url = f'{self.base_url}{resource_url}'
        characters_name = (person['name'] for person in requests.get(get_url).json()['results'])
        return characters_name

    def get_index_character(self, character):
        index = list(self.get_all_characters()).index(character) + 1
        return index

    def get_movies_with_character(self, character):
        index_character = self.get_index_character(character)
        resource_url = f'people/{index_character}'
        get_url = f'{self.base_url}{resource_url}'
        json_result_character = requests.get(get_url).json()
        return (film_url for film_url in json_result_character['films'])

ch = StarWarsAPI()
print(ch.get_number_character('Darth Vader'))
