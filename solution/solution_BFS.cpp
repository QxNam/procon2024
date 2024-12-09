#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <deque>
#include <map>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <array>
#include <chrono>
#include <cassert>
#include <filesystem>
#include<queue>


using namespace std;
#define ll int 
#define endl '\n'
#define sz(x) (ll)(x.size())
#define TOP 0 
#define BOTTOM 1 
#define LEFT 2 
#define RIGHT 3 

ll width, height, n;
vector<string> start, goal;
vector<tuple<ll, ll, ll, vector<string>>> dies;  //id, width, height, matrix 
ll dist[256][256], dx[]={0, 0, -1, 1}, dy[]={1, -1, 0, 0};
ll Fixed[256][256];
vector<tuple<ll, ll, ll, ll>> answer;

// Hàm tạo khuôn Loại I
vector<string> createTypeI(ll n) {
    vector<string> matrix(n, string(n, '1'));  // Khởi tạo vector với n chuỗi, mỗi chuỗi có n ký tự '1'
    return matrix; 
}

// Hàm tạo khuôn Loại II
vector<string> createTypeII(int n) {
    vector<string> matrix(n, string(n, '0'));
    for (int i = 0; i < n; i += 2) {
        for (int j = 0; j < n; ++j) {
            matrix[i][j] = '1';
        }
    }
    return matrix;
}

// Hàm tạo khuôn Loại III
vector<string> createTypeIII(int n) {
    vector<string> matrix(n, string(n, '0'));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; j += 2) {
            matrix[i][j] = '1';
        }
    }
    return matrix;
}

// Hàm in ra ma trận 
void print_matrix(vector<string> matrix)
{
    for (string s: matrix) cout<<s<<endl;
    cout<<endl;
}

// Hàm khởi tạo các die cố định ban đầu 
void init_die()
{
    dies.push_back({0, 1, 1, createTypeI(1)});
    for (ll idx=1, i=2; i<=256; i*=2, idx+=1) {
        dies.push_back({idx, i, i, createTypeI(i)});
        dies.push_back({idx, i, i, createTypeII(i)});
        dies.push_back({idx, i, i, createTypeIII(i)});
    }
}

// Hàm nhập input đầu vào (đã chuyển từ file json sang txt)
void read_input()
{
    cin>>width>>height;
    for (ll i=0; i<height; i++) {
        string x; cin>>x;
        start.push_back(x);
    }
    for (ll i=0; i<height; i++) {
        string x; cin>>x;
        goal.push_back(x);
    }
    cin>>n;
    for (ll i=0; i<n; i++){
        ll id, w, h; cin>>id>>w>>h;
        vector<string> pattern;
        for (ll j=0; j<h; j++) {
            string s; cin>>s;
            pattern.push_back(s);
        }
        dies.push_back({id, w, h, pattern});
    }
}

vector<string> apply_die(ll id, ll x, ll y, int direction, vector<string> board) {
    auto [_, w, h, pattern] = dies[id]; // id, width, height, matrix (pattern)

    if (direction==LEFT) {
        // Nhấc khuôn tại vị trí (x, y)
        for (ll i = 0; i < h; i++) {
            ll board_x = x + i;
            if (board_x >= 0 && board_x < height) {
                deque<char> lifted_elements;
                string new_row;
                for (ll j = 0; j < w; j++) {
                    ll board_y = y + j;

                    // Nếu phần này nằm trong bảng và có giá trị '1' trong khuôn
                    if (board_y >= 0 && board_y < width) {
                        if (pattern[i][j] == '1') {
                            lifted_elements.push_back(board[board_x][board_y]);
                            board[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                        }
                    }
                }
                for (ll board_y=0; board_y<width; board_y++) if (board[board_x][board_y]!='.') new_row.push_back(board[board_x][board_y]);
                while (!lifted_elements.empty()) {
                    ll x=lifted_elements.front(); 
                    lifted_elements.pop_front();
                    new_row.push_back(x);
                }
                board[board_x]=new_row;
            }
        }
    }
    else if (direction==RIGHT) {
        // Nhấc khuôn tại vị trí (x, y)
        for (ll i = 0; i < h; i++) {
            ll board_x = x + i;
            if (board_x >= 0 && board_x < height) {
                deque<char> lifted_elements;
                for (ll j = 0; j < w; j++) {
                    ll board_y = y + j;

                    // Nếu phần này nằm trong bảng và có giá trị '1' trong khuôn
                    if (board_y >= 0 && board_y < width) {
                        if (pattern[i][j] == '1') {
                            lifted_elements.push_back(board[board_x][board_y]);
                            board[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                        }
                    }
                }
                string new_row;
                while (!lifted_elements.empty()) {
                    ll x=lifted_elements.front(); 
                    lifted_elements.pop_front();
                    new_row.push_back(x);
                }
                for (ll board_y=0; board_y<width; board_y++) if (board[board_x][board_y]!='.') new_row.push_back(board[board_x][board_y]);
                board[board_x]=new_row;
            }
        }
    }
    else if (direction==TOP) {
        // Nhấc khuôn tại vị trí (x, y)
        for (ll j = 0; j < w; j++) {
            ll board_y = y + j;
            if (board_y >= 0 && board_y < width) {
                deque<char> lifted_elements;
                for (ll i = 0; i < h; i++) {
                    ll board_x = x + i;

                    // Nếu phần này nằm trong bảng và có giá trị '1' trong khuôn
                    if (board_x >= 0 && board_x < height) {
                        if (pattern[i][j] == '1') {
                            lifted_elements.push_back(board[board_x][board_y]);
                            board[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                        }
                    }
                }
                string new_col;
                for (ll board_x=0; board_x<height; board_x++) if (board[board_x][board_y]!='.') new_col.push_back(board[board_x][board_y]);
                while (!lifted_elements.empty()) {
                    ll x=lifted_elements.front(); 
                    lifted_elements.pop_front();
                    new_col.push_back(x);
                }
                for (ll board_x=0; board_x<height; board_x++) board[board_x][board_y]=new_col[board_x];
            }
        }
    }
    else {
        // Nhấc khuôn tại vị trí (x, y)
        for (ll j = 0; j < w; j++) {
            ll board_y = y + j;
            if (board_y >= 0 && board_y < width) {
                deque<char> lifted_elements;
                for (ll i = 0; i < h; i++) {
                    ll board_x = x + i;

                    // Nếu phần này nằm trong bảng và có giá trị '1' trong khuôn
                    if (board_x >= 0 && board_x < height) {
                        if (pattern[i][j] == '1') {
                            lifted_elements.push_back(board[board_x][board_y]);
                            board[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                        }
                    }
                }
                string new_col;
                while (!lifted_elements.empty()) {
                    ll x=lifted_elements.front(); 
                    lifted_elements.pop_front();
                    new_col.push_back(x);
                }
                for (ll board_x=0; board_x<height; board_x++) if (board[board_x][board_y]!='.') new_col.push_back(board[board_x][board_y]);
                for (ll board_x=0; board_x<height; board_x++) board[board_x][board_y]=new_col[board_x];
            }
        }
    }

    return board;
}

pair<ll, ll> bfs(ll curx, ll cury)
{
    if (start[curx][cury]==goal[curx][cury]) return {curx, cury};
    for (ll i=0; i<height; i++)
        for (ll j=0; j<width; j++)
            dist[i][j]=-1;
    queue<pair<ll, ll>> q;
    q.push({curx, cury});
    dist[curx][cury]=0;
    while (!q.empty())
    {
        auto [x, y]=q.front(); q.pop();
        for (ll i=0; i<4; i++) 
        {
            ll newx=x+dx[i], newy=y+dy[i];
            if (0<=newx && newx<height && 0<=newy && newy<width && dist[newx][newy]==-1 && Fixed[newx][newy]==0)
            {
                if (start[newx][newy]==goal[curx][cury]) return {newx, newy};
                q.push({newx, newy});
                dist[newx][newy]=dist[x][y]+1;
            } 
        }
    }
    return {curx, cury};
}

vector<tuple<ll, ll, ll, ll>> apply_bfs(vector<string> &start, bool is_debug=false)
{
    vector<tuple<ll, ll, ll, ll>> answer;
    for (ll i=0; i<height; i++)
    {
        for (ll j=0; j<width; j++) 
        {
            auto [x, y]=bfs(i, j);
            // cout<<"[i, j   x, y  ]: "<<i<<" "<<j<<"    "<<x<<" "<<y<<"   "<<endl;
            while (y<j) 
            {
                if (is_debug) cout<<"[direction, id, x, y]:   RIGHT "<<0<<" "<<x<<" "<<y+1<<" "<<endl;
                start=apply_die(0, x, y+1, RIGHT, start);
                answer.push_back({0, y+1, x, RIGHT});
                ++y;
                // print_matrix(start);
            }
            while (y>j)
            {
                if (is_debug) cout<<"[direction, id, x, y]:   LEFT "<<0<<" "<<x<<" "<<y-1<<" "<<endl;
                start=apply_die(0, x, y-1, LEFT, start);
                answer.push_back({0, y-1, x, LEFT});
                --y;
                // print_matrix(start);
            }
            while (x<i)
            {
                if (is_debug) cout<<"[direction, id, x, y]:   BOTTOM "<<0<<" "<<x+1<<" "<<y<<" "<<endl;
                start=apply_die(0, x+1, y, BOTTOM, start);
                answer.push_back({0, y, x+1, BOTTOM});
                ++x;
                // print_matrix(start);
            }
            while (x>i) 
            {
                if (is_debug) cout<<"[direction, id, x, y]:   TOP "<<0<<" "<<x-1<<" "<<y<<" "<<endl;
                start=apply_die(0, x-1, y, TOP, start);
                answer.push_back({0, y, x-1, TOP});
                --x;
                // print_matrix(start);
            }
            Fixed[i][j]=1;
        }
    }
    return answer;
}

// Hàm in JSON từ vector<tuple<ll, ll, ll, ll>>
void print_answer(const vector<tuple<ll, ll, ll, ll>> &answer, string question_id)
{
    // Mở file để ghi
    filesystem::create_directories("data\\output");
    ofstream outFile("data\\output\\output_"+question_id+".json");
    if (!outFile.is_open())
    {
        cerr << "Không thể mở file để ghi!" << endl;
        return;
    }

    // Bắt đầu chuỗi JSON
    outFile << "{" << endl;
    outFile << "  \"n\":" << answer.size() << "," << endl;
    outFile << "  \"ops\":[" << endl;

    // Duyệt qua từng phần tử trong vector và xây dựng chuỗi JSON
    for (size_t i = 0; i < answer.size(); ++i)
    {
        auto [p, x, y, s] = answer[i];
        outFile << "    {" << endl;
        outFile << "      \"p\":" << p << "," << endl;
        outFile << "      \"x\":" << x << "," << endl;
        outFile << "      \"y\":" << y << "," << endl;
        outFile << "      \"s\":" << s << endl;
        outFile << "    }";

        // Thêm dấu phẩy trừ phần tử cuối cùng
        if (i != answer.size() - 1)
            outFile << ",";
        outFile << endl;
    }

    // Kết thúc chuỗi JSON
    outFile << "  ]" << endl;
    outFile << "}" << endl;

    // Đóng file
    outFile.close();
    cerr << "Data successfully written to data\\output\\output_"+question_id+".json" << endl;
}

void solve(string question_id) {
    init_die();
    read_input();
    answer=apply_bfs(start, 0);
    print_matrix(start);
    print_answer(answer, question_id);
}

int main(int argc, char* argv[])
{
    if (argc != 2) {
        cerr << "Used argument: " << argv[0] << " <question_id>" << endl;
        return 1; // Thoát với mã lỗi
    }

    // Đọc file input_{id}.txt và ghi kết quả ra file output_{id}.txt
    string question_id = argv[1];
    string input_file = "data\\input\\input_" + question_id + ".txt";
    string output_file = "data\\output\\output_" + question_id + ".txt";

    ios_base::sync_with_stdio(false); cin.tie(NULL);
    #ifndef ONLINE_JUDGE
    freopen(input_file.c_str(), "r", stdin);
    freopen(output_file.c_str(), "w", stdout);
    #endif

    clock_t start2 = clock();
    solve(question_id);
    clock_t end2 = clock();
    double duration2 = double(end2 - start2) / CLOCKS_PER_SEC;
    cerr << "Time find solution: " << duration2 << " seconds" << endl;
    return 0;
}