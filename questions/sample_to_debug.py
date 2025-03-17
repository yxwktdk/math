import json  
import random  
from collections import defaultdict  

def load_data(file_path):  
    """从 JSONL 文件中加载数据"""  
    data = []  
    with open(file_path, 'r', encoding='utf-8') as file:  
        for line in file:  
            data.append(json.loads(line))  
    return data  

def select_entries(data, num_entries=200):  
    """从数据中选择指定数量的条目，确保每个 ID 至少有一个问题"""  
    # 将数据按 ID 分组  
    grouped_data = defaultdict(list)  
    for entry in data:  
        grouped_data[entry["ID"]].append(entry)  

    selected_entries = []  
    for id_, entries in grouped_data.items():  
        # 筛选出答案不是 "wrong prerequisite" 的条目  
        valid_entries = [entry for entry in entries if entry["Answer"] != "wrong prerequisite."]  
        
        if valid_entries:   
            # 如果有有效条目，随机选择一个  
            selected_entries.append(random.choice(valid_entries))  
        else:  
            # 如果没有有效条目，随机选择一个条目  
            selected_entries.append(random.choice(entries))  

    # 如果需要更多条目，随机选择其他条目  
    while len(selected_entries) < num_entries:  
        id_ = random.choice(list(grouped_data.keys()))  
        entry = random.choice(grouped_data[id_])  
        if entry not in selected_entries:  
            selected_entries.append(entry)  

    # 按 pid 排序  
    selected_entries.sort(key=lambda x: x["pid"])  

    return selected_entries  

if __name__ == "__main__":  
    file_path = '/home/yangxw/math/questions/test.jsonl'  # 输入文件路径  
    data = load_data(file_path)  # 加载数据  
    selected_entries = select_entries(data)  # 选择条目  

    # 保存  
    output_file = '/home/yangxw/math/questions/test-debug.jsonl'  # 输出文件路径  
    with open(output_file, 'w', encoding='utf-8') as file:  
        for entry in selected_entries:  
            file.write(json.dumps(entry, ensure_ascii=False) + '\n')