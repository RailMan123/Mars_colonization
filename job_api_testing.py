from requests import get, post, delete
from werkzeug.security import generate_password_hash
import datetime

# ПРАВИЛЬНЫЙ ЗАПРОС НА ДОБАВЛЕНИЕ НОВОЙ РАБОТЫ
print(post('http://localhost:5000/api/v2/jobs',
           json={   'id': '10',
                    'team_leader': 2,
                    'job': 'digging digging cave',
                    'work_size': 400,
                    'collaborators': '1, 2, 3, 4',
                    'is_finished': False}).json())

# ID ДОЛЖЕН БЫТЬ БОЛЬШЕ 0, ПАРАМЕТР team_leader ДОЛЖЕН БЫТЬ ЧИСЛОМ,
#  ПАРАМЕТР is_finished ДОЛЖЕН БЫТЬ БУЛЕВЫМ ЗНАЧНИЕМ
print(post('http://localhost:5000/api/v2/jobs',
           json={   'id': '-10',
                    'team_leader': 'firstone',
                    'job': 'catching marsohod',
                    'work_size': 99,
                    'collaborators': '1, 2',
                    'is_finished': 'False'}).json())

# ПОПЫТКА ДОБАВИТЬ РАБОТУ С УЖЕ СУЩЕСТВУЮЩИМ ID
print(post('http://localhost:5000/api/v2/jobs',
           json={   'id': 10,
                    'team_leader': 1,
                    'job': 'fighting with inoprishlecz',
                    'work_size': 15,
                    'collaborators': '1, 2, 3, 4, 5',
                    'is_finished': False}).json())


# ПРАВИЛЬНЫЙ ЗАПРОС НА ПОЛУЧЕНИЕ ВСЕХ РАБОТ
print(get('http://localhost:5000/api/v2/jobs').json())

# ПРАВИЛЬНЫЙ ЗАПРОС НА ПОЛУЧЕНИЕ ОДНОЙ РАБОТЫ
print(get('http://localhost:5000/api/v2/jobs/10').json())

# ТАКОЙ РАБОТЫ НЕТ В БАЗЕ
print(get('http://localhost:5000/api/v2/jobs/999').json())

# НЕПРАВИЛЬНЫЙ ID
# print(get('http://localhost:5000/api/v2/jobs/-1').json())

# ПРАВИЛЬНЫЙ ЗАПРОС НА РЕДАКТИРОВАНИЕ РАБОТЫ (ID НЕ МЕНЯЕМ)
print(post('http://localhost:5000/api/v2/jobs/10',
           json={   'id': '10',
                    'team_leader': 2,
                    'job': 'digging digging cave',
                    'work_size': 400,
                    'collaborators': '1, 2, 3, 4',
                    'is_finished': True}).json())


# НЕ ВСЕ ПАРАМЕТРЫ
print(post('http://localhost:5000/api/v2/jobs/10',
           json={   'id': 20,
                    'team_leader': 2,
                    'work_size': 400,
                    'collaborators': '1, 2, 3, 4'}).json())

# ПРАВИЛЬНЫЙ ЗАПРОС НА УДАЛЕНИЕ РАБОТЫ
print(delete('http://localhost:5000/api/v2/jobs/10').json())

# ПОПЫТКА УДАЛИТЬ ВСЕ РАБОТЫ (МЕТОД НЕ ПРЕДУСМТОРЕН)
print(delete('http://localhost:5000/api/v2/users').json())

