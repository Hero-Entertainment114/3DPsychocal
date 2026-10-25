# Đối chiếu yêu cầu V1 + V2

V2 ưu tiên khi mâu thuẫn. “Có dữ liệu” không đồng nghĩa đã triển khai. Các prompt gốc giữ nguyên trong BRIEF_V1.txt và BRIEF_V2.txt.

| Yêu cầu | Trạng thái 0.1 | Bằng chứng / việc còn lại |
|---|---|---|
| Python 3.12 + Pygame CE; không Unity/Unreal | Có | requirements, main.py |
| Repo 3DPsychocal, source modular | Có | core/systems/scenes/data/tools/tests |
| Game 2D top-down | Có | Five tilemaps, world.py |
| Side-view, điều khiển nhân vật khác | Chưa | Roadmap |
| Windows EXE độc lập | Đã build + smoke test Windows CI | QA.md, run 40203737430, artifact Windows |
| Chơi không Internet/API trả phí | Có | Assets/font/WAV đóng gói, runtime không network |
| 9–12 giờ chính, 15–20 giờ mở rộng | Chưa | Không có playtest người thật; không dùng số giờ này làm quảng cáo |
| 100 câu đố được thiết kế | Bản registry ban đầu | 100 prompt/clues/answers/hints/graph; còn cần biên tập độ khác biệt |
| 100 câu đố playable, đa dạng cơ chế | Chưa | Chỉ P001–P022; chủ yếu bảng nhập/chọn + memory observation |
| Ngân sách 35/20/20/15/10 | Chưa | Thực tế 16/25/17/24/18 theo semantic tags |
| ≥30 liên kết xuyên chương | Có trong thiết kế | 125 graph edges; chưa chứng minh hiệu quả qua playtest |
| 25 hồ sơ có vai trò | Có dữ liệu | characters.json, một puzzle role/người, network quan hệ |
| 25 người có gameplay riêng | Chưa | 8 có thoại live; 17 cần scene/schedule/quest |
| ≥3.000 từ thoại tiếng Việt | Bản viết vượt sàn theo khoảng trắng | 3.914 đơn vị cách trắng, live 1.246; không phải phép tách từ ngôn ngữ học |
| ≥2 liên kết mỗi thoại quan trọng | Có dữ liệu | Validator kiểm tra ID; biên tập sâu vẫn cần |
| 25–40 nghìn thoại mục tiêu | Chưa | Mở rộng theo scenes thực, không nhân bản lời |
| Ren về vì mẹ, đời sống đầu ngày | Có phần lớn | Thăm mẹ, gặp bạn, mua đồ, về nhà/ăn/TV; không phải mô phỏng đời sống đầy đủ |
| Năm twist, mỗi twist ≥5 báo trước | Có thiết kế | Story Bible + Truth Matrix; các báo trước chương sau chưa playable |
| Nhật ký / inventory / kết hợp chứng cứ | Có | UI, 2 cặp đúng, giả thuyết sai có thể sửa |
| Fear/Guilt/Clarity | Có trạng thái | UI nội bộ và tiến trình; phần điều biến âm/hình còn hạn chế |
| Relationship 6 trục | Có nền tảng | 6 trường lưu; dependence chưa có tuyến tăng giảm |
| NPC Schedule | Có bản tối thiểu | Phase truyện, Yui đổi chỗ, Mio có điều kiện; không 25 lịch riêng |
| Tin đồn ảnh hưởng xã hội | Một phần | Cờ và resentment; mạng truyền lời nhiều người chưa có |
| 5 ending tích lũy, 10 epilogue mỗi ending | Rules + preview | 15 đoạn scene và 50 epilogue riêng, chưa đạt từ campaign |
| Cutscene sprites/camera chuyên biệt | Một phần | Scene preview có sprite; chưa cinematic timeline đầy đủ |
| Pixel artwork thật | Có tài nguyên phát triển | 77 file gồm sprite/portrait/tile/props/menu/map/audio/font/licenses/atlas |
| 25 tạo hình đạt chất lượng sản xuất | Chưa | Bộ hình thể chung cần thay bằng dáng riêng |
| Menu đầy đủ hoạt động | Có | New/Continue/Chapters/Settings/Extras/Credits/Exit, chương rỗng không mở |
| Menu đổi theo tiến trình | Một phần | Bóng sau I và tông sáng; thay đổi III–V chưa có |
| 12 địa điểm | Chưa | 5 playable; tên địa điểm tương lai chỉ là data design |
| Nhật/Viet/Anh | Việt runtime + logo Nhật | Chưa có bản dịch Anh/Nhật; không menu chọn giả |
| Font có phép, không ảnh/nhạc vi phạm | Có provenance | Noto SIL OFL, originals Apache-2.0 |
| Synth âm thanh thực | Có | WAV và generator; chưa audition/production mix |
| Jump/chase/gore vừa phải | Rất hạn chế | Một bóng xuất hiện có chuẩn bị, không chase/gore trong slice |
| Access options | Có phần triển khai | Mưa/scare/CRT/volume; flash/blood/voice dự phòng nói rõ |
| Remap/fullscreen/mouse | Có | Input handlers; kiểm thực máy Windows vẫn cần |
| Multiple saves, schema checking | Có | Autosave + 3 slot, atomic replace, preserve corrupt file |
| Asset validator / graph validator | Có | reports/content_validation.json |
| Route test start–finish | Có cho slice | tools/playtest_route.py, không gọi là human playtest |
| CI test và build | Có workflow | Trạng thái chạy thực ở reports/QA.md / Actions |
| ZIP dự án | Có công cụ + archive GitHub | tools/package_source.py |
| Game thương mại hoàn chỉnh | Chưa | Release gate ở ROADMAP.md |

Các trạng thái này là một phần của sản phẩm giao. Không được thay “designed/written/preview_only” thành “playable” chỉ để qua kiểm đếm.
