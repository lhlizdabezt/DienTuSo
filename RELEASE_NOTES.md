# v1.1.0 - Reviewer-ready polish cho project Điện tử số

## Nội dung chính

- Bổ sung liên kết review nhanh cho repo, release, tags, GitHub portfolio và LinkedIn.
- Làm rõ vai trò của `DienTuSo` trong portfolio kỹ thuật: bằng chứng nền tảng về logic tuần tự, bộ đếm mod-12, JK flip-flop, mô phỏng CircuitJS/Falstad và kiểm thử bằng Node.js.
- Giữ toàn bộ nội dung Markdown/bảng/chú thích bằng tiếng Việt; phần text trong SVG tiếp tục dùng ASCII-safe để tránh lỗi render dấu.
- Giữ nguyên mạch, GIF motion, ảnh preview, video/report release asset và script kiểm thử logic từ bản portfolio release ban đầu.

## Artifact release

- Source snapshot từ commit `v1.1.0`.
- Video demo project nộp Moodle.
- Video demo Falstad/CircuitJS bản 1080p.
- Báo cáo Word của project.
- Banner SVG `assets/digital-logic-hero.svg`.
- GIF motion `assets/roundabout-motion.gif`.
- Ảnh preview CircuitJS `assets/circuitjs-preview.png`.

## Kiểm thử

```powershell
node .\tools\circuitjs-local\verify-roundabout-logic.js
```

Kết quả mong đợi: `OK: normal cycle, emergency mode, and night mode passed.`

---

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
