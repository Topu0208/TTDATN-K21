import requests
import threading
from queue import Queue

# Định nghĩa file
file_path = 'prop_all_mention'
output_file_path = 'property_list_file_wikidata_complete_all_mention'
state_file_path = 'processing_state.txt'  # Lưu trạng thái dòng đã xử lý

# Số lượng ID gửi mỗi lần
BATCH_SIZE = 50 
NUM_THREADS = 12  # Có thể tăng nếu muốn xử lý nhanh hơn

# Đọc trạng thái dòng đã xử lý
try:
    with open(state_file_path, 'r') as state_file:
        processed_lines = int(state_file.read().strip())
except FileNotFoundError:
    processed_lines = 0  # Bắt đầu từ đầu nếu không có trạng thái trước đó

queue = Queue()

# Lấy nhãn từ Wikidata bằng batch request
def get_labels_from_wikidata(property_ids, session):
    ids_string = '|'.join(property_ids)
    url = f'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={ids_string}&props=labels&languages=en&format=json'
    
    try:
        response = session.get(url)
        data = response.json()
        
        labels = {}
        if 'entities' in data:
            for prop_id, entity in data['entities'].items():
                if prop_id.startswith('P'):  # Chỉ lấy property
                    label = entity.get('labels', {}).get('en', {}).get('value')
                    if label:
                        labels[prop_id] = label
        return labels
    except Exception as e:
        print(f"Lỗi khi lấy nhãn: {e}")
        return {}

def process_batch(batch, session, output_file, current_line):
    """Xử lý một batch dữ liệu"""
    property_ids = [line.split('\t')[0] for line in batch if line.startswith('P')]
    labels = get_labels_from_wikidata(property_ids, session)
    
    results = []
    for line in batch:
        prop_id, frequency = line.strip().split('\t')
        if prop_id in labels:
            results.append(f"{prop_id}\t{labels[prop_id]}\t{frequency}\n")

    if results:
        output_file.writelines(results)  # Ghi tất cả cùng lúc để giảm I/O

    # Cập nhật trạng thái dòng cuối cùng đã xử lý
    with open(state_file_path, 'w') as state_file:
        state_file.write(str(current_line))

def worker(session, output_file):
    """Luồng xử lý dữ liệu từ queue"""
    while True:
        item = queue.get()
        if item is None:  # Nhận tín hiệu kết thúc
            queue.task_done()
            break
        current_line, batch = item
        process_batch(batch, session, output_file, current_line)
        queue.task_done()

# Mở file để xử lý và ghi dữ liệu tiếp tục
with open(file_path, 'r', encoding='utf-8') as f, open(output_file_path, 'a', encoding='utf-8') as output_file:
    session = requests.Session()
    threads = [threading.Thread(target=worker, args=(session, output_file)) for _ in range(NUM_THREADS)]
    
    # Khởi động các luồng xử lý
    for thread in threads:
        thread.start()

    batch = []
    current_line = 0  # Đếm số dòng hiện tại

    # Đọc từng dòng trong file đầu vào
    for current_line, line in enumerate(f, start=1):
        if current_line <= processed_lines:
            continue  # Bỏ qua dòng đã xử lý trước đó

        if line.startswith('P'):  # Chỉ xử lý property
            batch.append(line)

        if len(batch) >= BATCH_SIZE:
            queue.put((current_line, batch))
            batch = []  # Xóa batch để tạo batch mới

    # Xử lý batch cuối nếu còn dữ liệu chưa gửi
    if batch:
        queue.put((current_line, batch))

    # Chờ cho tất cả các batch được xử lý
    queue.join()

    # Đẩy tín hiệu kết thúc vào hàng đợi cho mỗi luồng
    for _ in range(NUM_THREADS):
        queue.put(None)

    # Chờ tất cả các luồng kết thúc
    for thread in threads:
        thread.join()

print(f"Đã xử lý {current_line} dòng và lưu vào {output_file_path}")
