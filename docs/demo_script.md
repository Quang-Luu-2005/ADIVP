# Kịch Bản Demo Phần 1.6 - Source Code

## Mở đầu

"Ở phần 1.6, nhóm em xin giới thiệu cách tổ chức source code của đồ án QaTaLViT. Mục tiêu của phần này là cho thấy repo được chia tách rõ ràng giữa mã nguồn, thực nghiệm, tài liệu và phần trình bày, để việc chạy lại thí nghiệm và bảo trì về sau được thuận tiện hơn."

## Giới thiệu cấu trúc

"Kho mã được tổ chức theo các nhóm rõ ràng. Phần triển khai chính nằm trong `src`, các runner và công cụ phân tích nằm trong `scripts`, còn notebook, thí nghiệm và kiểm thử lần lượt nằm trong `notebooks`, `experiments` và `tests`. Phần source đã tuyển chọn để phục vụ bản nộp nằm trong `submission`, được chia theo baseline LViT, bản cải tiến QaTaLViT, runner theo dataset, EDA và output mẫu."

"Cách chia này giúp người xem phân biệt rõ đâu là mã lõi, đâu là mã hỗ trợ thí nghiệm, và đâu là phần đã được tuyển chọn để đưa vào báo cáo hoặc bản nộp chính thức."

## Các phần chính cần nhấn mạnh

"Trong `src/` là toàn bộ mã PyTorch cho huấn luyện, đánh giá, mô hình và dataset. Đây là phần quan trọng nhất nếu muốn hiểu luồng xử lý chính của hệ thống."

"Trong `scripts/` có các script khởi chạy thí nghiệm, tạo gói Kaggle và các công cụ hỗ trợ phân tích. Đây là nơi nhóm em gom những lệnh chạy lại thí nghiệm một cách nhất quán."

"Trong `notebooks/` và `experiments/` là các notebook phục vụ chạy trên Kaggle hoặc Colab, cùng với những snapshot đã được chọn để minh họa các ablation và kết quả thực nghiệm trong báo cáo."

"Các phần `manuscript/` và `slides/` chứa lần lượt bản thảo LaTeX và slide thuyết trình, nên người xem có thể thấy ngay mối liên kết giữa source code, kết quả và tài liệu báo cáo."

"Ngoài ra, `docs/` chứa ghi chú về dataset và cách dùng Kaggle, còn `tests/` chứa các kiểm thử đơn vị nhẹ để kiểm tra những tiện ích quan trọng của dataset, mô hình và huấn luyện."

## Cách chạy nhanh

"Nếu cần chạy thử nhanh, nhóm em tạo môi trường ảo bằng `python -m venv .venv`, kích hoạt bằng `.venv\Scripts\Activate.ps1`, rồi cài dependencies bằng `pip install -r requirements.txt`."

"Với Kaggle notebook, nhóm em dùng `requirements-kaggle.txt` và các cell thiết lập riêng trong notebook để đảm bảo môi trường chạy đồng nhất."

"Ví dụ khi huấn luyện trên QaTa-COV19 với 50% nhãn, có thể chạy script `python scripts/run_qatacov19_050pct.py --dataset-root C:\path\to\QaTa-Covid19 --epochs 120`. Kết quả sẽ được ghi vào thư mục `runs/`, và có thể dùng `--resume` để tiếp tục từ checkpoint tương ứng."

## Kết thúc

"Tóm lại, phần 1.6 cho thấy source code của đồ án được tổ chức theo hướng tách biệt rõ giữa mã nguồn, thực nghiệm, tài liệu và phần trình bày. Nhờ đó, quá trình tái lập kết quả, mở rộng thí nghiệm và bảo trì về sau đều dễ theo dõi hơn."

"Nếu cần, nhóm em có thể mở tiếp từng thư mục con để xem chi tiết mã nguồn, notebook hoặc các script huấn luyện cụ thể."
