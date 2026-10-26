# Lộ trình từ bản 0.2

Theo yêu cầu 26/10/2026, bàn giao mỗi đợt hai chương. Không đặt thời lượng tối thiểu hoặc thêm trì hoãn để đạt số giờ. `status` phân biệt designed/written/playable/preview; chỉ tăng trạng thái khi nội dung thực sự tiếp cận được từ game.

| Đợt | Chương | Ngân sách thoại | Maps tối thiểu | Câu đố |
|---|---|---:|---:|---|
| 0.2 hiện tại | C00 Mở đầu + C01 Hanako | 6.000 + 7.500; thực tế 13.777 | 16 đã làm | P001–P022, 22 đã chơi được |
| Tiếp theo | C02 Kuchisake + C03 Teke Teke | 7.000 + 6.500 | 16 mới | P023–P050, 28 |
| Đợt ba | C04 Inunaki + C05 Akai Heya | 7.000 + 7.000 | 16 mới | P051–P082, 32 |
| Đợt bốn | C06 Người thứ sáu + C07 Kết | 6.000 + 3.000 | 16 mới | P083–P100, 18; năm ending campaign |

Ngân sách tổng 50.000 đơn vị cách trắng; số thực có thể cao hơn một chút. Mục tiêu tối thiểu phát hành là 45.000 lời thoại chơi được, không trùng dòng. Tám maps của chương Kết phải là không gian có hành động/hậu quả và đường đi thật, không được cộng các ending menu như maps. Phân nhánh ending không buộc một lượt chơi đọc mọi lời thoại.

## Cổng chất lượng mỗi đợt

1. Mỗi phòng có mục đích, vật thể, collision, lối vào/ra; không đổi tên cùng một ảnh để tăng số maps. Ít nhất tám maps/chương.
2. Hội thoại viết theo cảnh đời sống và sự kiện, tối thiểu hai manh mối riêng trong câu nói, có đích puzzle và trích dẫn kiểm được. Không lấy mô tả/tiểu sử/ghi chép/UI vào số thoại. Không lặp đoạn để tăng số từ.
3. NPC xuất hiện theo tiến trình; tối đa hai người tương tác/phòng. Tách lần gặp bằng đường đi, nhiệm vụ và cảnh yên. Kiểm nhịp thực với người chơi trước khi khẳng định hiệu quả cảm xúc.
4. Puzzle chỉ playable khi có map reachable, manh mối thực, điều khiển thích hợp, hậu quả, ba cấp gợi ý, skip, save roundtrip và route test qua input.
5. Mỗi đợt chạy audit, tests, route, render kiểm đọc và build Windows. Ghi rõ kết quả tự động và điều chưa kiểm bằng người.

## Hệ thống cần nối khi mở chương

C02/C03: gương/ánh sáng, ảnh báo có đồng thuận, chuông ngõ, lịch tàu, cần ray và đường vòng. C04/C05: radio hai kênh có phụ đề tương đương, địa chỉ bị xóa, hầm có quy tắc, hai phiên bản làng, VHS và phỏng vấn. Giữ niên đại 1998: Akai Heya là tiền thân VHS hư cấu.

C06/C07: gắn `finale_ready`, `consent`, `corroborated`, `responsibility`, `public_hearing`, `sixth_name`, `original_tape` vào nhiệm vụ và hành động thật; năm ending đạt từ campaign, không fixture. Giữ ending C không cần sưu tập hết. Kiểm 50 số phận nhân vật theo năm nhánh, không gọi preview là kết thúc đã triển khai.

Các đợt tiếp cũng phải sửa phân bổ puzzle hiện 16/25/17/24/18 về yêu cầu gốc 35/20/20/15/10; hoàn thiện lịch/quest của những người chưa xuất hiện, tin đồn nhiều NPC, side-view và đổi nhân vật, chase/cutscene, tạo hình riêng, sound design, dịch Anh/Nhật. Đánh giá văn hóa và chơi thử trên Windows/iGPU thực còn cần trước phát hành.
