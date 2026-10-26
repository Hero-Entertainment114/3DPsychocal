# Nâng cấp theo prompt 0.3 và 0.3.1 — phần nền tảng

Ngày 26/10/2026, giờ Việt Nam. Đây chưa phải bản nghiệm thu v0.3.1.

Đã tích hợp trực tiếp vào game: điểm vào đối ứng cho mọi portal, ID exit/entrance và hướng sau khi chuyển phòng; không còn tên phòng ở góc màn hình, nhãn đích nổi hay dấu chấm than puzzle; hội thoại hoàn tất không được khai thác lại, lịch sử vẫn có trong sổ; đèn pin nhặt trên quầy tiệm sau mua đồ, L bật/tắt, lưu trạng thái; chùm sáng giới hạn và suy giảm, tile tường/bàn che sáng, lightmap cache. Đèn hiện đi kèm pin; chưa có hệ ghép vật phẩm. Ánh sáng mới chỉ áp dụng nội thất trường, chưa phải hệ point-light toàn thế giới. Sprite cầm đèn chưa có.

Kiểm tự động: 58 tests; tuyến input vẫn đi qua 16 maps, 22 puzzles, 44 ghi chép và 59 hội thoại. Test riêng cho portal hai chiều, vật cản ánh sáng, nhặt một lần, lưu công tắc và ngăn hỏi lại. Chưa benchmark iGPU hoặc playtest người thật. Script route chứng minh tiến trình, không chứng minh puzzle đã được thiết kế lại.

Còn phải triển khai trước nghiệm thu: thay toàn bộ câu hỏi/nhập đáp án bằng hành động môi trường; item-use/combine/giao nhận/đẩy vật; trường nhiều tầng với cầu thang thật; lịch NPC/A*/hoạt động/đi qua cửa; NPC nền và giao thông; transitions và fog; vẽ lại sprites/portraits/maps ở độ chi tiết mới; render 960×540; biển Nhật/font và bảng thuật ngữ; horror director, Hanako và sự kiện; biên tập thoại/menu. Các prompt gốc nằm tại BRIEF_V03.txt và BRIEF_V031.txt. Không coi portal đối ứng là đã đáp ứng kiến trúc trường liên thông.

Alpix đã mở canvas chung 256×256; không có công cụ xuất PNG/atlas được cung cấp. Không ghi đè canvas chung để giả làm tài nguyên repo. AutoSprite đã kiểm tra lại Ren: characterImage=null, spritesheets=[]; chưa có asset tải được. Không gọi sprite đang dùng là sản phẩm hai dịch vụ này.

Bản Windows liên kết trong README là 0.2 đã kiểm chứng, không phải bản nâng cấp này. Source ZIP của nhánh chứa các sửa đổi mới; CI tiếp theo sẽ kiểm build của commit mới riêng.

## Đợt tiếp tục: cấu trúc trường và khám phá

Đã thêm 8 maps: hành lang tầng một/hai, cầu thang một–hai và hai–ba, thư viện, phòng y tế, phòng trực, nhà vệ sinh tầng hai. Tổng 24 maps (8 mở đầu, 16 Hanako). Cửa lên tầng tiếp theo ở đầu trên của map cầu thang; người chơi đi qua bậc thang để tiếp cận. Graph ở `world_graph.mmd`; từng portal giữ exit/entrance ID, điều kiện, điểm vào, hướng và loại chuyển. Từ sân tới nhà vệ sinh tầng ba phải qua cả hai cầu thang. Các phòng phụ có đồ vật quan sát được và không cộng chúng thành câu đố mới.

16 biển Nhật raster bằng Noto Sans CJK, có bản dịch chủ động bằng E và bảng `data/japanese_glossary.json`. Chữ dùng các tên phòng thông dụng; chưa có người biên tập tiếng Nhật kiểm độc lập. Phông chữ hệ thống chỉ cần khi tái tạo tài nguyên, máy chơi dùng PNG đã đóng gói. Giấy phép Noto CJK đã có trong assets/fonts.

Chuyển cửa/cầu thang dùng fade 0,36 giây, khóa nhập liệu và dừng mô phỏng trong chuyển cảnh. Không có tên địa điểm/loading label. Đây là chuyển gần, chưa có phim lên tàu/xe buýt cho địa điểm xa. Boundary fog chỉ phủ dải mép ngoài trời, giữ vùng tiếp cận cửa rõ; không phủ hành lang. Fog hiện tĩnh theo tọa độ thế giới, chưa có nhiễu chuyển động.

62 tests local qua; route thực qua input đi đủ 24 maps, 22 puzzles, 44 ghi chép, 59 hội thoại; đã nhặt và dùng đèn pin trong tuyến kiểm. Save/load cuối tuyến và cửa hai chiều đều qua. Đã xem screenshot cầu thang/thư viện để kiểm bố cục ánh sáng; chưa có human playtest/benchmark. Asset manifest hiện 96 tệp.

Vẫn còn: NPC Schedule/A*/đi qua cửa, NPC nền, giao thông; đồ họa chi tiết mới và render 960×540; thay câu hỏi bằng tương tác môi trường; item-use/combine; horror director/Hanako; viết lại thoại/menu; fog động và chuyển phương tiện. Không coi đây là bản 0.3.1 hoàn chỉnh.
