# Cách dùng API

Cài đặt thu viện requests:

```bash
pip install requests
```

Sử dụng thư viện requests:

```python
import requests
```

## Tạo user

```python
data = {
    "username": "a",
    "password": "1234"
}
response = requests.post("http://192.168.1.3:8000/auth/register", json=data)
print(response.status_code)
response.json()
```

## Lấy token và tạo headers

```python
headers = {
    "Authorization": None
}
response = requests.post("http://192.168.1.3:8000/auth/token", data=data)
if response.status_code == 201:
    token = response.json()['token']
    headers["Authorization"] = token

headers
```

## Lấy đề

Endpoint: `http://192.168.1.3:8000/question/<id>`

```python
response = requests.get("http://192.168.1.3:8000/question/70", headers=headers)
print(response.status_code)
print(response.json())
```

Endpoint: `http://192.168.1.3:8000/answer`

```python
import json
with open('70.json', 'r') as f:
    data = json.load(f)

response = requests.post("http://192.168.1.3:8000/answer", json=data, headers=headers)
print(response.status_code)
print(response.json())
```

## Xem bài nộp

Endpoint: `http://192.168.1.3:8000/answer/70?user_id=1`

```python
response = requests.get("http://192.168.1.3:8000/answer/70", headers=headers)
print(response.status_code)
print(response.json())
```
