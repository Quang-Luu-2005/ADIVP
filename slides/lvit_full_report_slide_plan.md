# Kế hoạch làm slide từ report `manuscript`

## Nguyên tắc chung

- Bám trực tiếp nội dung trong `manuscript/main.pdf` và `manuscript/sections/content_main.tex`.
- Giữ đúng style template hiện có trong `slides/qatalvit_report_summary_slides.tex`:
  - `beamer`
  - theme `Madrid`
  - bảng màu `accentblue`, `accentteal`, `accentorange`
  - slide cover và slide figure theo phong cách hiện có
- Mỗi chương là một cụm task riêng.
- Chương dài sẽ tách tiếp theo section/subsection để không sót ý.
- Ưu tiên đưa tất cả hình quan trọng trong report vào deck; các hình cùng chủ đề có thể ghép chung một slide nếu vẫn đọc rõ.

## Task breakdown

### Chương 1. Giới thiệu

1. Slide mở đầu và agenda.
2. `1.1 Bối cảnh chung`
   - Khác biệt phân loại, phát hiện, phân đoạn.
   - Bối cảnh dữ liệu ảnh + văn bản + mask.
3. `1.2 Động lực nghiên cứu`
   - Ba động lực chính của LViT.
   - Ý nghĩa khoa học.
   - Ý nghĩa thực tiễn và quy trình lâm sàng.
4. `1.3 Phát biểu bài toán`
   - Input, output, ground truth.
   - Bộ dữ liệu QaTa-COV19.
   - Bộ dữ liệu MosMedData+.
   - Khung hệ thống tổng quan.
   - Phần pretrained và phần học từ đầu.
5. `1.4 Đóng góp`
   - Đóng góp khảo sát.
   - Đóng góp thực nghiệm và cải tiến.

### Chương 2. Các công trình nghiên cứu liên quan

1. `2.1 Các phương thức tiếp cận`
   - Taxonomy tổng quan.
   - Benchmark, độ đo, dữ liệu và challenges.
2. `2.2 State-of-the-Art Methods`
   - CNN/U-Net.
   - Transformer và hybrid CNN--Transformer.
   - Thị giác--ngôn ngữ và phân đoạn có văn bản.
   - Học bán giám sát và pseudo-label.
3. `2.3 Tổng kết và khoảng trống nghiên cứu`
   - Gap 1 đến Gap 4.
   - Dẫn dắt sang LViT.

### Chương 3. Phương pháp

1. `3.1 Tổng quan LViT`
   - Kiến trúc tổng thể.
2. `3.2 Luồng xử lý học và suy luận`
   - Dice/IoU.
   - Luồng huấn luyện.
   - Luồng suy luận.
3. `3.3 Double-U và Vision Transformer đa mức`
4. `3.4 Biểu diễn văn bản và LV Fusion`
5. `3.5 PLAM`
6. `3.6 EPI và LV loss`
7. `3.7 Hàm mất mát và độ đo`

### Chương 4. Cài đặt và thử nghiệm

1. `4.1 Mục đích thử nghiệm`
2. `4.2 Môi trường cài đặt`
   - Phần cứng.
   - Phần mềm.
   - Nguyên tắc kiểm soát thực nghiệm.
3. `4.3 EDA dữ liệu`
   - QaTa-COV19: ví dụ ảnh, mask geometry, text EDA, text-mask alignment.
   - MosMedData+: nguồn dữ liệu, ví dụ ảnh, mask geometry, text EDA, text-mask alignment.
4. `4.4 Quy trình thử nghiệm`
   - Thiết kế thực nghiệm.
   - Cấu hình LViT.
   - Thiết lập riêng cho QaTa-COV19 và MosMedData+.
   - Tiêu chí Dice/IoU.
5. `4.5 Kết quả thực nghiệm`
   - QaTa-COV19 baseline.
   - QaTaLViT cải tiến.
   - MosMedData+ baseline.
   - MosMedData+ cải tiến.
   - So sánh artifact và insight.
6. `4.6 Kết luận chương`

### Chương 5. Kết luận và hướng phát triển

1. `5.1-5.5`
   - Kết luận.
   - Kết quả đạt được.
   - Đóng góp của báo cáo.
   - Hạn chế.
   - Hướng phát triển.
2. `5.6-5.9`
   - Động lực của hướng mở rộng tự giám sát.
   - Khái niệm cơ bản.
   - Các nhóm phương pháp phù hợp với LViT.
   - Liên hệ với bài toán hiện tại.
   - Rủi ro và hạn chế.
   - Đề xuất thực nghiệm mở rộng.
3. `5.10`
   - Kết luận cuối.

## Deliverable

- `slides/lvit_full_report_slides.tex`
- `slides/lvit_full_report_slides.pdf`

