# QA — bản sản xuất 0.2

Ngày 26/10/2026 UTC. Local: Linux x86_64, Python 3.12.14, Pygame CE 2.5.8, SDL 2.32.10. Render/audio kiểm bằng SDL dummy; chưa có playtest người thật hoặc kiểm tai nghe/loa.

## Kết quả local

- **55 tests passed**, junit.xml. Bao gồm graph/dữ liệu, tiến trình, lựa chọn, skip, save roundtrip/corruption, chống cộng quan hệ khi nghe lại, gates hội thoại, anchor hai manh mối, bắt chu kỳ thoại, chín mô hình nhập liệu, nhịp cần khoảng nghỉ, chốt cần đúng thứ tự, ghi chép bắt buộc, ẩn gợi ý, schema migration và giữ backup.
- **Tuyến input đầy đủ đã qua:** 16 maps, 22 puzzles, 44 điểm ghi chép, cả 59 cảnh thoại live và 13.777 đơn vị lời thoại tiếp cận được. Đi theo collision bằng World.update; mở cổng/NPC/vật chứng bằng E; nhập thao tác bằng Game.handle; P014 dùng M trong kho; lưu và nạp lại trạng thái cuối. ui_route.json ghi từng puzzle. Thời gian script không phải thời lượng người chơi.
- **Kiểm đếm:** 76 cuộc thoại viết, 59 live; 16.586 written/13.777 playable whitespace units. Mở đầu 6.176, Hanako 7.601. Không có dòng thoại live trùng nhau. 25 hồ sơ, 11 người có cảnh live. 100 puzzle designs/22 playable; 125 cross edges thiết kế. 88 tài nguyên có hash, 16 maps khác ảnh và layout.
- Mỗi cuộc thoại có hai trích dẫn tại dòng nói cụ thể và hai đích puzzle khác nhau; audit kiểm anchor, ID và khả năng mở chuỗi cảnh. Điều này không thay review chất lượng liên hệ bằng người.
- Mọi hotspot/cổng hiện hành được kiểm có đường tiếp cận, spawn không nằm trong vật cản. Tuyến thực đi đủ mọi cảnh nên không chỉ kiểm trường hợp đã mở sẵn.
- Render mọi trang thoại và màn hình; kiểm chiều rộng chữ và số dòng puzzle. Đã xem ảnh runtime của nối dây, tiệm, thoại và các màn khác để kiểm đọc và bố cục. Ảnh reports không phải mockup.
- Source khởi động headless **120 frames** thành công. Compiler thoại chạy lại giữ nguyên số cảnh và số từ. Validator và audit cấu trúc không lỗi; các cảnh báo chưa đủ scope được giữ nguyên.
- `narrative_audit.py --release` chưa đạt và phải trả lỗi: sáu chương, các maps/thoại/puzzles còn thiếu, năm campaign ending chưa hoàn thiện. CI giai đoạn chạy structural audit, không bỏ dấu chưa hoàn thành full release.

## Packaging

<!-- CURRENT_BUILD -->
CI của commit 0.2 đang chờ chạy; không dùng artifact 0.1 làm bằng chứng cho bản này. Kết quả build Windows và smoke-test EXE thật sẽ được cập nhật sau khi workflow hoàn tất.
<!-- /CURRENT_BUILD -->

Lịch sử 0.1: run 40203737430 đã qua Ubuntu/Windows và EXE 60 frames; code commit 1cfc56fa87bf24233540fdadc85723895769e00e. Lỗi path separator Windows ở lượt trước đó đã sửa bằng Path.as_posix(); test này được giữ. Đây là bằng chứng lịch sử, không thay kiểm bản 0.2.

## Giới hạn chưa được chứng minh

Chưa có chơi thử bởi người để đánh giá nhịp, độ khó, cảm xúc, mệt khi đọc, logic liên hệ sâu và chất lượng văn hóa. Chưa có full campaign/năm ending kiếm được. Chưa benchmark iGPU 60 FPS, kiểm Windows desktop/fullscreen/focus/Unicode hoặc âm thanh thiết bị thật. Script route/headless/EXE smoke không đại diện các kiểm này. Chưa đủ 45.000–50.000 lời thoại tổng; không còn dùng thời lượng 9–12 giờ làm cổng theo yêu cầu mới.
