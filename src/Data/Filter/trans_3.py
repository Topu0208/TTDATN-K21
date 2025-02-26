from google.cloud import translate_v2 as translate
import json
from collections import OrderedDict
import os

# Thiết lập Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"googleKey.json"

# Khởi tạo Google Translate API client
translate_client = translate.Client()

def translate_to_vietnamese(input_text):
    """
    Dịch văn bản sang tiếng Việt.
    """
    if not input_text:
        return None
    
    try:
        result = translate_client.translate(
            input_text, 
            target_language="vi",
            format_="text"
        )
        return result["translatedText"]
    
    except Exception as e:
        print(f"Lỗi dịch: {str(e)}")
        return input_text  # Trả lại bản gốc nếu có lỗi

def process_data(data, output_file):
    """
    Xử lý dữ liệu và lưu file sau mỗi 10 bản ghi.
    """
    processed_data = []
    count = 0
    
    for idx, item in enumerate(data):
        try:
            # Tạo một OrderedDict mới để sắp xếp các trường
            new_item = OrderedDict()
            
            # Dịch trường question 
            question_vi = translate_to_vietnamese(item.get("question", ""))
            
            # Thêm tất cả các trường với thứ tự cụ thể
            for key in item.keys():
                new_item[key] = item[key]
                # Chèn question_vi ngay sau question
                if key == "question":
                    new_item["question_vi"] = question_vi
            
            processed_data.append(new_item)
            count += 1
            print(f"Đã xử lý: {count} bản ghi")
            
            # Lưu tạm sau mỗi 10 bản ghi
            if count % 10 == 0:
                write_json(output_file, processed_data)
                print(f"🔄 Đã lưu tạm {count} bản ghi")
        
        except Exception as e:
            print(f"❌ Lỗi ở bản ghi {idx}: {str(e)}")
            continue
    
    # Lưu phần còn lại
    write_json(output_file, processed_data)
    print(f"✅ Đã lưu tổng cộng {count} bản ghi")
    return processed_data

def read_json(file_path):
    """Đọc file JSON với encoding UTF-8"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(file_path, data):
    """Ghi file JSON với định dạng đẹp"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ": "))

# Thực thi chương trình
if __name__ == "__main__":
    input_file = "train_filtered.json"
    output_file = "train_filtered_translated.json"
    
    try:
        data = read_json(input_file)
        print(f"📖 Đã đọc {len(data)} bản ghi từ {input_file}")
        
        # Xử lý tiếp nếu file output đã tồn tại
        if os.path.exists(output_file):
            existing_data = read_json(output_file)
            start_idx = len(existing_data)
            print(f"⏩ Tiếp tục xử lý từ bản ghi {start_idx}")
            processed_data = process_data(data[start_idx:], output_file)
        else:
            processed_data = process_data(data, output_file)
            
        print("🎉 Hoàn thành!")

    except Exception as e:
        print(f"🔥 Lỗi nghiêm trọng: {str(e)}")