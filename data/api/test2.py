from requests import get, post

print(post('http://localhost:8014/api/jobs',
           json={'id': 3, 'job': 'installing a long-distance communication antenna', 'team_leader': 1, 'work_size': 5,
                 'collaborators': '6, 3', 'is_finished': True}).json())

print(post('http://localhost:8014/api/jobs', json={}).json())

print(post('http://localhost:8014/api/news',
           json={'job': '!!!'}).json())


print(get('http://localhost:8014/api/jobs').json())