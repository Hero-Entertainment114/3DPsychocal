> Windows mới nhất: [tải gói](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40319219417/artifacts/12647803477) · [CI Ubuntu/Windows thành công](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40319219417), code `70a8a2c`. 62 tests và EXE smoke 60 frames đã qua.

> Cập nhật đợt tiếp tục 0.3.1: **62 tests local qua**, route đủ **24 maps/22 puzzles/44 notes/59 conversations**, có nhặt đèn pin. Các kiểm mới gồm đường qua hai cầu thang, không nhảy tầng, portal hai chiều, biển/đồ vật quan sát, chuyển cảnh và fog theo loại bản đồ. Chi tiết ở [trạng thái nâng cấp](../docs/UPGRADE_031_STATUS.md). Phần 0.2 dưới đây là lịch sử, không đại diện toàn bộ thay đổi mới.

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
**Windows và Ubuntu đều thành công:** [run 40257150324](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40257150324), code commit `71b285fccb1062885c86306983983edae88a8662`. Cả hai job đã qua validator, narrative audit, pytest, full input route và source startup. Windows đã qua PyInstaller build và smoke-test **EXE thật 60 frames**.

[Tải gói Windows 0.2](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40257150324/artifacts/12622788024): 19.206.435 bytes; SHA-256 artifact ZIP `572078d399283daf4f7d888319b1604ced28eccb4853b47a8cdd2c073846e049`. GitHub yêu cầu đăng nhập để tải; metadata hiện ghi hạn 24/01/2027. Giữ cả `_internal` khi giải nén. Chi tiết máy đọc được ở build_verification.json. Commit tài liệu sau code commit chỉ bổ sung bằng chứng và đường tải, không thay chương trình.
<!-- /CURRENT_BUILD -->

Lịch sử 0.1: run 40203737430 đã qua Ubuntu/Windows và EXE 60 frames; code commit 1cfc56fa87bf24233540fdadc85723895769e00e. Lỗi path separator Windows ở lượt trước đó đã sửa bằng Path.as_posix(); test này được giữ. Đây là bằng chứng lịch sử, không thay kiểm bản 0.2.

## Giới hạn chưa được chứng minh

Chưa có chơi thử bởi người để đánh giá nhịp, độ khó, cảm xúc, mệt khi đọc, logic liên hệ sâu và chất lượng văn hóa. Chưa có full campaign/năm ending kiếm được. Chưa benchmark iGPU 60 FPS, kiểm Windows desktop/fullscreen/focus/Unicode hoặc âm thanh thiết bị thật. Script route/headless/EXE smoke không đại diện các kiểm này. Chưa đủ 45.000–50.000 lời thoại tổng; không còn dùng thời lượng 9–12 giờ làm cổng theo yêu cầu mới.
