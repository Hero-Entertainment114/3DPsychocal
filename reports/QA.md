# Báo cáo QA — bản sản xuất 0.1

Ngày 25/10/2026 (Asia/Saigon). Môi trường local: Linux x86_64, Python 3.12.14, Pygame CE 2.5.8, SDL 2.32.10. Render/audio test dùng SDL dummy; không có người chơi ngồi thử hoặc thiết bị âm thanh thực.

## Đã thực hiện

- `pytest`: **35 passed** trong lần chạy ghi tại `junit.xml`. Bao gồm dữ liệu/graph, route progression, checkpoint save roundtrip, cả hai lựa chọn P018, skip sau ba lần sai, chống farm quan hệ, giả thuyết và năm rule ending, save hỏng, settings lỗi, collision và render mọi màn.
- `tools/playtest_route.py`: **22/22** bằng route scripting. BFS chọn vị trí tiếp cận; nhân vật đi qua collision bằng `World.update`, cổng được mở bằng phím E, đáp án được nhập qua `Game.handle`, memory P014 kích hoạt bằng M. Kết quả đầy đủ trong `ui_route.json`.
- Tất cả điểm tương tác, NPC và cổng được kiểm tiếp cận; mọi portal spawn không nằm trong solid tile/prop.
- `validate_content.py`: không có structural error; **có cảnh báo scope chưa đạt** được giữ trong JSON. 100 records, 22 playable, 125 cross edges, 25 profiles, 25 dialogues, 3.914 whitespace units (1.246 live), 77 tệp asset.
- Headless startup từ source: chạy thành công. Ảnh menu, town, school, dialogue, puzzle và ending preview được render từ game thật. Đã xem ảnh menu/school/dialogue để kiểm readability, layout.
- Chữ thoại được chia trang tối đa sáu dòng; test kiểm chiều rộng mỗi dòng. Puzzle prompts/clues được đo chiều cao tránh tràn input. Không có ảnh mockup thay cho ảnh chạy game.
- ZIP packager có loại cache, save, venv, build và credential; font licenses/source briefs có trong archive.

## Chưa được chứng minh

- 9–12 giờ / 15–20 giờ; 20–30 phút của slice; độ khó và cảm xúc từ người chơi thật.
- Full campaign, tất cả 100 puzzle trong gameplay, năm ending đạt qua campaign.
- 60 FPS iGPU thực; headless không phải benchmark GPU. Nhạc được tạo có tệp hợp lệ nhưng chưa đánh giá bằng tai nghe/loa.
- Windows GUI, fullscreen, focus, antivirus và Unicode trên máy người dùng. Workflow build/smoke EXE là kiểm tự động, không thay playtest desktop.
- Vòng biên tập văn hóa, 25–40 nghìn lời thoại, localization Anh/Nhật, hình thể riêng 25 người.

## Packaging

**Đã build và chạy EXE thật trên Windows CI.** [Run 40203737430](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40203737430), commit `1cfc56fa87bf24233540fdadc85723895769e00e`: cả `test (ubuntu-latest)` và `test (windows-latest)` thành công. Windows đã qua validator, pytest, scripted UI route, source startup, PyInstaller build và smoke test executable 60 frames.

[Tải gói Windows standalone](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40203737430/artifacts/12603176931) (18.881.845 bytes; SHA-256 artifact ZIP `df7fdbafee377b4ca8d88cf31733d16ad558707549e9e8729a7ee7339c6d6c18`). Giải nén toàn bộ rồi chạy `3DPsychocal.exe`; không tách thư mục `_internal`. Artifact lưu tới 23/01/2027 theo metadata GitHub. Cần đăng nhập tài khoản có quyền repo để tải.

Bản Linux đóng gói bằng PyInstaller cũng đã mở headless 60 frames ở môi trường local. Không gọi đó là kiểm thử desktop/âm thanh bằng người. Các commit tài liệu sau commit build không thay code binary.

## Lỗi đa nền tảng đã phát hiện và sửa

Run CI đầu `40203553465`: Ubuntu qua; Windows 34/35 do registry ảnh dùng dấu phân cách Windows. Renderer đã đổi sang `Path.as_posix()` để ID tài nguyên giống nhau trên cả hai hệ điều hành. Run kế tiếp `40203737430` đã qua toàn bộ trên Ubuntu và Windows; không bỏ qua bài test thất bại.
