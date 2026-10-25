# Game Design Document · phiên bản sản xuất 0.1

## Định hướng và phạm vi

Tên quốc tế The Forgotten Voices. Tên Nhật 忘れられた声. Repo 3DPsychocal là tên kỹ thuật, không đổi yêu cầu 2D thành 3D. V2 thay V1 khi mâu thuẫn: Ren về vì mẹ và căn nhà; mục tiêu dài hạn 100 câu đố, 25 nhân vật, 5 ending, tuyến 9–12 giờ. Đây là ngân sách sản xuất, chưa phải thời lượng của bản 0.1.

Ba trụ cột: đời sống có người để quan tâm; chứng cứ có thể kiểm tra nhưng lời kể không toàn tri; sợ hãi đến từ quyền quyết định ai được ghi nhớ. Không dùng combat/level grind. Không có chỉ số chẩn đoán tâm thần. Fear, Guilt, Clarity là trạng thái kể chuyện.

Vòng chơi: tới địa điểm nhỏ → nói chuyện / xem đồ vật → ghi nhận thông tin → đối chiếu → quyết định phạm vi chia sẻ → môi trường hoặc quan hệ đổi → có một khoảng yên trước sự kiện kế tiếp. Người chơi không phải đoán điều tác giả giấu: mỗi puzzle có ít nhất hai dữ kiện và ba cấp gợi ý.

## Cấu trúc truyện

| Phần | Nội dung, cơ chế riêng dự kiến | Tình trạng |
|---|---|---|
| Prologue | Ga, bệnh viện, mua trà, cơm nhà, TV, cassette; 8 tương tác/câu đố | Chơi được |
| I Hanako | Nhật ký bị sửa, lịch học, nhịp loa, bảng phòng trong hồi tưởng, trả lại lời chứng; 14 câu | Chơi được bằng bảng đọc/nhập đáp án |
| II Kuchisake | Quyền tự định nghĩa; gương/đèn, chọn phạm vi ảnh báo, tránh ngõ theo chuông | 14 bản thiết kế |
| III Teke Teke | Con người ngoài giá trị lao động; lịch tàu, âm bánh, cần ray, đường vòng an toàn | 14 bản thiết kế |
| IV Inunaki | Xóa địa chỉ không xóa con người; radio hai kênh, hộ tịch, đường hầm có quy tắc | 16 bản thiết kế |
| V Akai Heya | Phỏng vấn dẫn dắt, VHS và hồ sơ; công khai sự thật khác phơi bày riêng tư | 16 bản thiết kế |
| VI Người thứ sáu | Tổng hợp nguyên nhân, đồng thuận, cộng đồng và trách nhiệm | 18 bản thiết kế |
| Epilogue | Năm biến thể có cảnh và số phận ít nhất mười người | Preview, chưa gắn campaign |

Lịch thời lượng mục tiêu giữ nguyên V2: 40/90/85/90/110/110/120/25 phút; tổng 670 phút. Không thêm delay để đạt giờ. Chỉ sau playtest người thật mới dùng con số thời lượng trong trang phát hành.

## Thiết kế phân đoạn chơi được

Ren đến ga, kiểm tra vé cửa hai, qua phố tới phòng mẹ. Người chơi có thể trò chuyện ngoài thứ tự. Câu đố đầu bệnh viện được mở sau vé; mua trà/pin sau lời dặn; ăn cơm và nghe cassette tại nhà. TV cải chính ngày trường đóng cửa. Thông báo chuyến 16:10 và khóa Đông mở lối trường.

Trường có hai hàng điểm quan sát và lối đi rộng; bàn và tủ có collision, không dùng hành lang trống kéo dài. Các giấy tờ trên bàn là cách tương tác hiện tại. Các cơ chế dây loa/gương/radio chuyên biệt cần bản điều khiển trực quan ở các đợt sau; phiên bản này chủ yếu dùng nhập mã và suy luận chọn đáp án.

P014 yêu cầu người chơi thực sự dùng M trong trường rồi mới trả lời, trừ khi dùng hỗ trợ. P018 chấp nhận hai quyết định: chọn lời giáo viên làm Ren mang thêm guilt; giữ hai bản cho phép nghe lời trẻ. Cả hai vẫn kết thúc chương, không trừng phạt bằng softlock. P021 rút chốt diễn đạt sửa hành động của Ren, không tuyên bố một hành động tốt xóa trách nhiệm.

P022 kết thúc phân đoạn với bản sao gửi cho Yui có đồng thuận. UI ghi rõ dừng ở bản sản xuất 0.1. Không đưa người chơi vào chapter rỗng.

## Hệ thống

- **State manager:** mode độc quyền menu/play/dialogue/puzzle/journal/ending; simulation chỉ cập nhật khi play. Chữ không bị thời gian truy đuổi ép đọc.
- **Di chuyển:** 72 px/s; Shift 108 px/s, vector chéo chuẩn hóa; bước collision tối đa 3 px ngăn xuyên tường khi frame chậm. Camera theo mượt có giới hạn bản đồ.
- **Tương tác:** bán kính 39 px, chọn điểm gần nhất. Portal có điều kiện tiến trình, vật phẩm không tiêu hao.
- **Puzzle registry:** `status=playable|designed`; cả hai đều có thiết kế, chỉ playable được runtime kích hoạt. `requires` là AND. Graph không chu kỳ; phần optional tương lai cần `any_of`, chưa triển khai.
- **Gợi ý:** H tăng ba cấp, sai không trừ vật phẩm. F sau ba lần sai ghi `assisted`; vẫn được nghe đoạn kết. Không yêu cầu chơi giỏi để hiểu chuyện.
- **Nhật ký:** ghi chép tự nhiên, lời thoại đã nghe, tài liệu, quan hệ theo cảm nhận, việc đang làm. Các internal links không bật thông báo “Clue Discovered”.
- **Đối chiếu:** E007+E015 cho mâu thuẫn vé/lời khai; E011+E018 cho nét chữ sửa và lựa chọn giữ hai lời kể. Cặp sai lưu giả thuyết không khóa; cặp đúng chỉ tăng clarity một lần.
- **Ký ức:** cassette mở M; palette và bảng y tế/nhà kho đổi. Đây là một quan sát được thiết kế, không shuffle map tùy tiện. Chưa triển khai hệ thống điều khiển nhân vật khác.
- **Quan hệ:** sáu trường trust/familiarity/resentment/dependence/knowledge/willingness. Lắng nghe và truyền lời có hậu quả khác; mỗi cuộc hội thoại nhận hiệu ứng một lần. UI không hiện mọi số. Dependence có lưu trữ, chưa có tuyến thay đổi trong slice.
- **Lịch NPC:** chiều/tối/đêm/rạng sáng tiến theo P004/P008/P022; Yui đổi vị trí ban đêm, Mio chỉ xuất hiện sau P018. Không phải hệ mô phỏng 24 giờ. Các lịch cho 25 hồ sơ là dữ liệu kế hoạch cần viết riêng.
- **Rumor:** cờ lan truyền và oán giận có tác dụng trong slice; mạng lan tin qua nhiều NPC chưa triển khai.
- **Fear:** tăng khi sai/xuất hiện, tự dịu theo thời gian; Guilt từ lựa chọn; Clarity từ chứng cứ. Chưa có toàn bộ phản ứng âm/hình theo ba trục.
- **Save:** JSON schema 1, đường dẫn người dùng; ghi tạm/fsync/replace; danh sách ID, dữ liệu số và quan hệ được kiểm tra. Không sửa save hỏng âm thầm. Autosave chuyển phòng, giải đố, hết thoại, thoát khi đã có tiến trình.
- **Âm thanh:** PCM mono 22.05 kHz; motif có sáu nốt, các chương đầu thiếu nốt cuối. `sixth_name.wav` hoàn chỉnh dùng trong preview. Synth chưa thay thế sound design sản xuất.

## Ending rule precedence

Đầu tiên cần `finale_ready`. Slice không đặt cờ này; UI preview dùng nội dung riêng, không làm giả tiến trình.

| Ưu tiên | Ending | Điều kiện |
|---:|---|---|
| 1 | D Sixth Name | sixth_name + consent + original_tape |
| 2 | E Town That Remembers | ≥5 willing NPC + public_hearing + corroborated |
| 3 | C Forgotten Voices | corroborated + responsibility + consent |
| 4 | B Price of Memory | clarity ≥12 + responsibility |
| 5 | A Convenient Truth | Các trạng thái còn lại khi finale_ready |

D không phải “tốt nhất”: giữ tên theo mong muốn riêng làm cộng đồng thiếu một lời giải công khai. E không xóa tranh luận. C không cần đủ mọi vật phẩm. Trước tích hợp campaign phải tạo nhiệm vụ thật gắn từng cờ, kiểm thử lời chứng riêng và điều kiện optional không chặn C.

## UX, tiếp cận và chất lượng

480×270 nội bộ; scale nguyên bằng nearest-neighbor, viền đen khi cửa sổ không chia hết. Chữ font Noto raster không làm mịn; tiếng Việt đầy đủ. Logo Nhật được raster một lần từ font CJK có giấy phép. Chưa có bản dịch UI tiếng Anh/Nhật.

H không hạn chế thời gian, phụ đề nhịp gõ tương đương âm thanh. Không đánh lừa người chơi bằng gợi ý vô căn cứ. Chớp/rung mặc định giảm, scare có thể tắt, âm lượng đỉnh WAV giới hạn. Trong bản 0.1 không có gore; không cộng tùy chọn dự phòng vào số cảnh đã làm.

Để chấp nhận bản thương mại cần: playtest đủ tuyến và ending không dùng cheat; timing logging cả thoại/cutscene (bộ đếm hiện tại chỉ thời gian tự do); review văn hóa/logic; art nhiều dáng và biểu cảm riêng; kiểm tra iGPU, controller, resize/fullscreen trên máy thật; localization; Windows package sạch và antivirus false-positive review nếu có bằng chứng phát sinh.
