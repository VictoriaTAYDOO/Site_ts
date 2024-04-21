from requests import delete

print(delete('http://localhost:8008/api/v2/users/1').json())  # id = 999 нет в базе
print(delete('http://localhost:8008/api/v2/users/10').json())