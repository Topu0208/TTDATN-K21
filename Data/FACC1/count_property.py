from collections import Counter
import re

def extract_property(line):
    """Hàm trích xuất thuộc tính từ dòng dữ liệu NT"""
    property_match = re.search(r'<http://www.wikidata.org/prop/direct/(P\d+)>', line)
    
    return property_match.group(1) if property_match else None

def count_filtered_properties(file_path):
    property_counter = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            prop = extract_property(line)
            if prop:
                property_counter[prop] += 1
    
    return property_counter

# Đường dẫn tới tệp .nt
file_path = "wikidata_dump_label.nt"
output_file = "prop_all_mention"

# Đếm số lần xuất hiện của mỗi thuộc tính
property_counts = count_filtered_properties(file_path)

# Ghi kết quả vào file filtered_properties (chỉ mã thuộc tính và số lần xuất hiện)
with open(output_file, "w", encoding="utf-8") as f:
    for prop, count in property_counts.items():
        f.write(f"{prop}\t{count}\n")

print(f"Đã ghi {len(property_counts)} thuộc tính vào {output_file}.")