# Sản xuất tiếp tục từ bản 0.1

Không thay giai đoạn chưa làm bằng ID hoặc đường dẫn rỗng. JSON luôn giữ `status` để phân biệt designed/written/playable.

1. **Đánh giá slice:** người chơi mới hoàn thành 22 câu, ghi thời gian theo hoạt động, lỗi và chỗ không hiểu. Chỉnh nhịp đời sống trước khi mở rộng. Không mặc định slice đã đạt 20–30 phút.
2. **Mở rộng cơ chế:** thay bảng câu hỏi ở P012/P013 bằng dây nối/nhịp gõ trực tiếp có hỗ trợ bàn phím; trò chơi gương, ánh sáng, radio, route loop, chase có checkpoint. Kiểm thử tiến trình vẫn dùng Progression nhưng UI scene chuyên biệt.
3. **Chương II và III:** thực hiện P023–P050, thêm phòng khám/ký túc/ga phụ. Viết lịch NPC riêng theo sự kiện; thêm side quest sửa radio, quan hệ gia đình và khả năng không công bố ảnh. Chỉ đổi `status` sau khi có interaction, map và route test.
4. **Chương IV và V:** P051–P082, hầm/2 phiên bản làng/kho/bệnh viện cũ. Không gian lặp phải có quy tắc chỉ đường từ journal và đường quay lại an toàn. Dùng audio hai kênh thật + phụ đề tương đương.
5. **Chương VI và epilogue:** P083–P100, nối cờ finale_ready/consent/corroborated/responsibility/public_hearing/sixth_name/original_tape bằng hành động thật. Năm ending chạy từ campaign, không dùng fixture. Optional không khóa ending C.
6. **Nội dung:** mở rộng dialogue lên mục tiêu 25–40 nghìn đơn vị cách trắng với người biên tập; sửa phân bổ loại puzzle (hiện không đạt quota); cross-link review bằng người, không lấy graph không chu kỳ làm bằng chứng tất cả suy luận hay.
7. **Art/audio/localization:** tạo dáng riêng 25 người, cutscene sprites/camera, hoạt ảnh cảm xúc, chase, UI Anh/Nhật. Asset từ AutoSprite nếu có phải lưu file/atlas thực và ghi provenance. Hoàn thiện âm thanh với người nghe kiểm.
8. **Release gate:** playtest 9–12 giờ nhanh không skip và 15–20 giờ khám phá; tất cả endings; không softlock; Unicode và controls; Windows package kiểm trên máy thật, iGPU 60 FPS, build provenance. Chỉ sau đó bỏ nhãn sản xuất.

Tiêu chí cho một puzzle chuyển playable: có map reachable, clues xuất hiện thực trong world/thoại, answer và consequence xác định, hint3/skip, save roundtrip, kiểm route bằng nhập liệu thực. Tiêu chí dialogue playable: được trigger từ NPC/sự kiện, pagination không tràn, lựa chọn tác động đúng và không farm.
