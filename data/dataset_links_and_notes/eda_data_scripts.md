# Các script EDA cho QaTa-COV19 và MosMedData+

Ghi chú này mô tả hai script EDA bộ dữ liệu được dùng để mở rộng Chương 4.

Các script này kỳ vọng một thư mục gốc bộ dữ liệu theo kiểu LViT:

```text
DatasetRoot/
  Train_Folder/
    img/
    labelcol/
    Train_text.xlsx
  Val_Folder/
    img/
    labelcol/
    Val_text.xlsx
  Test_Folder/
    img/
    labelcol/
    Test_text.xlsx
```

## 1. EDA hình học mask

Mục đích:

- Định lượng mức mất cân bằng giữa nền và tiền cảnh.
- Hiển thị ảnh trung bình và bản đồ nhiệt mask trung bình.
- Phân tích diện tích mask, phân bố trọng tâm và các thành phần liên thông.
- So sánh diện tích mask theo phía trái/phải được ghi trong văn bản.

QaTa-COV19:

```powershell
python .\scripts\eda_mask_geometry.py `
  --dataset-root "C:\path\to\QaTa-Covid19" `
  --output .\manuscript\figures\qata_mask_geometry_eda.png `
  --summary-json .\manuscript\figures\qata_mask_geometry_eda.summary.json `
  --samples-csv .\manuscript\figures\qata_mask_geometry_eda.samples.csv `
  --title "QaTa-COV19: EDA hình học mask"
```

MosMedData+:

```powershell
python .\scripts\eda_mask_geometry.py `
  --dataset-root "C:\path\to\MosMedDataPlus" `
  --output .\manuscript\figures\mosmed_mask_geometry_eda.png `
  --summary-json .\manuscript\figures\mosmed_mask_geometry_eda.summary.json `
  --samples-csv .\manuscript\figures\mosmed_mask_geometry_eda.samples.csv `
  --title "MosMedData+: EDA hình học mask"
```

Nhận xét rút ra:

- Diện tích mask trung vị nhỏ ủng hộ việc dùng Dice/BCE và giải thích độ nhạy của IoU.
- Bản đồ nhiệt mask trung bình tập trung cho thấy cần lựa chọn crop/resize cẩn thận.
- Nhiều thành phần liên thông ủng hộ phần thảo luận về nhãn giả nhiễu.

## 2. EDA khớp giữa văn bản và mask

Mục đích:

- Kiểm tra xem chú thích văn bản có phản ánh mask ở mức điểm ảnh hay không.
- So sánh phía trái/phải trong văn bản với phía trái/phải của mask.
- So sánh vùng theo trục dọc trong văn bản với vùng theo trục dọc của mask.
- So sánh số vùng nhiễm được nhắc trong văn bản với số thành phần liên thông.

QaTa-COV19:

```powershell
python .\scripts\eda_text_mask_alignment.py `
  --dataset-root "C:\path\to\QaTa-Covid19" `
  --output .\manuscript\figures\qata_text_mask_alignment.png `
  --summary-json .\manuscript\figures\qata_text_mask_alignment.summary.json `
  --samples-csv .\manuscript\figures\qata_text_mask_alignment.samples.csv `
  --title "QaTa-COV19: EDA khớp text annotation và mask"
```

MosMedData+:

```powershell
python .\scripts\eda_text_mask_alignment.py `
  --dataset-root "C:\path\to\MosMedDataPlus" `
  --output .\manuscript\figures\mosmed_text_mask_alignment.png `
  --summary-json .\manuscript\figures\mosmed_text_mask_alignment.summary.json `
  --samples-csv .\manuscript\figures\mosmed_text_mask_alignment.samples.csv `
  --title "MosMedData+: EDA khớp text annotation và mask"
```

Nhận xét rút ra:

- Mức khớp text-mask cao ủng hộ LV Fusion và LV loss.
- Mức khớp trung bình hoặc thấp ủng hộ nhận định rằng văn bản chỉ là phần hỗ trợ ngữ nghĩa, không thể thay thế mask.
- Mức khớp yếu hơn trên MosMedData+ ủng hộ thảo luận rằng lát cắt CT nhạy hơn với crop, ngưỡng tách và chất lượng nhãn giả.
