from requests import get
from requests import delete
from requests import post

print(get('http://localhost:8008/api/v2/users').json())
print(get('http://localhost:8008/api/v2/users/2').json())
print(get('http://localhost:8008/api/v2/users/-1').json())  # нет пользователя
print(get('http://localhost:8008/api/v2/users/q').json())  # не число

print(delete('http://localhost:8008/api/v2/users/1').json())  # id = 999 нет в базе
print(delete('http://localhost:8008/api/v2/users/10').json())

print(post('http://localhost:8008/api/v2/users').json())  # нет словаря
print(post('http://localhost:8008/api/v2/users', json={'name': 'Ваня'}).json())  # не все поля
print(post('http://localhost:8008/api/v2/users', json={'name': 'FFFF', 'position': 'кок',
                                                       'surname': 'Иванов', 'age': 17, 'address': 'module_3',
                                                       'speciality': 'прог',
                                                       'hashed_password': '123', 'email': '1234@mars.org'}).json())
