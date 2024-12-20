# Hướng dẫn sử dụng API và chạy bài toán

## Cách dùng API

### Cài đặt thư viện

Cài đặt thư viện requests:

```bash
pip install requests
```

Sử dụng thư viện requests:

```python
import requests
```

### Tạo user

```python
data = {
    "username": USER_NAME,
    "password": PASSWORD
}
response = requests.post("https://procon.iuhkart.systems/auth/register", json=data)
print(response.status_code)
response.json()
```

### Lấy token và tạo headers

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

### Lấy đề

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

### Xem bài nộp

Endpoint: `https://procon.iuhkart.systems/answer/70?user_id=1`

```python
response = requests.get("https://procon.iuhkart.systems/answer/70", headers=headers)
print(response.status_code)
print(response.json())
```

## Hướng dẫn chạy bài toán

### Mô tả

Chương trình này được thiết kế để thực hiện các bước sau:
1. **Tải dữ liệu câu hỏi** từ API (`get_test_quest.py`).
2. **Chuyển đổi dữ liệu** từ định dạng JSON sang định dạng đầu vào TXT để C++ có thể đọc.
3. **Biên dịch và chạy giải pháp C++** để tìm lời giải.
4. **Gửi kết quả lời giải** qua API (`post_test_quest.py`).

### Thư mục cấu trúc

```plaintext
.
├── api/
│   ├── get_test_quest.py      
│   ├── post_test_quest.py     
├── solution/
│   ├── convert_txt.py         
│   ├── solution_beam_search.cpp
│   ├── solution_BFS.cpp  
│   ├── solution_BFS_binary_lifting.cpp
│   ├── solution_z_function.cpp
├── main.py          
├── requirements.txt       
├── README.md           
```

### Yêu cầu
- Python (phiên bản >= 3.9)
- Trình biên dịch `g++` hỗ trợ chuẩn C++20
- Hệ điều hành Windows (hoặc cần điều chỉnh đường dẫn trên Unix/Linux)

### Cách chạy

#### Cài đặt các thư viện yêu cầu

Trước khi chạy chương trình, hãy cài đặt các thư viện Python yêu cầu bằng cách sử dụng requirements.txt:

```bash
pip install -r requirements.txt
```

#### Chạy từng phần riêng lẻ

1. **Tải dữ liệu câu hỏi:**

```bash
python ./api/get_test_quest.py --question_id <id>
```
##### Ví dụ

```bash
python ./api/get_test_quest.py --question_id 75
```

2. **Chuyển đổi dữ liệu:**

```bash
python ./solution/convert_txt.py --question_id <id>
```
##### Ví dụ

```bash
python ./solution/convert_txt.py --question_id 75
```

3. **Biên dịch và chạy giải pháp C++:**

```bash
g++ -std=c++20 -o solution/solution_z_function.exe solution/solution_z_function.cpp
solution/solution_z_function.exe <id>
```
##### Ví dụ

```bash
g++ -std=c++20 -o solution/solution_z_function.exe solution/solution_z_function.cpp
solution/solution_z_function.exe 75
```

4. **Gửi kết quả lời giải:**

```bash
python ./api/post_test_quest.py --question_id <id>
```
##### Ví dụ

```bash
python ./api/post_test_quest.py --question_id 75
```

### Chạy tất cả các bước

Để chạy toàn bộ các bước tự động, sử dụng file main.py:

```bash
python main.py --solution <solution_type> --question_id <id>
```
##### Ví dụ

```bash
python main.py --solution z_function --question_id 75
```

##### Các loại giải pháp có thể sử dụng:
- z_function
- BFS
- BFS_binary_lifting
- beam_search

