# Xây dựng ứng dụng trả lời câu hỏi trên đồ thị tri thức sử dụng mô hình ngôn ngữ lớn

## 1. Giới thiệu

**Trường Đại học Khoa học Tự nhiên - Khoa Công nghệ Thông tin**\
**Hội đồng Công nghệ Tri thức**

**Tên đề tài:** Xây dựng ứng dụng trả lời câu hỏi trên đồ thị tri thức sử dụng mô hình ngôn ngữ lớn\
**Mã đề tài:** *DA_2025_CNTT002*

**Danh sách thành viên:**

- 21120110 Nguyễn Tấn Phát
- 21120114 Nguyễn Trần Thiên Phúc
- 21120115 Nguyễn Trọng Phúc
- 21120140 Trần Gia Thịnh
- 21120405 Trần Minh Triết
- 21120417 Nguyễn Thị Ngọc Châm

Liên hệ với chúng tôi tại email: `<Student ID>.hcmus.edu.vn`
## 2. Mô tả đề tài

Đồ án tập trung vào việc xây dựng một hệ thống trả lời câu hỏi dựa trên đồ thị tri thức Wikidata, kết hợp với mô hình ngôn ngữ lớn (LLM). Hệ thống sẽ tiếp nhận câu hỏi từ người dùng, chuyển đổi thành truy vấn SPARQL để truy xuất dữ liệu từ Wikidata và trả về câu trả lời phù hợp.

## 3. Hướng dẫn cài đặt

### 3.1 Cài đặt môi trường

Chạy các lệnh sau để thiết lập môi trường làm việc:

```bash
conda create -n chatkbqa python=3.8
conda activate chatkbqa
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install -r requirement.txt
```

### 3.2 Cài đặt Virtuoso Open Source

1. Tạo dữ liệu dump từ Wikidata:
   ```bash
   # Chạy file tạo dump dữ liệu
   python generate_dump.ipynb
   ```
2. Khởi tạo Virtuoso:
   ```bash
   cd Wiki_setup
   python3 virtuoso.py start 8890 -d "virtuoso_db"
   ```
3. Nạp dữ liệu vào Virtuoso:
   ```bash
   Wiki_setup/virtuoso-opensource/bin/isql 18890 dba dba <<EOF
   log_enable(2);
   ld_dir('Wiki_setup/virtuoso_db', 'wikidata_dump.nt', 'http://www.wikidata.org');
   rdf_loader_run();
   checkpoint;
   exit;
   EOF
   ```
4. Dừng Virtuoso khi không sử dụng:
   ```bash
   python3 virtuoso.py stop 8890
   ```

## 4. Hướng dẫn sử dụng

### 4.1 Tiền xử lý dữ liệu

Thực hiện các bước xử lý dữ liệu trong thư mục `Data`:

1. **Dịch câu hỏi sang tiếng Việt:**
   ```bash
   run all "translate.ipynb"
   ```
2. **Lọc dữ liệu:**
   ```bash
   run all "filter.ipynb"
   ```
3. **Tạo các thuộc tính dữ liệu:**
   ```bash
   run all "sparql_to_sexpr.ipynb"
   run all "sexpr_to_nor_sexpr.ipynb"
   run all "nor_sexpr_vi.ipynb"
   ```
4. **Tạo danh sách ánh xạ thực thể và quan hệ:**
   ```bash
   run all "golden_map.ipynb"
   ```

### 4.2 Huấn luyện mô hình LLM

```bash
python process_NQ.py --dataset_type LC-QuAD2.0
```

Dữ liệu sẽ được lưu tại `LLMs/Data/WikiWebQuestions_Wikidata_NQ_test[train]/examples.json`.

Huấn luyện mô hình trên Kaggle với tập dữ liệu đã xử lý:

- Chạy file huấn luyện trong thư mục `LLMs/LoRA`

### 4.3 Dự đoán và đánh giá mô hình

1. **Dự đoán Logical Form với LLM**:
   ```bash
   run all "generate_prediction.ipynb"
   ```
   Kết quả dự đoán lưu tại `LLMs/beam_prediction/generated_predictions_beam.json`.
2. **Đánh giá mô hình:**
   ```bash
   run all "eval_final.ipynb"
   ```
   Kết quả lưu tại `LLMs/eval_result/`.

## 5. Cấu trúc thư mục

```
├── Data
│   ├── LC-QuAD2.0
│   ├── translate/
│   ├── filter/
│   ├── s_expr/
│   ├── nor_sexpr/
│   ├── label_map/
├── LLMs
│   ├── Data/
│   ├── LoRA/
│   ├── beam_prediction/
│   ├── eval_result/
├── Wiki_setup
│   ├── virtuoso_db/
│   ├── generate_dump/
├── scripts
│   ├── process_NQ.py
│   ├── generate_prediction.ipynb
│   ├── eval_final.ipynb
```

## 6. Liên hệ


---

