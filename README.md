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
    "username": USER_NAME,
    "password": PASSWORD"
}
response = requests.post("https://procon.iuhkart.systems/auth/register", json=data)
print(response.status_code)
response.json()
```

## Lấy token và tạo headers

```python
headers = {
    "Authorization": None
}
response = requests.post("https://procon.iuhkart.systems/auth/token", data=data)
if response.status_code == 201:
    token = response.json()['token']
    headers["Authorization"] = token

headers
```

## Lấy đề

Endpoint: `https://procon.iuhkart.systems/question/<id>`

```python
response = requests.get("https://procon.iuhkart.systems/question/70", headers=headers)
print(response.status_code)
print(response.json())
```

Endpoint: `https://procon.iuhkart.systems/answer`

```python
import json
with open('70.json', 'r') as f:
    data = json.load(f)

response = requests.post("https://procon.iuhkart.systems/answer", json=data, headers=headers)
print(response.status_code)
print(response.json())
```

## Xem bài nộp

Endpoint: `https://procon.iuhkart.systems/answer/70?user_id=1`

```python
response = requests.get("https://procon.iuhkart.systems/answer/70", headers=headers)
print(response.status_code)
print(response.json())
```
