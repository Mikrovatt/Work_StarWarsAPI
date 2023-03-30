import requests


class StarWarsAPI:

    base_url = 'https://swapi.dev/api/'  # Базовая URL для API

    def __init__(self):

        """Получение списка персонажей всех эпизодов "Звездные войны"
        для возможности выбора любого героя по имени """

        resource_url = 'people/'
        get_url = f'{self.base_url}{resource_url}'
        result_get = requests.get(get_url)  # получение ссылки на первую страницу
        next_page = result_get.json()["next"]
        characters_name = [(int(p['url'].split('/')[-2]), p['name']) for p in result_get.json()['results']]

        while next_page is not None:  # Перебор всех страниц с персонажами
            result_get = requests.get(next_page)
            next_page = result_get.json()["next"]
            characters_name.extend([(int(p['url'].split('/')[-2]), p['name']) for p in result_get.json()['results']])

        self.characters_name = dict(characters_name)
        print('Список всех персонажей получен!')

    def get_characters(self):
        for k, v in self.characters_name.items():
            print(f'k: v')

    def get_index_character(self, character: str) -> int:
        """ Метод получения индекса персонажа в API """
        index = list(self.characters_name.keys())[list(self.characters_name.values()).index(character)]
        return index

    def get_films_with_character(self, character: str):
        """ Метод получения ссылок на фильмы в которых снимался заданный персонаж """
        index_character = self.get_index_character(character)
        resource_url = f'people/{index_character}'
        get_url = f'{self.base_url}{resource_url}'
        json_result_character = requests.get(get_url).json()
        film_with_character = (film_url for film_url in json_result_character['films'])
        print(f'Список фильмов с участием {character} получен!')
        return film_with_character

    def get_characters_into_film(self, film_url: str):
        """ Метод получения всех персонажей, задействованных в заданном фильме """
        json_result_get_film = requests.get(film_url).json()
        result_characters_in_film = json_result_get_film['characters']
        index_name_characters = (int(index.split('/')[-2]) for index in result_characters_in_film)
        name_characters_into_film = (self.characters_name[index] for index in index_name_characters)
        print(f'Список персонажей задействованных в эпизоде Star Wars {json_result_get_film["title"]} получен!')
        return name_characters_into_film


ch = StarWarsAPI()
person = 'Darth Vader'
films = ch.get_films_with_character(person)  # Получение фильмов с участием Darth Vader
result = set()

# Получение массива персонажей снявшихся в фильме с Darth Vader
for film in films:
    result = result.union(set(ch.get_characters_into_film(film)))

name_file = f'characters_with_{person}.txt'.replace(' ', '_')
with open(name_file, 'w', encoding='UTF-8') as file:
    for name in sorted(result):
        file.write(name+'\n')
print(f'Файл с персонажами участвующими в фильмах c {person} создан: {name_file}')

