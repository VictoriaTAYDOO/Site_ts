from requests import get

print(get('http://localhost:8001/api/jobs').json())

print(get('http://localhost:8001/api/jobs/1').json())

print(get('http://localhost:8001/api/jobs/999').json())

print(get('http://localhost:8001/api/jobs/abc').json())