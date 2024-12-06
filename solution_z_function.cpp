#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define TOP 0 
#define BOTTOM 1 
#define LEFT 2 
#define RIGHT 3

ll width, height, n, best_answer=1e18;

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

struct Z_function
{
    vector<ll> z; // z[i]=do dai tien to dai nhat cua s[0:n-1] va s[i: n-1]
    ll n, l, r;
    string s;

    Z_function(){}
    Z_function(string _s)
    {
        s=_s;
        n=_s.size();
        z.resize(n+5);
        for (ll i=0; i<z.size(); i++) z[i]=0;
        z[0]=0;
        l=0; r=0;  //duy tri doan s[l, r)=s[0:r-l) da duoc tinh. z[i]=r-l 
        for (ll i=1; i<n; i++)
        {
            if (i<r) z[i]=min(z[i-l], r-i);  //lay min (z[i-l], r-i) vi z[i-l] co the lon hon r-i vo ly
            while (i+z[i]<n && s[z[i]]==s[i+z[i]]) ++z[i];  //thuat toan tam thuong 
            if (i+z[i]>r) l=i, r=i+z[i];  //cap nhat doan [l, r)=[i, i+z[i])
        }
    }
};

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

ll loss(ll curx, ll cury, ll newx, ll newy, ll len)
{
    ll dx=abs(curx-newx);
    ll dy=abs(cury-newy);
    ll L=__builtin_popcount(dy)+len*__builtin_popcount(dx)*len; 
    return L/len;
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

array<ll, 3> z_function(const board &cur_board, const board &goal, ll curx, ll cury) {
    string s;
    for (ll j=cury; j<width; j++) s.push_back(goal.matrix[curx][j]);
    s.push_back('$');
    ll m=s.size(), min_step=1e18, len=1;
    pair<ll, ll> ans={-1, -1};

    string x=s;
    for (ll j=cury; j<width; j++) x.push_back(cur_board.matrix[curx][j]);
    Z_function z1(x);  
    for (ll j=m; j<x.size(); j++) 
        if (z1.z[j]>0 && loss(curx, cury, curx, cury+j-m, z1.z[j])<min_step) {
            min_step=loss(curx, cury, curx, cury+j-m, z1.z[j]);
            ans={curx, cury+j-m};
            len=z1.z[j];
        }

    for (ll i=curx+1; i<height; i++)
    {
        string x=s;
        for (ll j=0; j<width; j++) x.push_back(cur_board.matrix[i][j]);
        Z_function z2(x);                        
        for (ll j=m; j<x.size(); j++) 
            if (z2.z[j]>0 && loss(curx, cury, i, j-m, z2.z[j])<min_step) {
                min_step=loss(curx, cury, i, j-m, z2.z[j]);
                ans={i, j-m};
                len=z2.z[j];
            }
    } 
    return {ans.first, ans.second, len};
}

vector<operation> apply_z_funtion(board cur_board)
{
    vector<operation> answer;
    ll total_cells = height * width;
    ll progress_threshold = 5; // Ngưỡng hiển thị tiến trình (5%)
    ll next_report = progress_threshold * total_cells / 100; 
    auto start_time = std::chrono::high_resolution_clock::now();
    ll processed_cells = 0; 

    map<ll, ll> cntlen, cntdie;

    for (ll i=0; i<height; i++)
    {
        for (ll j=0; j<width; j++) 
        {
            processed_cells++;
            if (processed_cells >= next_report) 
            {
                auto elapsed_time = std::chrono::high_resolution_clock::now() - start_time;
                auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed_time).count();
                double progress = (double)processed_cells / total_cells * 100;
                cerr << "\rProcessing: " << std::setw(3) << std::setfill(' ') << (int)progress << "%, Time elapsed: " << elapsed_ms / 1000.0 << "s" << flush;
            }
            
            if (cur_board.matrix[i][j]==goal.matrix[i][j]) continue;
            auto [x, y, len]=z_function(cur_board, goal, i, j);  
            ++cntlen[len];    
            while (y<j) 
            {
                ll d=j-y;
                for (ll k=8; k>=0; k--) if (d&(1LL<<k)) 
                {
                    cur_board=cur_board.apply_die(operation((k==0?0:3*k-2), x, y+len, RIGHT));
                    answer.push_back(operation((k==0?0:3*k-2), x, y+len, RIGHT));
                    ++cntdie[((k==0?0:3*k-2))];
                    // cout<<"[direction, id, x, y]:   RIGHT "<<dies[(k==0)?0:3*k-2].height<<" "<<x<<" "<<y+len<<" "<<endl;
                    // cur_board.print();
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
                    ++cntdie[((k==0?0:3*k-2))];
                    // cout<<"[direction, id, x, y]:   LEFT "<<dies[(k==0)?0:3*k-2].height<<" "<<x<<" "<<y-(1LL<<k)<<" "<<endl;
                    // cur_board.print();
                    y-=(1LL<<k);
                }
            }

            vector<ll> row_distances;
            for (ll l=0; l<len; l++) row_distances.push_back(x);
            for (ll l=0; l<len; l++) if (y+l<width)
            {
                ll d=row_distances[l]-i;      
                assert(d>=0);
                for (ll k=8; k>=0; k--) if (d&(1LL<<k))
                {
                    ll die_id=(k==0?0:3*k-2);
                    cur_board=cur_board.apply_die(operation(die_id, row_distances[l]-(1LL<<k), y+l, TOP));
                    answer.push_back(operation(die_id, row_distances[l]-(1LL<<k), y+l, TOP));
                    ++cntdie[((k==0?0:3*k-2))];
                    assert(row_distances[l]-(1LL<<k)>=i);
                    for (ll t=l; t<l+dies[die_id].width && t<len; t++) row_distances[t]-=(1LL<<k);
                    // cout<<"[direction, id, x, y]:   TOP "<<dies[die_id].height<<" "<<row_distances[l]-(1LL<<k)<<" "<<y+l<<" "<<endl;
                    // cur_board.print();
                }
            }
        }
    }
    cerr<<endl;
    for (auto [x, y]: cntlen) cout<<x<<" "<<y<<endl; cout<<endl;
    for (auto [x, y]: cntdie) cout<<x<<" "<<y<<endl; cout<<endl;
    return answer;
}

// Hàm lưu đáp án hiện tại vào cuối all_solution.json 
void append_answer_to_all_solution(const vector<operation> &answer, bool is_row=true) {
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
        if (is_row==1)
        {
            ss << "      {\n";
            ss << "        \"p\":" << p << ",\n";
            ss << "        \"x\":" << y << ",\n";
            ss << "        \"y\":" << x << ",\n";
            ss << "        \"s\":" << s << "\n";
            ss << "      }";
        }
        else 
        {
            ss << "      {\n";
            ss << "        \"p\":" << p << ",\n";
            ss << "        \"y\":" << x << ",\n";
            ss << "        \"x\":" << y << ",\n";
            ss << "        \"s\":" << s << "\n";
            ss << "      }";
        }
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
void print_answer(const vector<operation> &answer, bool is_row=true)
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
        if (is_row==1)
        {
            outFile << "      {\n";
            outFile << "        \"p\":" << p << ",\n";
            outFile << "        \"x\":" << y << ",\n";
            outFile << "        \"y\":" << x << ",\n";
            outFile << "        \"s\":" << s << "\n";
            outFile << "      }";
        }
        else 
        {
            outFile << "      {\n";
            outFile << "        \"p\":" << p << ",\n";
            outFile << "        \"y\":" << x << ",\n";
            outFile << "        \"x\":" << y << ",\n";
            outFile << "        \"s\":" << s << "\n";
            outFile << "      }";
        }
        if (i != answer.size() - 1) {
            outFile << ",";
        }
        outFile << "\n";
    }

    // Kết thúc chuỗi JSON
    outFile << "  ]" << endl;
    outFile << "}" << endl;

    // Đóng file
    outFile.close();
    cerr << "Data successfully written to output.json" << endl;
    // append_answer_to_all_solution(answer);
}

void solve(bool is_row=true) {
    init_die();
    read_input();
    cerr<<calculate_number_identical_squares(start, goal)<<"/"<<width*height<<endl;
    vector<operation> answer=apply_z_funtion(start);
    for (operation opt: answer) start=start.apply_die(opt);
    start.print();
    cerr<<calculate_number_identical_squares(start, goal)<<"/"<<width*height<<endl;
    if (answer.size()<best_answer) {
        best_answer=answer.size();
        print_answer(answer, is_row);
    }
}

int main()
{
    clock_t start1 = clock();
    system("python convert_txt.py");
    clock_t end1 = clock();
    double duration1 = double(end1 - start1) / CLOCKS_PER_SEC;
    cerr << "Time convert txt: " << duration1 << " seconds" << endl;

    clock_t start2 = clock();
    freopen("input_row.txt", "r", stdin);
    freopen("output_row.txt", "w", stdout);
    solve(true);
    clock_t end2 = clock();
    double duration2 = double(end2 - start2) / CLOCKS_PER_SEC;
    cerr << "Time find solution: " << duration2 << " seconds" << endl;

    clock_t start3 = clock();
    freopen("input_col.txt", "r", stdin);
    freopen("output_col.txt", "w", stdout);
    solve(false);
    clock_t end3 = clock();
    double duration3 = double(end3 - start3) / CLOCKS_PER_SEC;
    cerr << "Time find solution: " << duration3 << " seconds" << endl;


    // system("python visualize.py");

    return 0;
}