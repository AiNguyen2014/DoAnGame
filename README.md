# ĐỒ ÁN CUỐI KÌ - AI MUMMY MAZE SOLVER
trong đó người chơi phải điều hướng để thoát khỏi mê cung đầy xác ướp và bẫy. Trò chơi tích hợp các thuật toán tìm kiếm như Breadth-First Search (BFS), A*, Min-Conflict và Q-Learning để tự động tìm đường đi tối ưu
# Mục lục
1. Tổng quan
2. Tính năng
3. Công nghệ sử dụng
4. Cách hoạt động
5. Các thuật toán được triển khai
6. Bắt đầu
7. Cải tiến trong tương lai
8. Tác giả
9. Cách chơi
# Tổng quan
Mummy Maze là một trò chơi giải đố kinh điển, trong đó người chơi điều khiển player (nhà thám hiểm) để được yêu cầu thoát khỏi mê cung, trong khi tránh các loại địch (mummy trắng, đỏ) di chuyển và bẫy người chết. Dự án này kết hợp các thuật toán AI để:

 - Tự động giải quyết các cấp độ của Mummy Maze.
 - Tương tác mô phỏng trò chơi.
 - Đánh giá hiệu suất của các thuật toán tìm kiếm.

# Tính năng
  * Chơi tương tác : Chơi thủ công bằng phím hoặc xem AI auto de mê cung.
  * Nhiều thuật toán AI : BFS, A*, Min-Conflict và Q-Learning.
  * So sánh hiệu suất : Đo số bước, số trạng thái đã truy cập và thời gian thực hiện.
  * Đồ họa giao diện : Sử dụng Pygame để hiển thị cung cấp và các nhân vật.
  * Quản lý cấp độ : Hỗ trợ nhiều cấp độ với độ khó tăng dần, được định nghĩa trong tệp JSON.

# Công nghệ sử dụng
* Python 3.10 trở lên
* Trò chơi Pygame
* Các mô-đun chuẩn của Python: 
  1. json: Đọc dữ liệu cấp độ từ levels.json
  2. random: Hỗ trợ thuật toán Q-Learning.
  3. heapq: Hàng đợi ưu tiên cho A* và BFS.
  4. copy: Sao chép trạng thái trò chơi.
  5. collections: Hàng đợi cho BFS.
  6. sys: Thoát chương trình.
  7. math: Tính heuristic Euclidean.
     
# Cách hoạt động
  Biểu tượng diễn đàn trò chơi : Mỗi cấp độ được biểu diễn bằng ma trận 2D (mê cung) với các tường thuật, cầu thang, xác hoạt, bẫy và vị trí bắt đầu của người chơi, được tải xuống từ cấp độ tệp.json .
  Quản lý trạng thái : Theo dõi vị trí của người chơi, cụ thể và cổng trạng thái (cổng) trong mê cung.
  Thực thi thuật toán : Sử dụng các thuật toán tìm kiếm để tìm đường đi toàn bộ từ vị trí bắt đầu đến cầu thang, tránh tối ưu và bẫy.
  Người dùng giao diện : Hiển thị cung cấp mê cung, nhân vật và các nút điều khiển (như Undo, Reset, World Map) thông qua Pygame.
  
# Các thuật toán được triển khai

  Breadth-First Search (BFS) : Khám phá tất cả các trạng thái theo từng lớp, đảm bảo đường đi ngắn nhất nhưng có thể tốn nhiều tài nguyên.
  A *: Sử dụng heuristic (như khoảng cách Manhattan) để ưu tiên các trạng thái gần mục tiêu, cân bằng giữa hiệu quả và chất lượng đường đi.
  Min-Conflict : Chọn các bước chuyển giảm xung đột với tường hoặc bẫy, phù hợp cho các mê cung đơn giản.
  Q-Learning : Một thuật toán học tăng cường, học cách chọn hành động tối ưu thông qua thử và sai, thích hợp cho các vấn đề.

# Bắt đầu

1. Sao chép kho lưu trữ:
   
git clone https://github.com/your-repository/MummyMaze.git
cd MummyMaze

3. Cài đặt các thư viện cần thiết: pip install pygame,....
4. Chạy trò chơi: python main.py
5. Cấu trúc thư mục:
     - levels.json: Chứa dữ liệu các cấp độ.
     - images/: Thư mục chứa hình ảnh cho tường, cầu thang, nhân vật, v.v.
     - sounds/: Thư mục chứa âm thanh nền và hiệu ứng.
     - còn lại là các file .py
   
# Cải tiến trong tương lai
Cải thiện heuristic cho A* để tăng tốc độ tìm kiếm.
Thêm tính năng tạo tùy chọn mê cung.
Tích hợp phân tích hiệu suất trực tiếp trong trò chơi (ví dụ: hiển thị số bước và thời gian thực thi).
Thêm các AI thuật toán khác, như Thuật toán mô phỏng hoặc Thuật toán di truyền.
Hỗ trợ lưu trò chơi tiến trình và tải lại.

# Tác giả

1. **[Chung Thị Ái Nguyên] (https://github.com/AiNguyen2014)**
2. **[Lê Huỳnh Kiều Oanh] (https://github.com/kOanhNe)**
3. **[Nguyễn Tấn Thành] 

# Cách chơi
* Chơi thủ công :
    * Sử dụng các mũi tên mũi tên ↑ ↓ ← → để chuyển người chơi trong mê cung.
    * Nhấn UNDO DI CHUYỂN để quay lại bước trước đó.
    * Nhấn RESET MAZE để thực hiện cấp độ mới.
    * Nhấn WORLD MAP để chọn cấp độ khác.
    * Nhấn QUIT TO MAIN để quay lại menu chính.
* Chơi tự động :
    * Từ menu chính, nhấn AUTO PLAY để kích hoạt AI chế độ.
    * Chọn thuật toán (BFS, A*, Min-Conflict) bằng cách nhấp vào nút "Thuật toán" trong giao diện.
* Mục tiêu :
    * Đưa người chơi đến cầu thang (cầu thang) để hoàn thành cấp độ.
    * Tránh va chạm xác hoặc rơi vào bẫy.
* Đầu ra của bảng điều khiển :
    * Hiển thị thông tin về cấp độ, vị trí người chơi, linh hoạt và các bước chuyển đổi của AI.

