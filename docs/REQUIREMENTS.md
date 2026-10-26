# Đối chiếu V1 + V2 + yêu cầu tiếp tục 26/10/2026

Yêu cầu mới được lưu tại [REQUEST_2026-10-26](REQUEST_2026-10-26.md), ưu tiên khi khác ngân sách cũ. Prompt gốc được giữ nguyên. Báo cáo số thực sinh từ dữ liệu, không đánh dấu thiết kế thành gameplay để đủ số.

| Yêu cầu | Trạng thái 0.2 | Bằng chứng / phần còn lại |
|---|---|---|
| Python 3.12, Pygame CE, 2D offline | Có | Source modular, PNG/WAV/font đóng gói |
| 8 chương gồm mở đầu/kết | 2 playable, 6 planned | chapters.json; Mở đầu + Hanako |
| Ít nhất 7–8 maps mỗi chương | Hai chương đầu: mỗi chương 8 | 16 PNG/layout/collision riêng; còn ít nhất 48 maps |
| Ít nhất 45.000–50.000 lời thoại tổng | Chưa đủ toàn dự án | 13.777 live, 16.586 written; ngân sách 50.000 |
| Mỗi thoại ít nhất hai manh mối | 76/76 có hai trích dẫn riêng và hai đích puzzle | narrative_audit kiểm anchor/ID; cần review văn học với người |
| Không dồn NPC/manh mối | Đã triển khai gate theo sự kiện | 59 cảnh live; tối đa 2 NPC/phòng; 44 ghi chép mở dần |
| 25 nhân vật có tiểu sử/vai trò | Có 25 hồ sơ | 11 người có cảnh live; những người còn lại chưa có gameplay |
| 100 câu đố liên kết | 100 thiết kế, 22 playable | 125 liên kết xuyên chương trong graph; 78 chưa triển khai |
| Cơ chế đa dạng | 9 thao tác riêng + nhập/chọn + ký ức | Giỏ hàng, pin, chuỗi, dây, nhịp, vòng khóa, đếm, cửa, chốt |
| Quota puzzle 35/20/20/15/10 | Chưa đạt | Hiện 16/25/17/24/18; không đổi nhãn giả để đủ |
| 5 endings tích lũy, 10 epilogue/ending | Có rules và preview | Chưa đạt qua campaign; 15 scenes + 50 epilogues có sẵn |
| Truyền thuyết đúng chương | Hanako playable, chương sau theo kế hoạch gốc | Kuchisake, Teke Teke, Inunaki, Akai Heya VHS 1998 |
| Ren về vì mẹ/căn nhà; đời sống | Có | Đi ga, bệnh viện, tiệm, cơm nhà, TV, cassette và đối thoại |
| 5 twist, ≥5 báo trước mỗi twist | Thiết kế | Story Bible + Truth Matrix; chưa mọi báo trước playable |
| Journal/inventory/đối chiếu | Có | Hai cặp chứng cứ, giả thuyết sai không khóa; ghi chú thế giới |
| Fear/Guilt/Clarity; quan hệ sáu trục | Có nền tảng | Hậu quả một lần/cảnh; dependence và điều biến âm/hình còn hạn chế |
| NPC schedule/rumor | Một phần | Gate cảnh và cờ truyền lời; chưa mô phỏng 25 lịch/mạng lan tin |
| Save/schema/settings | Có | Schema 2; migration schema 1 có backup; báo lỗi không ghi đè |
| Pixel art/menu/audio | Tài nguyên phát triển | 88 tệp; 16 maps riêng; 25 sprites vẫn dùng hình thể cơ bản chung |
| Side-view/đổi nhân vật/chase/cinematic | Chưa đầy đủ | Chỉ một scare có chuẩn bị và preview sprites |
| Nhật/Việt/Anh | Tiếng Việt runtime + logo Nhật | Chưa dịch Anh/Nhật |
| Phím/chuột/fullscreen/remap/access | Có một phần đã triển khai | Giảm mưa/scare/CRT/volume; voice/blood/flash dự phòng |
| Windows standalone | Build tự động trên Windows | Trạng thái từng commit tại reports/build_verification.json |
| Route test + kiểm đếm độc lập | Có cho hai chương | 16 maps, 22 puzzles, 44 notes, 59 scenes qua input |
| Thời lượng 9–12 giờ | Không còn bắt buộc theo yêu cầu mới | Không quảng cáo thời lượng chưa playtest |
| Phát hành hoàn chỉnh | Chưa | `narrative_audit.py --release` vẫn phải trả lỗi |

Kiểm tự động không chứng minh nội dung đã được người chơi đánh giá, chất lượng văn hóa/nhịp kể hoặc âm thanh đạt phát hành. Alpix/AutoSprite chưa trả file runtime; không ghi chúng là nguồn sprite đã dùng.
