# Nâng cấp theo prompt 0.3 và 0.3.1 — phần nền tảng

Ngày 26/10/2026, giờ Việt Nam. Đây chưa phải bản nghiệm thu v0.3.1.

Đã tích hợp trực tiếp vào game: điểm vào đối ứng cho mọi portal, ID exit/entrance và hướng sau khi chuyển phòng; không còn tên phòng ở góc màn hình, nhãn đích nổi hay dấu chấm than puzzle; hội thoại hoàn tất không được khai thác lại, lịch sử vẫn có trong sổ; đèn pin nhặt trên quầy tiệm sau mua đồ, L bật/tắt, lưu trạng thái; chùm sáng giới hạn và suy giảm, tile tường/bàn che sáng, lightmap cache. Đèn hiện đi kèm pin; chưa có hệ ghép vật phẩm. Ánh sáng mới chỉ áp dụng nội thất trường, chưa phải hệ point-light toàn thế giới. Sprite cầm đèn chưa có.

Kiểm tự động: 58 tests; tuyến input vẫn đi qua 16 maps, 22 puzzles, 44 ghi chép và 59 hội thoại. Test riêng cho portal hai chiều, vật cản ánh sáng, nhặt một lần, lưu công tắc và ngăn hỏi lại. Chưa benchmark iGPU hoặc playtest người thật. Script route chứng minh tiến trình, không chứng minh puzzle đã được thiết kế lại.

Còn phải triển khai trước nghiệm thu: thay toàn bộ câu hỏi/nhập đáp án bằng hành động môi trường; item-use/combine/giao nhận/đẩy vật; trường nhiều tầng với cầu thang thật; lịch NPC/A*/hoạt động/đi qua cửa; NPC nền và giao thông; transitions và fog; vẽ lại sprites/portraits/maps ở độ chi tiết mới; render 960×540; biển Nhật/font và bảng thuật ngữ; horror director, Hanako và sự kiện; biên tập thoại/menu. Các prompt gốc nằm tại BRIEF_V03.txt và BRIEF_V031.txt. Không coi portal đối ứng là đã đáp ứng kiến trúc trường liên thông.

Alpix đã mở canvas chung 256×256; không có công cụ xuất PNG/atlas được cung cấp. Không ghi đè canvas chung để giả làm tài nguyên repo. AutoSprite đã kiểm tra lại Ren: characterImage=null, spritesheets=[]; chưa có asset tải được. Không gọi sprite đang dùng là sản phẩm hai dịch vụ này.

Bản Windows liên kết trong README là 0.2 đã kiểm chứng, không phải bản nâng cấp này. Source ZIP của nhánh chứa các sửa đổi mới; CI tiếp theo sẽ kiểm build của commit mới riêng.
