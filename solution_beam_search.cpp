#include <bits/stdc++.h>
using namespace std;
#define ll long long
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
vector<array<ll, 4>> answer;

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

// Hàm áp dụng die cutting của die thứ id vào vị trí (x, y), hướng là direction={TOP, BOTTOM, LEFT, RIGHT}
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

//Hàm tìm vị trí ô đúng gần nhất với ô (curx, cury)
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
                if (start[newx][newy]==goal[curx][cury]) 
                    return {newx, newy};
                q.push({newx, newy});
                dist[newx][newy]=dist[x][y]+1;
            } 
        }
    }
    return {-1, -1};
}

//Hàm kiểm tra ma trận con của start có ô góc trên bên trái là (posx, posy), kích thước là die_size có giống với ma trận con của goal không? 
bool check_same_matrix(ll posx, ll posy, ll height, ll width, const vector<string> &start, const vector<string> &goal)
{
    for (ll i=posx; i<posx+height; i++)
        for (ll j=posy; j<posy+width; j++)
            if (start[i][j]!=goal[i][j]) return false;
    return true;
}

// Hàm tính toán số lượng ô vuông ở vị trí giống nhau của ma trận start so với ma trận goal 
ll calculate_number_identical_squares(const vector<string> &start, const vector<string> &goal)
{
    ll height=start.size();
    ll width=start[0].size();
    ll cnt=0;
    for (ll i=0; i<height; i++)
        for (ll j=0; j<width; j++) 
            if (start[i][j]==goal[i][j]) 
                ++cnt;
    return cnt;
}

// Hàm lấy ra k phần tử có số ô vuông ở vị trí giống nhau lớn nhất. Độ phức tạp O(n.k)
vector<ll> take_index_k_largest_elements(const vector<ll> num_candidates_matching, ll k) 
{
    ll n=num_candidates_matching.size();
    vector<bool> used(n);
    vector<ll> answers;
    for (ll i=0; i<min(n, k); i++) 
    {
        ll mx=-1;
        for (ll i=0; i<num_candidates_matching.size(); i++) if (used[i]==false)
            if (mx==-1 || num_candidates_matching[i]>mx)
                mx=i;
        answers.push_back(mx);
        used[mx]=true;
    }
    return answers;
}

// Hàm tạo ra ứng cử viên tiếp theo 
vector<vector<string>> create_next_generations(const vector<vector<string>> &states, const vector<tuple<ll, ll, ll, vector<string>>> &dies, ll limit_candidates)
{
    vector<vector<string>> candidates, best_candidates;
    vector<ll> num_matching_matrix;
    if (states.size()==0) return best_candidates;
    ll height=states[0].size();
    ll width=states[0][0].size();
    
    for (auto state: states)
        for (ll id=13; id<=dies.size(); id++)
            for (ll i=0, die_height=get<2>(dies[id]); i<height-die_height; i++)
                for (ll j=0, die_width=get<1>(dies[id]); j<width-die_width; j++)
                    if (check_same_matrix(i, j, die_height, die_width, state, goal)==false) 
                            for (ll direction=0; direction<4; direction++) 
                            {
                                vector<string> new_state=apply_die(id, i, j, direction, state);
                                candidates.push_back(new_state);
                                num_matching_matrix.push_back(calculate_number_identical_squares(new_state, goal));
                            }
    
    vector<ll> index_best_candidates=take_index_k_largest_elements(num_matching_matrix, limit_candidates);
    for (ll id: index_best_candidates) best_candidates.push_back(candidates[id]);
    return best_candidates;
}

// Hàm áp dụng thuật toán tìm kiếm bằng beam search 
pair<vector<vector<string>>, vector<array<ll, 4>>> apply_beam_search(vector<string> &start, ll max_steps=2)
{
    vector<vector<string>> answer;
    vector<array<ll, 4>> ops;
    answer.push_back(start);
    for (ll i=0; i<max_steps; i++) answer=create_next_generations(answer, dies, 5);
    return {answer, ops};
}

// Hàm lưu đáp án hiện tại vào cuối all_solution.json 
void append_answer_to_all_solution(const vector<array<ll, 4>> &answer) {
    // Đọc nội dung của file all_solution.json
    ifstream inFile("all_solution.json");
    string content;
    if (inFile.is_open()) {
        stringstream buffer;
        buffer << inFile.rdbuf();
        content = buffer.str();
        inFile.close();
    }

    // Kiểm tra nếu file trống hoặc không đúng định dạng JSON
    if (content.empty()) {
        content = "[\n";
    } else {
        // Xóa dấu đóng "]" cuối cùng
        size_t pos = content.rfind("]");
        if (pos != string::npos) {
            content = content.substr(0, pos);
        } else {
            cerr << "File all_solution.json không đúng định dạng!" << endl;
            return;
        }
        content += ",\n";
    }

    // Chuyển answer thành chuỗi JSON
    stringstream ss;
    ss << "  {\n";
    ss << "    \"n\":" << answer.size() << ",\n";
    ss << "    \"ops\":[\n";
    for (size_t i = 0; i < answer.size(); ++i) {
        auto [p, x, y, s] = answer[i];
        ss << "      {\n";
        ss << "        \"p\":" << p << ",\n";
        ss << "        \"x\":" << x << ",\n";
        ss << "        \"y\":" << y << ",\n";
        ss << "        \"s\":" << s << "\n";
        ss << "      }";
        if (i != answer.size() - 1) {
            ss << ",";
        }
        ss << "\n";
    }
    ss << "    ]\n";
    ss << "  }";

    // Thêm dữ liệu mới và đóng JSON array
    content += ss.str();
    content += "\n]";

    // Ghi nội dung mới vào file all_solution.json
    ofstream outFile("all_solution.json");
    if (!outFile.is_open()) {
        cerr << "Không thể mở file all_solution.json để ghi!" << endl;
        return;
    }
    outFile << content;
    outFile.close();
    cerr << "Data successfully appended to all_solution.json" << endl;
}

// Hàm in JSON từ vector<array<ll, 4>>
void print_answer(const vector<array<ll, 4>> &answer)
{
    // Mở file để ghi
    ofstream outFile("output.json");
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
    cerr << "Data successfully written to output.json" << endl;
    append_answer_to_all_solution(answer);
}

void solve() {
    init_die();
    read_input();
    auto answer=apply_beam_search(start);
    // print_matrix(start);
    // print_answer(answer.second);
}

int main()
{
    clock_t start1 = clock();
    system("python convert_txt.py");
    clock_t end1 = clock();
    double duration1 = double(end1 - start1) / CLOCKS_PER_SEC;
    cerr << "Time convert txt: " << duration1 << " seconds" << endl;
    
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    #ifndef ONLINE_JUDGE
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
    #endif

    clock_t start2 = clock();
    solve();
    clock_t end2 = clock();
    double duration2 = double(end2 - start2) / CLOCKS_PER_SEC;
    cerr << "Time find solution: " << duration2 << " seconds" << endl;

    // system("python visualize.py");

    return 0;
}