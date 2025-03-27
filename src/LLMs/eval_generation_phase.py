import json
import torch
import re
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

# Đọc dữ liệu từ file JSON
with open("beam_prediction/generated_predictions_beam.json", "r", encoding="utf-8") as f:
    sampled_data = json.load(f)

model = SentenceTransformer("intfloat/multilingual-e5-small", trust_remote_code=True)

# Ngưỡng tương đồng để coi là khớp
similarity_threshold = 0.9

# Biến đếm
total_samples = len(sampled_data)
exact_match_count = 0
first_exact_match_count = 0
structure_match_count = 0
similarity_match_count = 0

def remove_bracket_content(text):
    return re.sub(r"\[.*?\]", "", text).strip()

with tqdm(total=total_samples, desc="Đang xử lý", unit=" mẫu") as pbar:
    for sample in sampled_data:
        predicted_query = sample["predicted_query"]
        gen_label = sample["gen_label"]

        if not predicted_query:
            pbar.update(1)
            continue

        # Kiểm tra khớp hoàn toàn
        if gen_label in predicted_query:
            exact_match_count += 1

        # Kiểm tra câu đầu tiên có khớp hoàn toàn không
        if predicted_query[0] == gen_label:
            first_exact_match_count += 1

        gen_label_clean = remove_bracket_content(gen_label)
        predicted_clean = [remove_bracket_content(q) for q in predicted_query]

        gen_brackets = re.findall(r"\[(.*?)\]", gen_label)
        
        structure_matched = False
        similarity_matched = False
        
        for q in predicted_query:
            if remove_bracket_content(q) == gen_label_clean:
                structure_matched = True  # Đếm số lần khớp bộ khung
                pred_brackets = re.findall(r"\[(.*?)\]", q)
                
                if len(gen_brackets) == len(pred_brackets):
                    similarities = []
                    for gb, pb in zip(gen_brackets, pred_brackets):
                        queries = [gb, pb]
                        embeddings = model.encode(queries, convert_to_tensor=True)
                        similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
                        similarities.append(similarity)
                    
                    if all(sim >= similarity_threshold for sim in similarities):
                        similarity_matched = True
        
        if structure_matched:
            structure_match_count += 1
        
        if similarity_matched:
            similarity_match_count += 1
        
        pbar.update(1)

# Tính tỷ lệ
exact_match_ratio = exact_match_count / total_samples
first_exact_match_ratio = first_exact_match_count / total_samples
structure_match_ratio = structure_match_count / total_samples
similarity_match_ratio = similarity_match_count / total_samples

# In kết quả
print(f"Tỷ lệ câu đầu tiên khớp hoàn toàn (EM): {first_exact_match_ratio:.2%}")
print(f"Tỷ lệ khớp hoàn toàn với beam search (BM): {exact_match_ratio:.2%}")
print(f"Tỷ lệ khớp bộ khung (SM): {structure_match_ratio:.2%}")
print(f"Tỷ lệ khớp độ tương đồng (CSM): {similarity_match_ratio:.2%}")
