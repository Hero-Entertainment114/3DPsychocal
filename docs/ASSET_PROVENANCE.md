# Nguồn gốc và quyền dùng

## Asset runtime

Toàn bộ PNG ngoài font-rendered logo được vẽ bằng Pillow primitives ở độ phân giải pixel thấp trong `tools/generate_assets.py` và `tools/build_world_art.py`. Không dùng ảnh đầu vào, tài nguyên từ game khác, hoặc bộ lọc biến ảnh thành pixel. WAV được tổng hợp bằng sin/noise có seed trong cùng công cụ. Code, dữ liệu tự viết, PNG và WAV phát hành Apache-2.0 cùng repo. Manifest liệt kê path/bytes/SHA-256 cho 88 tệp.

Font `NotoSans-Regular.ttf` và chữ logo từ Noto Serif CJK là Google Noto, SIL Open Font License. Giấy phép và thông báo gốc được giữ trong `assets/fonts/NOTO-LICENSE.txt` và `NOTO-CJK-LICENSE.txt`. Font license độc lập với Apache-2.0 của dự án.

## Các plugin được yêu cầu

- Alpix: đã mở canvas 256×256. Công cụ là canvas cộng đồng, không có xuất asset PNG/atlas cho repo. Không nhận được tên người dùng từ widget để quy thuộc nét vẽ, nên không ghi đè pixel chung. Không có file runtime nào lấy từ canvas.
- AutoSprite: tạo character `cmvnw8jov00brn1gj138qm6hc`, tên “Mizuhara Ren — Forgotten Voices”, pixelArt=true. Phản hồi tạo và lần đọc thư viện tiếp theo đều có ảnh null, danh sách spritesheets trống. Không có ảnh/animation tải được trong phiên này. Repo ghi rõ trạng thái, không đặt đường dẫn ảnh giả.
- Các sheets runtime hiện là bản thuật toán gốc. Không gọi chúng là kết quả AutoSprite. Khi có sheet từ AutoSprite, đưa vào nhánh riêng, lưu atlas gốc và đối chiếu frame/pivot trước khi thay loader. Quyền phân phối của asset dịch vụ phải kiểm tra theo tài khoản và điều khoản hiện hành, không tự gán Apache cho output chưa có.

## Nội dung hư cấu và tham khảo

Tsukimori, Kiroku và các nhân vật là sáng tác. Hanako-san, Kuchisake-onna, Teke Teke và Inunaki dùng như mô-típ truyền thuyết, không khẳng định tội ác/hồn ma là lịch sử. Akai Heya là tiền thân hư cấu qua VHS năm 1998, không đưa nguyên bản truyền thuyết web muộn vào năm 1998.

Nguồn cho vòng nghiên cứu tiếp theo (danh mục đọc, **chưa hoàn thành kiểm chứng học thuật**): Michael Dylan Foster, *The Book of Yōkai* (University of California Press); tài liệu niên biểu kinh tế của Bank of Japan; tài liệu lịch sử mạng và truyền thuyết Internet cần kiểm tra xuất xứ riêng. Bản hiện tại không dựa trên một nghiên cứu lịch sử đã nghiệm thu. Cần người đọc văn hóa Nhật trước phát hành.
