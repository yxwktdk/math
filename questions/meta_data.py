# 将new中的全部文件放入到test.jsonl中
import json  
import os

def convert_json_to_jsonl(json_files, output_jsonl):  
    """  
    将指定的 JSON 文件列表中的 `problems` 元素提取为独立的 JSON 行，写入 JSONL 文件中，并确保 `pid` 全局递增。  
    同时将 `problem` 中的内容提取到顶层。  

    Args:  
        json_files (list): 包含 JSON 文件路径的列表。  
        output_jsonl (str): 输出 JSONL 文件路径。  
    """  
    global_pid = 1  # 全局递增的 pid  
    with open(output_jsonl, "w", encoding="utf-8") as jsonl_file:  
        for json_file in json_files:  
            # 读取 JSON 文件  
            with open(os.path.join(JSON_PATH, json_file), "r", encoding="utf-8") as f:
                data = json.load(f)  
            # 输出问题数目
            print(f'{json_file}问题数目：', len(data.get("problems", [])))
            # 遍历每个文件中的 `problems` 列表  
            for problem_entry in data.get("problems", []): 
            
                # 更新 pid  
                problem_entry["pid"] = global_pid  
                global_pid += 1  

                if isinstance(problem_entry["problem"]["Category"], str):
                    problem_entry["problem"]["Category"] = [problem_entry["problem"]["Category"]]
                # 如果"Image"中包含"autogeo"将路径中的image_i.png变为i.png
                
                # 提取 `problem` 中的内容到顶层  
                flattened_entry = {"pid": problem_entry["pid"]}  
                flattened_entry.update(problem_entry["problem"])  # 将 problem 的内容提取到顶层  
                
                # 写入 JSONL 文件  
                jsonl_file.write(json.dumps(flattened_entry, ensure_ascii=False) + "\n")  
        print('Done!')

# 示例用法  
json_files = []
JSON_PATH = "D:/senior/毕设/math/questions/new"
# JSON_PATH = "/home/yangxw/math/questions/new"
# 遍历文件夹
# for root, dirs, files in os.walk(JSON_PATH):
#     for file in files:
#         if file.endswith(".json"):
#             json_files.append(file)
# 遍历子文件夹
for root, dirs, files in os.walk(JSON_PATH):
    for dir in dirs:
        for root, dirs, files in os.walk(os.path.join(JSON_PATH, dir)):
            for file in files:
                if file.endswith(".json"):
                    json_files.append(os.path.join(dir, file))
# json_files中的//换成/
json_files = [file.replace('\\', '/') for file in json_files]
# 删除questions_ver0101_0.json文件
json_files.remove('mathverse/questions_ver0101_0.json')
# sort
json_files.sort()

output_jsonl = """test.jsonl"""  # 输出的 JSONL 文件路径  
convert_json_to_jsonl(json_files, output_jsonl)