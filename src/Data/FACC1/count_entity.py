from collections import Counter
import re

def extract_entity(line):
    """Hàm trích xuất mã thực thể từ dòng dữ liệu NT"""
    match = re.match(r'<http://www.wikidata.org/entity/(Q\d+)>', line)
    return match.group(1) if match else None

def count_entities(file_path):
    entity_counter = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            entity = extract_entity(line)
            if entity:
                entity_counter[entity] += 1

    return entity_counter

# Đường dẫn tới tệp .nt
file_path = "wikidata_dump_label.nt"
output_file = "all_mention"

# Đếm số lần xuất hiện của mỗi thực thể
entity_counts = count_entities(file_path)

# Ghi kết quả vào file all_mention (chỉ mã thực thể và số lần xuất hiện)
with open(output_file, "w", encoding="utf-8") as f:
    for entity, count in entity_counts.items():
        f.write(f"{entity}\t{count}\n")

print(f"Đã ghi {len(entity_counts)} thực thể vào {output_file}.")
