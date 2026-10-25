> **Current development status:** see [PROJECT_STATUS.md](PROJECT_STATUS.md). Four-language draft, 20 main + 6 side puzzles; not a completed 4–6 hour game.

# Bến Không Tên / The Nameless Wharf

Trò chơi điều tra 3D ngôi thứ nhất, lấy bối cảnh một xóm ven sông hư cấu ở Việt Nam năm 2008. Ngôn ngữ mặc định **Tiếng Việt**, đổi **English** tại Cài đặt → Ngôn ngữ. Tất cả chương, manh mối, câu đố, lời thoại, gợi ý và kết thúc có hai bản ngữ.

**Trạng thái:** bản phát triển chơi được với mạch truyện ngắn đi từ đầu đến cuối. Có 5 khu vực, 20 câu đố, 3 kết thúc; chưa phải sản phẩm hoàn thiện 4–6 giờ trong yêu cầu sản xuất. Xem [TEST_REPORT.md](TEST_REPORT.md) và [docs/PRODUCTION_BACKLOG.md](docs/PRODUCTION_BACKLOG.md). Không có Windows EXE đã được xác minh trong gói nguồn này.

## Chạy từ mã nguồn

Máy phát triển cần Python 3.12 64-bit và trình điều khiển OpenGL:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python run_game.py
```

Không cần mạng trong lúc chơi. Công cụ tạo tài nguyên cũng chạy offline. Không có tài khoản, API hay telemetry. Hai kỹ năng Lux3D và Build 3D Game Rooms đã được đọc. Chưa gọi dịch vụ tạo mesh: người dùng chưa có tài khoản Lux3D, không có khóa hoặc ngân sách dịch vụ. Bộ chạy riêng Lux3D đã cài; tài liệu body.md của plugin không đọc được. Xem hồ sơ đề xuất Blender tại production/room-review/review.html.

## Cách chơi

- WASD di chuyển, chuột nhìn, Shift chạy, C giữ để ngồi; phím mũi tên nhìn thay chuột.
- Đến gần trang giấy, nhân vật, bàn điều tra hoặc cửa và nhìn vào chúng, nhấn E.
- J mở nhật ký, B mở bảng suy luận, M xem sơ đồ. Chứng cứ thu được tự lưu.
- Mỗi khu vực có ba tờ chứng cứ và bốn câu đố theo thứ tự. Câu đố thiếu dữ kiện sẽ liệt kê vật chứng cần tìm. Nút Gợi ý có hai cấp, không trừ điểm.
- Hoàn tất bốn câu đố rồi tới cửa có dấu mũi tên để sang chương. Sau chương 5, cửa mở lựa chọn kết thúc.
- Xin phép Hạnh và Lan trích lời để mở phương án cùng công bố. Nhật ký → Gặp lại nhân chứng cho phép trở lại hội thoại mà không mất tiến trình.
- Esc mở menu; F5 lưu ô 1, F9 tải ô 1. Menu hỗ trợ ba ô lưu tay và tự lưu.
- Lưu dưới `%LOCALAPPDATA%\BenKhongTen` trên Windows, `~/.local/share/BenKhongTen` trên Linux. Bản `.bak` được dùng khi bản chính hỏng.

Cài đặt: ngôn ngữ, góc nhìn, độ nhạy chuột, âm lượng chung, rung bước chân, độ sáng, giới hạn FPS, độ phân giải, toàn màn hình và cỡ chữ. Low/Medium/High hiện điều chỉnh khoảng nhìn; chưa phải hệ thống LOD đa cấp.

## English

A first-person investigation game in a fictional Vietnamese riverside neighbourhood in 2008. Vietnamese is the default; choose **Cài đặt → Ngôn ngữ** to switch to English. All story and interface text is bilingual. This is a short playable development build with five chapters, twenty puzzles and three endings, not the requested finished 4–6 hour commercial game.

Install Python 3.12 and the pinned requirements, then run `python run_game.py`. Player releases are built on Windows using `tools\build_windows.bat`; players of that build do not need Python. Windows execution is **not yet tested**. See BUILD_INSTRUCTIONS.md.

WASD move, mouse or arrow keys look, E interact, Shift run, C crouch, J evidence journal, B deduction board, M map, Esc menu, F5/F9 quick save/load. Read all three clues per area, solve the four deductions, then use the arrow-marked door. Consent can be revisited through the journal. The audio puzzle has a full text transcript.

## Development

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
# Linux headless render validation:
EGL_PLATFORM=surfaceless XDG_CACHE_HOME=/tmp/game-cache python tools/render_validation.py /tmp/ben-validation
```

`source/core.py` is engine-independent state/save logic; `source/main.py` handles input and UI; `source/world.py` builds original textured geometry. `data/story.json` contains authored bilingual narrative. `tools/create_content.py` is its editable authoring source. `tools/generate_assets.py` creates six textures and five WAVs using a fixed seed. Assets are included; regeneration is optional. Use the current checkout; cloud tasks are already isolated and need no extra Git worktree.

## Bổ sung bản 0.2

I mở kho vật chứng để xoay/lật trang giấy 3D. B → Ghim & liên kết chứng cứ: kéo thanh chấm của thẻ, chọn hai thẻ để kiểm tra liên hệ; có thể chọn thẻ ở các trang khác nhau. Menu có chọn chương đã mở; chế độ chơi lại giữ nguyên bản lưu cốt truyện. Cài đặt bổ sung âm lượng riêng, phụ đề môi trường và đổi phím di chuyển/tương tác.

Ngăn hồ sơ chương 4 cần chìa khóa từ hộp bánh quy; dùng chìa để trượt ngăn ra và lấy bản nháp. Nhạc thay đổi giữa menu, các chương và kết thúc.

[Đối chiếu đầy đủ yêu cầu và phần chưa đạt](docs/REQUIREMENTS_STATUS.md) · [Bố trí Blender chờ duyệt](production/room-review/review.html).

## Bổ sung bản 0.3

Trong hội thoại, chọn **Hỏi thêm về chuyện cũ** để đọc 15 cuộc trò chuyện mới ở hai ngôn ngữ. Lịch sử đọc được lưu. Năm tệp Blender có vật liệu/ánh sáng và 40 góc xem nằm trong `production/form-review`; bố trí đã được duyệt, bước Form và xuất sang runtime chưa được duyệt. Chúng chưa thay thế các cảnh phát triển đang chạy. Gói mới nhất do `tools/package_source.py` tạo là `dist/BenKhongTen_Project_Source_v0_3.zip`.

## Version 0.4

Settings cycles through Vietnamese, English, Japanese and Simplified Chinese. Japanese/Chinese are complete offline machine-translation drafts pending editorial review. Two optional dossier side stories unlock in chapters 2 and 4, with six additional puzzles and saved progress. The source archive is `dist/BenKhongTen_Project_Source_v0_4.zip`; GitHub Code → Download ZIP includes all committed sources and assets.
