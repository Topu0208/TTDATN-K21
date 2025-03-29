# XÂY DỰNG ỨNG DỤNG TRẢ LỜI CÂU HỎI TRÊN DỮ LIỆU WIKIMEDIA SỬ DỤNG MÔ HÌNH LLaMA

## 1. Giới thiệu

**Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM - Khoa Công nghệ Thông tin**  
**Hội đồng Công nghệ Tri thức**  

**Tên đề tài:** Xây dựng ứng dụng trả lời câu hỏi trên đồ thị tri thức sử dụng mô hình ngôn ngữ lớn  
**Mã đề tài:** *DA_2025_CNTT002*  

**Danh sách thành viên:**  

- 21120110 Nguyễn Tấn Phát  
- 21120114 Nguyễn Trần Thiên Phúc  
- 21120115 Nguyễn Trọng Phúc  
- 21120140 Trần Gia Thịnh  
- 21120405 Trần Minh Triết  
- 21120417 Nguyễn Thị Ngọc Châm  

## 2. Mô tả đề tài

Đồ án tập trung vào việc xây dựng một hệ thống trả lời câu hỏi dựa trên đồ thị tri thức Wikidata, kết hợp với mô hình ngôn ngữ lớn (LLM). Hệ thống sẽ tiếp nhận câu hỏi từ người dùng, chuyển đổi thành biểu mẫu logic tương ứng, sau đó thực hiện quá trình truy vấn để tìm thực thể và quan hệ phù hợp tìm ra câu truy vấn SPARQL cuối cùng để truy vấn dữ liệu từ Wikidata và trả về câu trả lời phù hợp.

## 3. Hướng dẫn cài đặt

### 3.1 Tạo dữ liệu FACC1

#### Đối với thực thể:
1. Cài đặt các thư viện cần thiết.
2. Chạy tệp `count_entity.py` để lấy danh sách thực thể và tần suất xuất hiện từ cơ sở tri thức.
3. Đối với dữ liệu tiếng Anh, chạy tệp `map_wiki_entity.py` để lấy nhãn thực thể.
4. Đối với dữ liệu tiếng Việt, chạy tệp `map_wiki_entity_vi.py` để lấy nhãn thực thể.
5. Chạy tệp `process.py` để tính toán tỷ lệ phần trăm xuất hiện của thực thể.

#### Đối với quan hệ:
Thực hiện các bước tương tự như trên nhưng với các tệp `count_property.py`, `map_wiki_property.py`, `map_wiki_property_vi.py`, `process.py`.

**Lưu ý:**
- Kiểm tra tên tệp đầu vào và đầu ra.
- Theo dõi tiến trình thông qua tệp `processing_state.txt`.

### 3.2 Cài đặt môi trường

Chạy các lệnh sau để thiết lập môi trường:

```sh
conda create -n chatkbqa python=3.8
conda activate chatkbqa
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install -r requirement.txt
```

## 4. Hướng dẫn sử dụng

### 4.1 Tiền xử lý dữ liệu

Thực hiện trong thư mục `Data`:

1. **Tạo thuộc tính "s_expr" từ "sparql"**:
   - Chạy `sparql_to_sexpression.ipynb`, dữ liệu sẽ được lưu tại `LC-QuAD2.0/s_expression/`.
2. **Truy vấn Wikidata, lọc câu không có kết quả, tạo các thuộc tính bổ sung**:
   - Chạy `filter.ipynb`, dữ liệu sẽ lưu tại `LC-QuAD2.0/filter/`.
3. **Dịch câu hỏi sang tiếng Việt**:
   - Chạy `translate.ipynb`, dữ liệu sẽ lưu tại `LC-QuAD2.0/translate/`.
4. **Cập nhật thuộc tính "template"**:
   - Chạy `template_update.ipynb`, dữ liệu sẽ lưu tại `LC-QuAD2.0/template/`. Riêng tập test sẽ nằm trong `LC-QuAD2.0/final_process/`.
5. **Chia tập train và validation**:
   - Chạy `split_validation_data.ipynb`, dữ liệu sẽ lưu tại `LC-QuAD2.0/final_process/`.

### 4.2 Chuẩn bị dữ liệu huấn luyện LLM

Chạy lệnh sau để xử lý dữ liệu huấn luyện:

```sh
python process_NQ.py --dataset_type LC-QUAD2.0
```

Dữ liệu sẽ được lưu tại `LLMs/Data/LC-QuAD2.0_Wikidata_NQ_test[train][dev]/examples.json`.

### 4.3 Huấn luyện mô hình

- Mô hình sẽ được huấn luyện trên Kaggle.
- File notebook dùng để huấn luyện và mô hình đã huấn luyện sẽ lưu tại `LLMs/model`.
- Dự đoán LOGICAL FORM với LLM:
  - Sử dụng `generate_prediction.ipynb`, đầu ra lưu tại `LLMs/beam_prediction/`.
  - Mô hình sẽ tạo 5 dự đoán (`num_beam = 5`).
- Đánh giá giai đoạn tạo biểu diễn logic:
  - Chạy `eval_generation_phase.py`, sử dụng dữ liệu từ `LLMs/beam_prediction/`.

### 4.4 Truy xuất và đánh giá mô hình

- Chạy `eval_final_FACC1[SIMCSE][WIKI].ipynb` để đánh giá mô hình.
- Kết quả được lưu tại `LLMs/eval_result/` trong ba thư mục tương ứng với ba phương pháp: `SIMCSE`, `FACC1`, `WIKI`.


