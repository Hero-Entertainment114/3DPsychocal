from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]/'production/form-review'
records=json.loads((ROOT/'manifest.json').read_text())
parts=['<!doctype html><html lang="vi"><meta charset="utf-8"><title>Bến Không Tên · Cảnh Blender đang hoàn thiện</title><style>body{max-width:1100px;margin:36px auto;background:#16201e;color:#eee2c8;font:17px system-ui}img{width:100%}section{margin:40px 0}.views{display:grid;grid-template-columns:1fr 1fr;gap:16px}a{color:#e4b978}figcaption{padding:8px}</style><h1>Năm cảnh Blender · Bản xem xét hình khối và vật liệu</h1><p>Bố trí đã được bạn duyệt. Đây là bước Form, chưa phải xác nhận chất lượng cuối hoặc cảnh đã xuất sang game. Các mesh, vật liệu và ánh sáng được dựng cục bộ; không dùng API Lux3D/Meshy.</p><p>Ảnh Cycles 16 mẫu có nhiễu vì bản Blender không có bộ khử nhiễu. Báo cáo geometry-audit.json ghi riêng kiểm tra đã chạy và phần còn thiếu. Chưa có đánh giá hiệu năng trong game.</p>']
for r in records:
 rid=r['room'];parts.append(f'<section><h2>{html.escape(rid)}</h2><img src="{rid}/production.png"><p><a href="{r["source"]}">Tệp Blender có thể chỉnh sửa</a></p><div class="views">')
 for view in ['corner-sw','corner-se','corner-nw','corner-ne','center-up','ceiling-a','ceiling-b']:parts.append(f'<figure><img src="{rid}/{view}.png"><figcaption>{view}</figcaption></figure>')
 parts.append('</div></section>')
parts.append('<a href="geometry-audit.json">Kết quả kiểm tra hình học</a></html>')
(ROOT/'review.html').write_text(''.join(parts),encoding='utf8')
