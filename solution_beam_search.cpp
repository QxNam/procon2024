#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define TOP 0 
#define BOTTOM 1 
#define LEFT 2 
#define RIGHT 3

ll width, height, n, Fixed[257][257];
ll pre_num_matching, best_num_matching=0, check=1;

struct die_pattern
{
    ll id, width, height;
    vector<string> matrix;
    
    die_pattern(){}
    die_pattern(ll _id, ll _width, ll _height, vector<string> _matrix) {
        id=_id;
        width=_width;
        height=_height;
        matrix=_matrix;
    }

    void print() {
        for (string row: matrix)
            cout<<row<<endl;
    }
};

vector<die_pattern> dies;

struct operation {
    ll id, x, y, direction;

    operation(){}
    operation(ll _id, ll _x, ll _y, ll _direction){
        id=_id;
        x=_x;
        y=_y;
        direction=_direction;
    }
};

struct board {
    ll height, width;
    vector<string> matrix;

    board() {}

    board(ll _height, ll _width, vector<string> _matrix) {
        height=_height;
        width=_width;
        matrix=_matrix;
    }

    board clone() const {
        board new_board;
        new_board.height = height;
        new_board.width = width;
        new_board.matrix = matrix;
        return new_board;
    }

    // Hàm áp dụng die cutting của die thứ id vào vị trí (x, y), hướng là direction={TOP, BOTTOM, LEFT, RIGHT}
    board apply_die(operation opt) {
        auto [id, x, y, direction]=opt;
        auto [_, w, h, pattern] = dies[id];
        board new_board=this->clone();

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
                                lifted_elements.push_back(new_board.matrix[board_x][board_y]);
                                new_board.matrix[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                            }
                        }
                    }
                    for (ll board_y=0; board_y<width; board_y++) if (new_board.matrix[board_x][board_y]!='.') new_row.push_back(new_board.matrix[board_x][board_y]);
                    while (!lifted_elements.empty()) {
                        ll x=lifted_elements.front(); 
                        lifted_elements.pop_front();
                        new_row.push_back(x);
                    }
                    new_board.matrix[board_x]=new_row;
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
                                lifted_elements.push_back(new_board.matrix[board_x][board_y]);
                                new_board.matrix[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                            }
                        }
                    }
                    string new_row;
                    while (!lifted_elements.empty()) {
                        ll x=lifted_elements.front(); 
                        lifted_elements.pop_front();
                        new_row.push_back(x);
                    }
                    for (ll board_y=0; board_y<width; board_y++) if (new_board.matrix[board_x][board_y]!='.') new_row.push_back(new_board.matrix[board_x][board_y]);
                    new_board.matrix[board_x]=new_row;
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
                                lifted_elements.push_back(new_board.matrix[board_x][board_y]);
                                new_board.matrix[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                            }
                        }
                    }
                    string new_col;
                    for (ll board_x=0; board_x<height; board_x++) if (new_board.matrix[board_x][board_y]!='.') new_col.push_back(new_board.matrix[board_x][board_y]);
                    while (!lifted_elements.empty()) {
                        ll x=lifted_elements.front(); 
                        lifted_elements.pop_front();
                        new_col.push_back(x);
                    }
                    for (ll board_x=0; board_x<height; board_x++) new_board.matrix[board_x][board_y]=new_col[board_x];
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
                                lifted_elements.push_back(new_board.matrix[board_x][board_y]);
                                new_board.matrix[board_x][board_y] = '.'; // Ký hiệu '.' cho phần đã nhấc lên
                            }
                        }
                    }
                    string new_col;
                    while (!lifted_elements.empty()) {
                        ll x=lifted_elements.front(); 
                        lifted_elements.pop_front();
                        new_col.push_back(x);
                    }
                    for (ll board_x=0; board_x<height; board_x++) if (new_board.matrix[board_x][board_y]!='.') new_col.push_back(new_board.matrix[board_x][board_y]);
                    for (ll board_x=0; board_x<height; board_x++) new_board.matrix[board_x][board_y]=new_col[board_x];
                }
            }
        }

        return new_board;
    }

    void print() {
        for (string row: matrix)
            cout<<row<<endl;
    }
};
board start, goal;

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

// Hàm khởi tạo các die cố định ban đầu 
void init_die() {
    dies.push_back(die_pattern(0, 1, 1, createTypeI(1)));
    for (ll idx=1, i=2; i<=256; i*=2) {
        dies.push_back(die_pattern(idx, i, i, createTypeI(i)));
        ++idx;
        dies.push_back(die_pattern(idx, i, i, createTypeII(i)));
        ++idx;
        dies.push_back(die_pattern(idx, i, i, createTypeIII(i)));
    }
}

// Hàm nhập input đầu vào (đã chuyển từ file json sang txt)
void read_input()
{
    cin>>width>>height;
    vector<string> st, fi;
    for (ll i=0; i<height; i++) {
        string x; cin>>x;
        st.push_back(x);
    }
    for (ll i=0; i<height; i++) {
        string x; cin>>x;
        fi.push_back(x);
    }
    start=board(height, width, st);
    goal=board(height, width, fi);
    cin>>n;
    for (ll i=0; i<n; i++){
        ll id, w, h; cin>>id>>w>>h;
        vector<string> pattern;
        for (ll j=0; j<h; j++) {
            string s; cin>>s;
            pattern.push_back(s);
        }
        dies.push_back(die_pattern(id, w, h, pattern));
    }
}

//Hàm tìm vị trí ô đúng gần nhất với ô (curx, cury)
pair<ll, ll> bfs(const board &start, const board &goal, ll curx, ll cury)
{
    auto [heigt, width, start_matrix]=start;
    auto [_, __, goal_matrix]=goal;
    if (start_matrix[curx][cury]==goal_matrix[curx][cury]) return {curx, cury};
    ll dx[]={0, 0, -1, 1};
    ll dy[]={1, -1, 0, 0};

    queue<pair<ll, ll>> q;
    q.push({curx, cury});
    while (!q.empty())
    {
        auto [x, y]=q.front(); q.pop();
        for (ll i=0; i<4; i++) 
        {
            ll newx=x+dx[i], newy=y+dy[i];
            if (0<=newx && newx<height && 0<=newy && newy<width && Fixed[newx][newy]==0)
            {
                if (start_matrix[newx][newy]==goal_matrix[curx][cury]) 
                    return {newx, newy};
                q.push({newx, newy});
            } 
        }
    }
    return {-1, -1};
}

// Hàm tính toán số lượng ô vuông ở vị trí giống nhau của ma trận start so với ma trận goal 
ll calculate_number_identical_squares(const board &start, const board &goal)
{
    ll cnt=0;
    for (ll i=0; i<height; i++)
        for (ll j=0; j<width; j++) 
            if (start.matrix[i][j]==goal.matrix[i][j]) 
                ++cnt;
    return cnt;
}

// Hàm lấy ra k phần tử có số ô vuông ở vị trí giống nhau lớn nhất. Độ phức tạp O(n.k)
vector<ll> take_index_k_largest_elements(const vector<ll> num_candidates_matching, ll k) 
{
    ll n=num_candidates_matching.size();
    vector<bool> used(n, false);
    vector<ll> answers;
    for (ll i=0; i<min(n, k); i++) 
    {
        ll id_max=-1;
        for (ll i=0; i<num_candidates_matching.size(); i++) if (used[i]==false)
            if (id_max==-1 || num_candidates_matching[i]>num_candidates_matching[id_max])
                id_max=i;
        answers.push_back(id_max);
        used[id_max]=true;
    }
    return answers;
}

// Hàm tạo ra ứng cử viên tiếp theo 
vector<vector<operation>> create_next_generations(vector<vector<operation>> states, vector<die_pattern> dies, ll max_candidates=5, double grow_rate=0.1)
{
    vector<vector<operation>> candidates, best_candidates;
    vector<ll> num_matching_matrix;
    if (states.size()==0) return best_candidates;

    ll total_operations = states.size() * dies.size() * height * 2 * width * 2 * 4;
    ll processed_operations = 0;
    auto start_time = std::chrono::high_resolution_clock::now();

    for (vector<operation> state: states)
        for (ll id=0; id<dies.size(); id++)
            for (ll i=-height, die_height=dies[id].height; i<height; i++)
                for (ll j=-width, die_width=dies[id].width; j<width; j++)
                    for (ll direction=0; direction<4; direction++) 
                    {
                        processed_operations++;
                        if (processed_operations % 10000 == 0) {
                            auto elapsed_time = std::chrono::high_resolution_clock::now() - start_time;
                            auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed_time).count();
                            double progress = (double)processed_operations / total_operations * 100;
                            cerr << "\rProcessing: " << std::setw(3) << std::setfill(' ') << (int)progress << "%, Time elapsed: " << elapsed_ms / 1000.0 << "s";
                        }

                        board new_board=start;
                        for (operation opt: state) new_board=new_board.apply_die(opt);
                        new_board=new_board.apply_die(operation(id, i, j, direction));
                        vector<operation> new_state=state;
                        new_state.push_back(operation(id, i, j, direction));
                        candidates.push_back(new_state);
                        num_matching_matrix.push_back(calculate_number_identical_squares(new_board, goal));
                    }
    cerr<<endl;
    
    best_num_matching=num_matching_matrix[0];
    if (1.0*pre_num_matching/best_num_matching<grow_rate) return states;
    vector<ll> index_best_candidates=take_index_k_largest_elements(num_matching_matrix, 5);
    for (ll id: index_best_candidates) best_candidates.push_back(candidates[id]);
    return best_candidates;
}

// Hàm áp dụng thuật toán tìm kiếm bằng beam search 
vector<operation> apply_beam_search(ll max_steps=1, double grow_rate=0.1)
{
    vector<operation> init_state;
    vector<vector<operation>> candides;
    candides.push_back(init_state);
    pre_num_matching=calculate_number_identical_squares(start, goal);
    for (ll i=0; i<max_steps; i++) 
    {
        candides=create_next_generations(candides, dies, 5, grow_rate);
        if (1.0*pre_num_matching/best_num_matching<grow_rate) break;
    }
    return candides[0];
}

// Hàm lưu đáp án hiện tại vào cuối all_solution.json 
void append_answer_to_all_solution(const vector<operation> &answer) {
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
        ss << "        \"x\":" << y << ",\n";
        ss << "        \"y\":" << x << ",\n";
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

// Hàm in JSON từ vector<operation>
void print_answer(const vector<operation> &answer)
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
        outFile << "      \"x\":" << y << "," << endl;
        outFile << "      \"y\":" << x << "," << endl;
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
    // append_answer_to_all_solution(answer);
}

void solve() {
    init_die();
    read_input();
    vector<operation> answer=apply_beam_search(2);
    print_answer(answer);
    board tmp=start;
    for (operation opt: answer) tmp=tmp.apply_die(opt);
    cerr<<calculate_number_identical_squares(tmp, goal)<<"/"<<width*height<<endl;
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