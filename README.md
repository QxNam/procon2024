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
    
## 2. Biên dịch và chạy file C++

### **Cách 1: Chạy `solution_BFS.cpp`**

1. Mở terminal hoặc command prompt tại thư mục dự án.
2. Biên dịch file C++:
    ```bash
    g++ solution_BFS.cpp -o solution_BFS
3. Chạy chương trình:
    ```bash
    ./solution_BFS

### **Cách 2: Chạy `solution_BFS_binary_lifting.cpp`**

1. Mở terminal hoặc command prompt tại thư mục dự án.
2. Biên dịch file C++:
    ```bash
    g++ solution_BFS_binary_lifting.cpp -o solution_BFS_binary_lifting
3. Chạy chương trình:
    ```bash
    ./solution_BFS_binary_lifting

## 3. Kết quả 

Sau khi chạy chương trình, các bước di chuyển sẽ được xuất ra file output.json.