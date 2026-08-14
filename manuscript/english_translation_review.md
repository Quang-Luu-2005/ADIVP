# English Terms Translation Review

File này ghi các cụm tiếng Anh còn xuất hiện nhiều trong báo cáo và hướng dịch đề xuất. Chưa nên thay hàng loạt các tên riêng như LViT, U-Net, Transformer, CNN, BiomedBERT, Dice, IoU, PLAM, EPI vì đó là tên mô hình/độ đo/thuật ngữ chuẩn; nên dịch phần diễn giải xung quanh chúng.

## Nên dịch trong thân bài

| Cụm đang dùng | Hướng dịch đề xuất |
|---|---|
| framework | khung hệ thống / khung bài toán |
| ground truth | nhãn xác thực / mặt nạ xác thực |
| input / output | đầu vào / đầu ra |
| train / validation / test | tập huấn luyện / tập kiểm định / tập kiểm thử |
| baseline | mốc nền / mô hình nền |
| benchmark | mốc đánh giá / bộ chuẩn đánh giá |
| performance | hiệu suất / kết quả đánh giá |
| accuracy | độ chính xác toàn pixel |
| precision | độ chính xác dương |
| recall | độ bao phủ / độ nhạy |
| foreground | vùng tiền cảnh / vùng tổn thương |
| background | vùng nền |
| feature map | bản đồ đặc trưng |
| feature | đặc trưng |
| token | mã thông tin / token |
| embedding | biểu diễn nhúng / vector nhúng |
| encoder | bộ mã hóa |
| decoder | bộ giải mã |
| fusion | hợp nhất |
| attention | cơ chế chú ý |
| self-attention | tự chú ý |
| skip connection | kết nối tắt |
| pseudo-label | nhãn giả |
| loss | hàm mất mát |
| pretrained / pretrain | tiền huấn luyện / đã tiền huấn luyện |
| fine-tune | tinh chỉnh |
| semi-supervised | bán giám sát |
| supervised | có giám sát |
| unsupervised | không giám sát |
| teacher / student | mô hình giáo viên / mô hình học viên |
| batch size | kích thước lô |
| epoch | vòng huấn luyện |
| learning rate | tốc độ học |
| weight decay | suy giảm trọng số |
| scheduler | bộ điều chỉnh tốc độ học |
| seed | hạt giống ngẫu nhiên |
| pipeline | quy trình xử lý |
| artifact | sản phẩm trung gian / hiện vật thực nghiệm |
| ablation | thí nghiệm loại trừ thành phần |
| domain shift | lệch miền dữ liệu |
| calibration | hiệu chuẩn xác suất |
| cross-modal | liên phương thức |
| multimodal | đa phương thức |
| modality | phương thức dữ liệu |
| prompt | câu nhắc / mẫu văn bản chuẩn hóa |
| optimizer | bộ tối ưu |
| augmentation | tăng cường dữ liệu |
| crop | cắt vùng ảnh |
| heatmap | bản đồ nhiệt |
| threshold | ngưỡng |
| thresholding | nhị phân hóa theo ngưỡng |
| boundary-based metric | độ đo dựa trên biên |
| long-range context | ngữ cảnh xa |
| local feature | đặc trưng cục bộ |
| pixel-level | mức điểm ảnh |
| image-text fusion | hợp nhất ảnh--văn bản |
| text annotation | chú thích văn bản |
| text encoder | bộ mã hóa văn bản |

## Nên giữ nguyên hoặc dịch kèm lần đầu

| Cụm | Cách dùng đề xuất |
|---|---|
| CNN | giữ nguyên; lần đầu có thể ghi "mạng tích chập (CNN)" |
| Transformer | giữ nguyên như tên kiến trúc |
| U-Net / nnU-Net / TransUNet / Swin-Unet | giữ nguyên tên mô hình |
| LViT / QaTaLViT | giữ nguyên tên phương pháp |
| BiomedBERT / BERT | giữ nguyên tên mô hình |
| Dice / IoU / mIoU | giữ nguyên tên độ đo; giải thích bằng tiếng Việt |
| BCE / FLOPs | giữ nguyên ký hiệu; giải thích khi xuất hiện lần đầu |
| PLAM / EPI / LV loss | giữ nguyên tên module/loss của LViT; có thể dịch diễn giải phía sau |

## Hình taxonomy liên quan

Hình `related_taxonomy_lvit.png` hiện dùng nhãn tiếng Anh. Nếu thay bằng bản tiếng Việt, nên đổi:

| Nhãn tiếng Anh trong hình | Nhãn tiếng Việt đề xuất |
|---|---|
| Taxonomy of Related Work for LVIT | Bản đồ các công trình liên quan đến LViT |
| From image-only segmentation to language-guided semi-supervised medical segmentation | Từ phân đoạn chỉ dùng ảnh đến phân đoạn y khoa bán giám sát có văn bản dẫn hướng |
| image branch | nhánh ảnh |
| language branch | nhánh văn bản |
| limited-label branch | nhánh ít nhãn |
| Local feature maps, sharp boundaries | Bản đồ đặc trưng cục bộ, biên sắc hơn |
| Patch tokens, long-range context | Token patch, ngữ cảnh xa |
| Hybrid CNN-Transformer | Lai CNN--Transformer |
| Keep local details while modeling global context | Giữ chi tiết cục bộ và học ngữ cảnh toàn cục |
| Vision-Language | Thị giác--ngôn ngữ |
| Text encoder and image-text fusion | Mã hóa văn bản và hợp nhất ảnh--văn bản |
| Semi-supervised | Bán giám sát |
| Pseudo-labels for unlabeled images | Nhãn giả cho ảnh chưa nhãn |
| Double-U + LV Fusion + PLAM | Double-U + LV Fusion + PLAM |
| EPI and LV loss for pseudo-label control | EPI và LV loss để kiểm soát nhãn giả |
| Open Gaps | Khoảng trống còn mở |
| text quality, CT domain shift, small masks, calibration | chất lượng văn bản, lệch miền CT, mặt nạ nhỏ, hiệu chuẩn |

