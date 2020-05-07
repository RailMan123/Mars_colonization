from requests import get, post, delete
from werkzeug.security import generate_password_hash
import datetime

# ПРАВИЛЬНЫЙ ЗАПРОС НА ДОБАВЛЕНИЕ НОВОГО УЧАСТНИКА
print(post('http://localhost:5000/api/v2/users',
           json={   'id': 5,
                    'email': 'admin@mail.ru',
                    'name': 'Main',
                    'surname': 'Captain',
                    'about': 'Great colonizator',
                    'age': 42,
                    'position': 'Captain',
                    'speciality': 'Shturman',
                    'address': 'module_42',
                    'hashed_password': generate_password_hash('password_cap'),
                    'city_from': 'Rim'}).json())

# ID ДОЛЖЕН БЫТЬ БОЛЬШЕ 0, ПАРАМЕТР age ДОЛЖЕН БЫТЬ ЧИСЛОМ
print(post('http://localhost:5000/api/v2/users',
           json={   'id': -1,
                    'email': 'ww@ww',
                    'name': 'Second',
                    'surname': 'Officer',
                    'about': 'Talantly person',
                    'age': "pp",
                    'position': 'Serjant',
                    'speciality': 'Guardian',
                    'address': 'module_33',
                    'hashed_password': generate_password_hash('password_serj'),
                    'city_from': 'Iran'}).json())


# ПРАВИЛЬНЫЙ ЗАПРОС НА ПОЛУЧЕНИЕ ВСЕХ УЧАСТНИКОВ
print(get('http://localhost:5000/api/v2/users').json())

# ПРАВИЛЬНЫЙ ЗАПРОС НА ПОЛУЧЕНИЕ ОДНОГО УЧАСТНИКА
print(get('http://localhost:5000/api/v2/users/1').json())

# ТАКОГО УЧАСТНИКА НЕТ В БАЗЕ
print(get('http://localhost:5000/api/v2/users/999').json())

# НЕПРАВИЛЬНЫЙ ПАРАМЕТР
# print(get('http://localhost:5000/api/v2/users/-1').json())

# ПРАВИЛЬНЫЙ ЗАПРОС НА РЕДАКТИРОВАНИЕ УЧАСТНИКА
print(post('http://localhost:5000/api/v2/users/1',
           json={   'id': 2,
                    'email': 'admin@mail.ru',
                    'name': 'Main',
                    'surname': 'Captain',
                    'about': 'Great colonizator',
                    'age': 43,
                    'position': 'Captain',
                    'speciality': 'Shturman',
                    'address': 'module_44',
                    'hashed_password': generate_password_hash('password_cap'),
                    'city_from': 'Rim'}).json())

# ID КАПИТАНА СТАЛО 2, А ЗНАЧИТ УЧАСТНИКА С ID 1 НЕ СУЩЕСТВУЕТ
print(post('http://localhost:5000/api/v2/users/1',
           json={   'id': 3,
                    'email': 'admin@mail.ru',
                    'name': 'NOT Main',
                    'surname': 'NOT Captain',
                    'about': 'NOT Great colonizator',
                    'age': 43,
                    'position': 'Captain',
                    'speciality': 'Shturman',
                    'address': 'module_44',
                    'hashed_password': generate_password_hash('password_cap'),
                    'city_from': 'Rim'}).json())

# ID ДОЛЖЕН БЫТЬ > 0 (ЕСТЬ ПРОВЕРКА), age ДОЛЖЕН БЫТЬ ЧИСЛОМ
print(post('http://localhost:5000/api/v2/users/2',
           json={   'id': -1,
                    'email': 'admin@mail.ru',
                    'name': 'NOT Main',
                    'surname': 'NOT Captain',
                    'about': 'NOT Great colonizator',
                    'age': 'pp',
                    'position': 'Captain',
                    'speciality': 'POVARR',
                    'address': 'module_44',
                    'hashed_password': generate_password_hash('password_cap'),
                    'city_from': 'Rim'}).json())

# ПРАВИЛЬНЫЙ ЗАПРОС НА УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
print(delete('http://localhost:5000/api/v2/users/2').json())

# ПОПЫТКА УДАЛИТЬ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ :-D (МЕТОД НЕ ПРЕДУСМТОРЕН)
print(delete('http://localhost:5000/api/v2/users').json())

