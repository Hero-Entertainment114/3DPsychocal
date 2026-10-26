# Art & audio bible

Pixel gốc, không ảnh thu nhỏ. Tile 16×16, sprite 32×48, 6 frames × 4 hướng. Portrait 96×96 từ nét gốc 48×48 bằng nearest-neighbor, ba trạng thái. Canvas 480×270. GUI Noto raster không antialias; Japanese logo raster 1-bit. Không dùng smoothing khi scale.

| Vai trò | Màu |
|---|---|
| Mực / outline | #111b24 |
| Bóng sâu | #182733 |
| Xanh bóng | #293f4b |
| Sương | #4b6970 |
| Xanh bạc | #728777 |
| Giấy cũ | #d1c5a5 |
| Đèn / focus | #d6ad68 |
| Đỏ ký ức | #8d4447 |

Nét outline một pixel ở môi trường. Nhân vật có bóng chân, tóc chia khối, mắt nhỏ, đường áo, chân bước khác pha. Ren có túi chéo; áo mỗi người khác palette. **Giới hạn:** hiện cùng một bộ hình thể/tóc cơ bản, chưa đủ đặc trưng của 25 người theo brief. Art sản xuất phải thay bằng bộ tạo hình riêng, không đánh dấu số PNG là số nhân vật đã được hoàn thiện mỹ thuật.

Menu hành lang phối cảnh, cửa cuối, bảng thông báo, cửa sổ mưa, clock 4:44 và vệt phản sáng. Tờ giấy là inset menu để chữ luôn đọc được. Sau tiến trình có bóng nhỏ và tông rạng sáng. Các thay đổi sau chương III–V chỉ có kế hoạch.

WAV đều là tổng hợp có seed, không sample bên ngoài. Rain/hum nền, step/knock/chime, bảy motif (sáu chương thiếu nốt cuối + Sixth Name đủ sáu nốt). Âm lượng nhỏ, đầu/cuối fade. Cần nghe kiểm trên loa/tai nghe trước production; headless test chỉ xác nhận tệp phát được, không xác nhận chất lượng nghe.

Tái tạo: `python tools/generate_assets.py`. Cần Pillow, font Latin đã đóng gói. Muốn tái tạo Japanese logo trên Linux cần NotoSerifCJK-Regular.ttc hệ thống và giấy phép tương ứng; logo có sẵn nên máy chơi không cần CJK font. Trình sinh ghi atlas và manifest SHA-256. Không tải asset khi chạy game.

## Bản đồ 0.2

16 ảnh gốc tương ứng 16 collision maps, vẽ bằng `tools/build_world_art.py`. Hai ga/phòng vé có đường ray, ghế, cửa soát và điện thoại; phố có mái hiên, tiệm có kệ và mèo; bệnh viện có hàng chờ, giường, bình truyền; nhà có kệ giày, CRT, bát và bếp. Trường chia sân, tủ giày, bàn học/bảng, giấy giáo viên, máy phát/reel, đồng hồ 4:44, kệ thuốc và ba buồng vệ sinh. Vật chứng hiện theo trạng thái runtime; không vẽ toàn bộ manh mối tương lai lên ảnh nền.

Tất cả 16 ảnh có hash khác nhau. Điều này xác nhận tệp riêng, không thay đánh giá thẩm mỹ. Các hình screenshot trong reports là ảnh game thật, giữ giới hạn bộ sprite phát triển hiện tại.
