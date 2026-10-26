# Game Design Document · phiên bản sản xuất 0.2

## Định hướng và phạm vi

Tên quốc tế The Forgotten Voices. Tên Nhật 忘れられた声. Repo 3DPsychocal là tên kỹ thuật, không đổi yêu cầu 2D thành 3D. Yêu cầu tiếp tục 26/10/2026 ưu tiên ngân sách mới; V2 thay V1 ở các điểm còn lại: Ren về vì mẹ và căn nhà; mục tiêu toàn dự án 8 chương tính cả mở đầu/kết, 45.000–50.000 lời thoại, 100 câu đố, 25 nhân vật và 5 ending. Mỗi chương ít nhất 8 maps. Đợt này làm Mở đầu + Hanako; chưa hoàn thành toàn dự án.

Ba trụ cột: đời sống có người để quan tâm; chứng cứ có thể kiểm tra nhưng lời kể không toàn tri; sợ hãi đến từ quyền quyết định ai được ghi nhớ. Không dùng combat/level grind. Không có chỉ số chẩn đoán tâm thần. Fear, Guilt, Clarity là trạng thái kể chuyện.

Vòng chơi: tới địa điểm nhỏ → nói chuyện / xem đồ vật → ghi nhận thông tin → đối chiếu → quyết định phạm vi chia sẻ → môi trường hoặc quan hệ đổi → có một khoảng yên trước sự kiện kế tiếp. Người chơi không phải đoán điều tác giả giấu: mỗi puzzle có ít nhất hai dữ kiện và ba cấp gợi ý.

## Cấu trúc truyện

| Phần | Nội dung, cơ chế riêng dự kiến | Tình trạng |
|---|---|---|
| Prologue | Ga, bệnh viện, mua trà, cơm nhà, TV, cassette; 8 tương tác/câu đố | Chơi được |
| I Hanako | Nhật ký bị sửa, lịch học, nhịp loa, bảng phòng trong hồi tưởng, trả lại lời chứng; 14 câu | Chơi được trên 8 maps với thao tác và suy luận |
| II Kuchisake | Quyền tự định nghĩa; gương/đèn, chọn phạm vi ảnh báo, tránh ngõ theo chuông | 14 bản thiết kế |
| III Teke Teke | Con người ngoài giá trị lao động; lịch tàu, âm bánh, cần ray, đường vòng an toàn | 14 bản thiết kế |
| IV Inunaki | Xóa địa chỉ không xóa con người; radio hai kênh, hộ tịch, đường hầm có quy tắc | 16 bản thiết kế |
| V Akai Heya | Phỏng vấn dẫn dắt, VHS và hồ sơ; công khai sự thật khác phơi bày riêng tư | 16 bản thiết kế |
| VI Người thứ sáu | Tổng hợp nguyên nhân, đồng thuận, cộng đồng và trách nhiệm | 18 bản thiết kế |
| Epilogue | Năm biến thể có cảnh và số phận ít nhất mười người | Preview, chưa gắn campaign |

Ngân sách thoại: 6.000/7.500/7.000/6.500/7.000/7.000/6.000/3.000, tổng 50.000. Bản 0.2 có 6.176 và 7.601 ở hai chương đầu. Đếm đơn vị cách trắng của lời nói, loại UI/mô tả/tên người nói/ghi chép/lượt nghe lại. Không đặt thời lượng tối thiểu; kiểm chất lượng nhịp bằng người vẫn cần.

## Thiết kế phân đoạn chơi được

Ren đến ga, kiểm tra vé cửa hai, qua phố tới phòng mẹ. Người chơi có thể trò chuyện ngoài thứ tự. Câu đố đầu bệnh viện được mở sau vé; mua trà/pin sau lời dặn; ăn cơm và nghe cassette tại nhà. TV cải chính ngày trường đóng cửa. Thông báo chuyến 16:10 và khóa Đông mở lối trường.

Mở đầu có sân ga, sảnh vé, phố, tiệm Sakurai, sảnh bệnh viện, phòng bệnh, hiên nhà và bếp. Hanako có sân trường, tiền sảnh, lớp học, phòng giáo viên, phòng phát thanh, hành lang, kho và nhà vệ sinh. Mỗi map có layout và đồ vật riêng. Cổng theo tiến trình nối đường quay lại; khoảng đi và sinh hoạt tách lần gặp.

44 ghi chép vật lý phân bố ở các phòng. Mỗi câu đố cần hai ghi chép đã xem; gõ đúng mã trước vẫn chưa đủ. Đồ vật tương lai chỉ hiện sau prerequisites; gợi ý H chỉ phòng còn thiếu ghi chép, Tab ẩn bảng để tiếp tục thao tác. Giỏ hàng, pin, chuỗi, nối dây, nhịp gõ có khoảng nghỉ, ba vòng số, đếm ảnh, cửa và chốt có mô hình nhập liệu riêng. Các câu suy luận còn lại giữ nhập/chọn đáp án.

59 cảnh thoại live, 76 cảnh viết tổng; mỗi cảnh có hai câu trích manh mối riêng trỏ tới hai puzzle. Cảnh mở theo puzzle và thoại trước. Runtime cho tối đa hai người tương tác/phòng, ưu tiên cảnh chưa nghe; Ren tự suy nghĩ ở điểm quan sát thay vì tạo NPC Ren thứ hai. Hai tập văn bản tác giả ở data/story được biên dịch vào registry; không lấy tiểu sử thay thoại.

P014 yêu cầu người chơi thực sự dùng M trong kho trường rồi mới trả lời, trừ khi dùng hỗ trợ. P018 chấp nhận hai quyết định: chọn lời giáo viên làm Ren mang thêm guilt; giữ hai bản cho phép nghe lời trẻ. Cả hai vẫn kết thúc chương, không trừng phạt bằng softlock. P021 rút chốt diễn đạt sửa hành động của Ren, không tuyên bố một hành động tốt xóa trách nhiệm.

P022 kết thúc phân đoạn với bản sao gửi cho Yui có đồng thuận. UI ghi rõ dừng ở bản sản xuất 0.2. Không đưa người chơi vào chapter rỗng.

## Hệ thống

- **State manager:** mode độc quyền menu/play/dialogue/puzzle/journal/ending; simulation chỉ cập nhật khi play. Chữ không bị thời gian truy đuổi ép đọc.
- **Di chuyển:** 72 px/s; Shift 108 px/s, vector chéo chuẩn hóa; bước collision tối đa 3 px ngăn xuyên tường khi frame chậm. Camera theo mượt có giới hạn bản đồ.
- **Tương tác:** bán kính 39 px, chọn điểm gần nhất. Portal có điều kiện tiến trình, vật phẩm không tiêu hao.
- **Puzzle registry:** `status=playable|designed`; cả hai đều có thiết kế, chỉ playable được runtime kích hoạt. `requires` là AND. Graph không chu kỳ; phần optional tương lai cần `any_of`, chưa triển khai.
- **Gợi ý:** H tăng ba cấp; Tab ẩn bảng và giữ cấp đã đọc; mở lại câu đố bắt đầu bằng bảng thao tác. Sai không trừ vật phẩm. F sau ba lần sai ghi `assisted`; vẫn được nghe đoạn kết. Không yêu cầu chơi giỏi để hiểu chuyện.
- **Nhật ký:** ghi chép tự nhiên, lời thoại đã nghe, tài liệu, quan hệ theo cảm nhận, việc đang làm. Các internal links không bật thông báo “Clue Discovered”.
- **Đối chiếu:** E007+E015 cho mâu thuẫn vé/lời khai; E011+E018 cho nét chữ sửa và lựa chọn giữ hai lời kể. Cặp sai lưu giả thuyết không khóa; cặp đúng chỉ tăng clarity một lần.
- **Ký ức:** cassette mở M; palette và bảng y tế/nhà kho đổi. Đây là một quan sát được thiết kế, không shuffle map tùy tiện. Chưa triển khai hệ thống điều khiển nhân vật khác.
- **Quan hệ:** sáu trường trust/familiarity/resentment/dependence/knowledge/willingness. Lắng nghe và truyền lời có hậu quả khác; mỗi cuộc hội thoại nhận hiệu ứng một lần. UI không hiện mọi số. Dependence có lưu trữ, chưa có tuyến thay đổi trong slice.
- **Lịch NPC:** chiều/tối/đêm/rạng sáng tiến theo P004/P008/P022; cảnh mới dùng `requires` và `after_dialogues`. Mio chỉ xuất hiện sau P020. Không phải hệ mô phỏng 24 giờ; NPC theo cảnh có thể được trò chuyện lại ở địa điểm cũ. Lịch riêng cho các chương tương lai còn phải viết.
- **Rumor:** cờ lan truyền và oán giận có tác dụng trong slice; mạng lan tin qua nhiều NPC chưa triển khai.
- **Fear:** tăng khi sai/xuất hiện, tự dịu theo thời gian; Guilt từ lựa chọn; Clarity từ chứng cứ. Chưa có toàn bộ phản ứng âm/hình theo ba trục.
- **Save:** JSON schema 2, đường dẫn người dùng; ghi tạm/fsync/replace; danh sách ID, dữ liệu số và quan hệ được kiểm tra. Không sửa save hỏng âm thầm. Autosave chuyển phòng, xem ghi chép, giải đố, hết thoại, thoát khi đã có tiến trình. Schema 1 được kiểm tra trước khi chuyển, lưu backup .v1.bak và đặt nhân vật tại lối vào an toàn. Không dùng việc đặt lại vị trí để che dữ liệu số bị hỏng.
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

H không hạn chế thời gian, phụ đề nhịp gõ tương đương âm thanh. Không đánh lừa người chơi bằng gợi ý vô căn cứ. Chớp/rung mặc định giảm, scare có thể tắt, âm lượng đỉnh WAV giới hạn. Trong bản 0.2 không có gore; không cộng tùy chọn dự phòng vào số cảnh đã làm.

Để chấp nhận bản thương mại cần: playtest đủ tuyến và ending không dùng cheat; timing logging cả thoại/cutscene (bộ đếm hiện tại chỉ thời gian tự do); review văn hóa/logic; art nhiều dáng và biểu cảm riêng; kiểm tra iGPU, controller, resize/fullscreen trên máy thật; localization; Windows package sạch và antivirus false-positive review nếu có bằng chứng phát sinh.
