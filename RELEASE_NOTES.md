# v1.0.0 - Portfolio release cho project Điện tử số

## Nội dung chính

- Đóng gói project điều khiển đèn giao thông vòng xoay 4 hướng bằng mạch số.
- Thêm README tiếng Việt theo cấu trúc reviewer/HR có thể đọc nhanh.
- Thêm banner SVG, GIF motion 12 trạng thái và ảnh preview CircuitJS.
- Giữ SVG ở dạng ASCII-safe để tránh lỗi dấu tiếng Việt khi GitHub render.
- Kèm script kiểm thử logic bằng Node.js cho chu kỳ thường, emergency mode và night mode.

## Artifact release

- Video demo project nộp Moodle.
- Video demo Falstad/CircuitJS bản 1080p.
- Báo cáo Word của project.
- Source snapshot tạo từ commit release.

## Kiểm thử

```powershell
node .\tools\circuitjs-local\verify-roundabout-logic.js
```

Kết quả mong đợi: `OK: normal cycle, emergency mode, and night mode passed.`
