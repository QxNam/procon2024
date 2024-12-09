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
#include <queue>


using namespace std;
#define ll int 
#define endl '\n'
#define TOP 0 
#define BOTTOM 1 
#define LEFT 2 
#define RIGHT 3

ll width, height, n, Fixed[257][257];
ll pre_num_matching, best_num_matching=0, check=1;
ll dx[]={0, 0, 1, -1}, dy[]={1, -1, 0, 0}, visited[257][257];

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
vector<vector<operation>> create_next_generations(vector<vector<operation>> states, vector<die_pattern> dies, ll max_candidates=1, double grow_rate=0.1)
{
    vector<vector<operation>> candidates, best_candidates;
    vector<ll> num_matching_matrix;
    if (states.size()==0) return best_candidates;

    ll total_operations = states.size() * dies.size() * height * 2 * width * 2 * 4;
    ll processed_operations = 0;
    auto start_time = std::chrono::high_resolution_clock::now();

    for (vector<operation> state: states)
    {
        board cur_board=start;
        for (operation opt: state) cur_board=cur_board.apply_die(opt);
        for (ll id=0; id<dies.size(); id++) if (dies[id].height<=height)
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
                        
                        board new_board=cur_board.apply_die(operation(id, i, j, direction));
                        vector<operation> new_state=state;
                        new_state.push_back(operation(id, i, j, direction));
                        candidates.push_back(new_state);
                        num_matching_matrix.push_back(calculate_number_identical_squares(new_board, goal));
                    }
    }
    cerr<<endl;
    
    best_num_matching=num_matching_matrix[0];
    if (1.0*pre_num_matching/best_num_matching<grow_rate) return states;
    vector<ll> index_best_candidates=take_index_k_largest_elements(num_matching_matrix, 5);
    for (ll id: index_best_candidates) best_candidates.push_back(candidates[id]);
    cerr<<num_matching_matrix[index_best_candidates[0]]<<"/"<<height*width<<endl;
    return best_candidates;
}

// Hàm áp dụng thuật toán tìm kiếm bằng beam search 
vector<operation> apply_beam_search(ll max_steps=1, ll max_candidates=1, double grow_rate=0.1)
{
    vector<operation> init_state;
    vector<vector<operation>> candides;
    candides.push_back(init_state);
    pre_num_matching=calculate_number_identical_squares(start, goal);
    for (ll i=0; i<max_steps; i++) 
    {
        cerr<<"Generation "<<i+1<<endl;
        candides=create_next_generations(candides, dies, max_candidates, grow_rate);
        if (1.0-1.0*pre_num_matching/best_num_matching<grow_rate) break;
    }
    return candides[0];
}

pair<ll, ll> bfs(const board &start, const board &goal, ll curx, ll cury)
{
    if (start.matrix[curx][cury]==goal.matrix[curx][cury]) return {curx, cury};

    for (ll i=0; i<height; i++)
        for (ll j=0; j<width; j++)
            visited[i][j]=0;

    queue<pair<ll, ll>> q;
    q.push({curx, cury});
    visited[curx][cury]=1;
    pair<ll, ll> ans={curx, cury};
    ll min_bit=20;
    while (!q.empty())
    {
        auto [x, y]=q.front(); q.pop();
        for (ll i=0; i<4; i++) 
        {
            ll newx=x+dx[i], newy=y+dy[i];
            if (0<=newx && newx<height && 0<=newy && newy<width && Fixed[newx][newy]==0 && visited[newx][newy]==0)
            {
                if (start.matrix[newx][newy]==goal.matrix[curx][cury]) {
                    ll dx=abs(newx-curx), dy=abs(newy-cury);
                    if (__builtin_popcount(dx)+__builtin_popcount(dy)<=min_bit) 
                    {
                        min_bit=__builtin_popcount(dx)+__builtin_popcount(dy);
                        ans={newx, newy};
                    }
                }
                visited[newx][newy]=1;
                q.push({newx, newy});
            } 
        }
    }
    return ans;
}

vector<operation> apply_binary_lifting(board cur_board)
{
    vector<operation> answer;
    ll total_cells = height * width;
    ll progress_threshold = 5; // Ngưỡng hiển thị tiến trình (5%)
    ll next_report = progress_threshold * total_cells / 100; 
    auto start_time = std::chrono::high_resolution_clock::now();
    ll processed_cells = 0; 

    for (ll i=0; i<height; i++)
    {
        for (ll j=0; j<width; j++) 
        {
            auto [x, y]=bfs(cur_board, goal, i, j);
            while (y<j) 
            {
                ll d=j-y;
                for (ll k=8; k>=0; k--) if (d&(1LL<<k)) 
                {
                    cur_board=cur_board.apply_die(operation((k==0?0:3*k-2), x, y+1, RIGHT));
                    answer.push_back(operation((k==0?0:3*k-2), x, y+1, RIGHT));
                    y+=(1LL<<k);
                }
            }
            while (y>j)
            {
                ll d=y-j;
                for (ll k=8; k>=0; k--) if (d&(1LL<<k)) 
                {
                    cur_board=cur_board.apply_die(operation((k==0?0:3*k-2), x, y-(1LL<<k), LEFT));
                    answer.push_back(operation((k==0?0:3*k-2), x, y-(1LL<<k), LEFT));
                    y-=(1LL<<k);
                }
            }
            while (x<i)
            {
                ll d=i-x;
                for (ll k=8; k>=0; k--) if (d&(1LL<<k)) 
                {
                    cur_board=cur_board.apply_die(operation((k==0?0:3*k-2), x+1, y, BOTTOM));
                    answer.push_back(operation((k==0?0:3*k-2), x+1, y, BOTTOM));
                    x+=(1LL<<k);
                }
            }
            while (x>i) 
            {
                ll d=x-i;
                for (ll k=8; k>=0; k--) if (d&(1LL<<k))
                {
                    cur_board=cur_board.apply_die(operation((k==0?0:3*k-2), x-(1LL<<k), y, TOP));
                    answer.push_back(operation((k==0?0:3*k-2), x-(1LL<<k), y, TOP));
                    x-=(1LL<<k);
                }
            }
            Fixed[i][j]=1;

            processed_cells++;
            if (processed_cells >= next_report) 
            {
                auto elapsed_time = std::chrono::high_resolution_clock::now() - start_time;
                auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed_time).count();
                double progress = (double)processed_cells / total_cells * 100;
                cerr << "\rProcessing: " << std::setw(3) << std::setfill(' ') << (int)progress << "%, Time elapsed: " << elapsed_ms / 1000.0 << "s" << flush;
            }
        }
    }
    cerr<<endl;
    return answer;
}

// Hàm in JSON từ vector<operation>
void print_answer(const vector<operation> &answer, string id)
{
    // Mở file để ghi
    ofstream outFile("data\\output\\output_"+id+".json");
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
    cerr << "Data successfully written to data\\output\\output_"<<id<<".json" << endl;
}

void solve(string question_id) {
    init_die();
    read_input();
    cerr<<calculate_number_identical_squares(start, goal)<<"/"<<width*height<<endl;
    vector<operation> answer1=apply_beam_search(3, 1, 0.1);
    for (operation opt: answer1) start=start.apply_die(opt);
    vector<operation> answer2=apply_binary_lifting(start);
    for (operation opt: answer2) answer1.push_back(opt);
    print_answer(answer1, question_id);
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
    filesystem::create_directories("data\\output");
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