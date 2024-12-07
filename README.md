# Hướng dẫn sử dụng

## 1. Sao chép dữ liệu vào `input.json`

Để chạy chương trình, bạn cần sao chép dữ liệu JSON của bạn vào file `input.json`. Đảm bảo rằng file `input.json` có cấu trúc đúng theo yêu cầu của chương trình.

Ví dụ: 

```json
{
    "board": {
        "width": 7,
        "height": 6,
        "start": [
            [1, 0, 1, 1, 2, 2, 1],
            [2, 3, 1, 1, 0, 0, 2],
            [3, 0, 2, 1, 1, 1, 1],
            [3, 0, 0, 2, 2, 3, 1],
            [2, 2, 3, 2, 0, 2, 2],
            [3, 3, 1, 0, 3, 2, 3]
        ],
        "goal": [
            [1, 0, 1, 1, 2, 2, 1],
            [2, 3, 1, 1, 0, 0, 2],
            [3, 0, 1, 1, 1, 1, 2],
            [3, 0, 2, 3, 1, 0, 2],
            [2, 2, 0, 2, 2, 2, 3],
            [3, 3, 1, 0, 3, 2, 3]
        ]
    },
    "general": {
        "n": 1,
        "patterns": [
            {
                "p": 25,
                "width": 3,
                "height": 3,
                "cells": [
                    [0, 1, 0],
                    [1, 0, 1],
                    [1, 1, 0]
                ]
            }
        ]
    }
}
```

Tham khảo ma trận 256x256: https://drive.google.com/file/d/1DQiXZ4Y9KZFBqtFPfbpkCzalp699YAzl/view?usp=sharing
    
## 2. Biên dịch và chạy file C++

### **Cách 1: Chạy `solution_BFS.cpp`**

```bash
g++ -o solution_BFS solution_BFS.cpp && ./solution_BFS
```

### **Cách 2: Chạy `solution_BFS_binary_lifting.cpp`**

```bash
g++ -o solution_BFS_binary_lifting solution_BFS_binary_lifting.cpp && ./solution_BFS_binary_lifting
```

### **Cách 3: Chạy `solution_beam_search.cpp`**

```bash
g++ -o solution_beam_search solution_beam_search.cpp && ./solution_beam_search
```
g++ -std=c++20 -o solution_z_function solution_z_function.cpp && ./solution_z_function
## 3. Kết quả 

Sau khi chạy chương trình, các bước di chuyển sẽ được xuất ra file output.json.