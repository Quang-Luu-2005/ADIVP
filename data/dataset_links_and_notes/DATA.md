# Bộ dữ liệu

Kho lưu trữ này không theo dõi các bộ dữ liệu ảnh y tế hoặc các checkpoint đã huấn luyện. Hãy để dữ liệu cục bộ trong `data/`, `datasets/`, hoặc một thư mục khác đã được bỏ qua.

## QaTa-COV19

Bộ dữ liệu công khai:

- Kaggle: https://www.kaggle.com/datasets/aysendegerli/qatacov19-dataset

Cấu trúc thư mục dự kiến:

```text
QaTa-Covid19/
|-- Train_Folder/
|   |-- Train_text.xlsx
|   |-- img/
|   `-- labelcol/
|-- Val_Folder/
|   |-- Val_text.xlsx
|   |-- img/
|   `-- labelcol/
`-- Test_Folder/
    |-- Test_text.xlsx
    |-- img/
    `-- labelcol/
```

## MosMedData+

Các nguồn công khai:

- Medical Segmentation: http://medicalsegmentation.com/covid19/
- Bản sao trên Kaggle: https://www.kaggle.com/datasets/maedemaftouni/covid19-ct-scan-lesion-segmentation-dataset

Sau khi tiền xử lý, dùng cùng cấu trúc thư mục chia tách theo kiểu LViT như trên.

## Checkpoint

Các checkpoint mô hình được Git bỏ qua. Với bản phát hành công khai, hãy tải checkpoint lên tài nguyên phát hành, model Kaggle, kho Hugging Face, hoặc một điểm lưu trữ ngoài khác, rồi ghi lại đường dẫn tải xuống ở đây.
