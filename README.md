# 3DPsychocal · 忘れられた声

> Đang nâng cấp theo hai prompt 0.3/0.3.1. [Trạng thái triển khai mới](docs/UPGRADE_031_STATUS.md): 24 maps, trường ba tầng với hai cầu thang, biển Nhật đọc được, chuyển cửa có fade, sương mép ngoài trời, thoại một lần và đèn pin có occlusion. 62 tests local đã qua. Chưa đạt nghiệm thu 0.3.1; các số liệu và gói Windows 0.2 bên dưới là mốc nền.

**Wasurerareta Koe / The Forgotten Voices / Những Tiếng Nói Bị Lãng Quên**

Game kinh dị tâm lý **2D pixel art**, Python 3.12 + Pygame CE, chạy offline. Tsukimori, tháng 10 năm 1998. Ren về quê thăm mẹ nhập viện và giải quyết giấy tờ căn nhà. Anh chỉ xin nghỉ ba ngày.

![Hành lang Tsukimori](reports/menu.png)

## Bản sản xuất 0.2 — mở rộng Mở đầu và Hanako

Đợt này hoàn thiện nội dung của **hai chương đầu**, theo yêu cầu chia mỗi đợt 2–3 chương. Mỗi chương có **8 bản đồ**, hội thoại mở dần theo sự kiện và vật chứng nằm trong thế giới. **Chưa phải toàn bộ game 8 chương.** Yêu cầu mới ngày 26/10/2026 thay mục tiêu thời lượng bằng 45.000–50.000 từ lời thoại cho toàn dự án; ngân sách biên soạn là 50.000 đơn vị cách trắng, không dùng thời gian chờ để kéo dài game.

| Hạng mục | Đã viết / thiết kế | Chơi được trong 0.2 |
|---|---:|---:|
| Chương, gồm mở đầu và kết | 8 trong kế hoạch | 2 |
| Bản đồ riêng có collision và lối nối | 16 | 8 Mở đầu + 8 Hanako |
| Hội thoại | 76 | 59 |
| Lời thoại theo khoảng trắng | 16.586 | **13.777**, không trùng dòng |
| Theo chương | — | Mở đầu 6.176; Hanako 7.601 |
| Nhân vật có hồ sơ / vai trò | 25 | 11 người có cảnh thoại |
| Câu đố liên kết | 100 | 22 (P001–P022) |
| Manh mối quan sát tại phòng | 44 | 44; mỗi câu đố cần hai ghi chép |
| Kết thúc | 5 quy tắc + phân cảnh xem thử | Chưa đạt qua campaign |

Số lời thoại chỉ đếm nội dung nhân vật nói, **không tính tên người nói, UI, tiểu sử, mô tả, manh mối đồ vật hay lượt nghe lại**. Tiếng Việt được đếm theo khoảng trắng, không phải tách từ ngôn ngữ học. Mọi cuộc thoại có ít nhất hai manh mối được gắn vào câu nói cụ thể và liên kết tới hai puzzle ID khác nhau. Kiểm tra cấu trúc tự động không thay việc biên tập chất lượng suy luận.

**Phần còn lại:** sáu chương, ít nhất 48 bản đồ, 78 câu đố triển khai, phần lời thoại còn thiếu tới 45.000–50.000, năm ending đạt bằng hành động thật. Chưa có chase, side-view/đổi nhân vật, dịch Anh/Nhật, âm thanh và tạo hình 25 người đạt cấp phát hành. Quota loại puzzle 35/20/20/15/10 vẫn cần điều chỉnh. Xem [yêu cầu](docs/REQUIREMENTS.md) và [lộ trình](docs/ROADMAP.md).

## Tải và chạy

[Tải toàn bộ mã nguồn ZIP](https://github.com/Hero-Entertainment114/3DPsychocal/archive/refs/heads/codex/forgotten-voices-stage1.zip) · [Nhánh bàn giao](https://github.com/Hero-Entertainment114/3DPsychocal/tree/codex/forgotten-voices-stage1).

<!-- WINDOWS_BUILD -->
**[Tải Windows mới nhất — đợt nâng cấp trường ba tầng](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40319219417/artifacts/12647803477)** · [CI thành công](https://github.com/Hero-Entertainment114/3DPsychocal/actions/runs/40319219417). Giải nén toàn bộ rồi mở `3DPsychocal.exe`, giữ `_internal`. Đã build và smoke-test EXE 60 frames trên Windows; chưa phải nghiệm thu đầy đủ v0.3.1 hay playtest bằng người. Cần đăng nhập GitHub để tải artifact.
<!-- /WINDOWS_BUILD -->

Chạy từ source với Python **3.12 hoặc 3.13**:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Windows có thể dùng `run_windows.bat`. Sau khi cài thư viện, game không cần mạng, tài khoản hay API. PNG, WAV, font, atlas và giấy phép nằm sẵn trong repo; không cần sinh lại tài nguyên để chơi.

## Điều khiển

| Phím | Tác dụng |
|---|---|
| WASD / mũi tên, Shift | Đi, chạy |
| E / nhấp trái khi đứng gần | Nói chuyện, xem vật, đi qua lối ra |
| Enter; 1 / 2 ở cuối thoại | Tiếp trang; chọn phản hồi |
| J; ← →; ↑ ↓ | Sổ tay; đổi mục; đổi trang |
| Space / C trong mục Chứng cứ | Chọn hai tài liệu / ghép giả thuyết |
| Tab trong thế giới | Túi đồ |
| M | Hiện tại / hồi tưởng sau khi nghe cassette; dấu vết P014 ở kho trường |
| H / Tab trong câu đố | Tăng gợi ý / ẩn bảng gợi ý |
| F sau ba lần thử sai | Bỏ qua có ghi nhận, không khóa truyện |
| F5 / F9 | Lưu / tải trang 1–3 |
| Esc | Khép bảng / tạm dừng |

Mỗi cơ chế hiển thị phím riêng: giỏ hàng, cực pin, chuỗi số, dây loa, nhịp gõ có khoảng nghỉ, ba vòng khóa, đếm ảnh, chọn cửa, kéo chốt. Những câu suy luận còn lại dùng nhập/chọn đáp án. Cần xem hai ghi chép trước khi giải; biết mã trước không thay việc khám phá. H chỉ vị trí ghi chép còn thiếu. Thoại có thể nghe lại nhưng không cộng quan hệ nhiều lần.

Phím E/J/Tab/M có thể đổi trong Thiết lập. `Chọn chương` chỉ mở Hanako khi autosave hoàn thành mở đầu. Sau P022 có thể tiếp tục trò chuyện và quay lại các phòng, hoặc xem ending thử trong Tư liệu.

Save ở `%LOCALAPPDATA%\3DPsychocal` (Windows), `~/.local/share/3DPsychocal` (Linux), hoặc `--user-dir PATH`. Autosave + ba trang thủ công, ghi nguyên tử. Save schema 1 của 0.1 được kiểm tra rồi chuyển sang schema 2, giữ bản `.v1.bak`, đặt Ren tại lối vào an toàn. Save hỏng được báo và giữ nguyên.

Tiếp cận: phụ đề nhịp gõ, giảm xuất hiện bất ngờ, giảm mưa chuyển động, CRT tùy chọn, âm lượng và toàn màn hình. Chưa có lồng tiếng, gore hay chớp mạnh; các tùy chọn tương ứng là dự phòng.

## Kiểm thử và công cụ biên soạn

```sh
python -m pip install -r requirements-dev.txt
python tools/compile_dialogues.py
python tools/validate_content.py
python tools/narrative_audit.py
python -m pytest -q
python tools/playtest_route.py
python main.py --headless --frames 120 --user-dir work/smoke
```

`narrative_audit.py --release` **cố ý trả lỗi** cho đến khi đủ 8 chương, mỗi chương 8 maps, 45.000 lời thoại chơi được không trùng dòng, 25 tiểu sử, 100 câu đố chơi được, 5 ending campaign và hai manh mối mỗi thoại. CI của đợt sản xuất chạy audit cấu trúc, không che những điều kiện phát hành còn thiếu.

`build_windows.bat` tạo `dist/3DPsychocal/3DPsychocal.exe` cùng `_internal`; giữ toàn bộ thư mục. CI chạy test trên Ubuntu/Windows, PyInstaller Windows và smoke-test EXE thật. [QA](reports/QA.md) phân biệt kiểm tự động với playtest người thật. `tools/package_source.py` đóng ZIP loại cache, save, venv và build.

## Nội dung và tài nguyên

- `core/`, `systems/`, `scenes/`: game loop, UI, collision, tiến trình, quan hệ, âm thanh, lưu game.
- `data/story/*.vi.txt`: kịch bản mới có thể biên tập; `compile_dialogues.py` biên dịch vào `dialogues.json`.
- `data/`: 8 chapter records, 100 puzzle designs, 25 hồ sơ, 76 hội thoại, 16 maps, 44 ghi chép, quests, truth matrix, 5 ending previews.
- `assets/`: 88 tệp sprite/portrait/props/map/menu/audio/font/licenses/atlas; manifest SHA-256.
- `docs/`: [GDD](docs/GDD.md), [Story Bible](docs/STORY_BIBLE.md), prompt gốc, CSV và graph câu đố, lộ trình.
- `reports/`: kiểm đếm, kiểm thử, ảnh từ runtime và bằng chứng build.

Code, nội dung gốc, PNG vẽ bằng công cụ Python và WAV tổng hợp dùng [Apache-2.0](LICENSE). Font Noto dùng SIL OFL. `tools/build_world_art.py` tái tạo 16 bản đồ; `tools/generate_assets.py` tái tạo toàn bộ bộ tài nguyên gốc.

Alpix đã mở canvas nhưng không cung cấp file xuất; AutoSprite tạo bản ghi Ren nhưng chưa trả ảnh. **Runtime chưa dùng tài nguyên từ hai plugin này**; [nguồn gốc tài nguyên](docs/ASSET_PROVENANCE.md) ghi rõ kết quả thực. Tsukimori/Kiroku là hư cấu; truyền thuyết là chất liệu kể chuyện.
