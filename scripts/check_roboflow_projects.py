import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

api_key = 'Dbsq4wpnTVr9UkRb7YBj'
workspace = 'mes-workspace-02uvi'
url = f'https://api.roboflow.com/{workspace}?api_key={api_key}'

res = requests.get(url)
print('Status code:', res.status_code)
if res.status_code == 200:
    data = res.json()
    ws = data.get('workspace', {})
    print('Workspace name:', ws.get('name'))
    projects = ws.get('projects', [])
    print(f'Total projects: {len(projects)}')
    for p in projects:
        print(f"  - ID: {p.get('id')}, Name: {p.get('name')}, Type: {p.get('type')}, Images: {p.get('images')}")
else:
    print('Response:', res.text)
