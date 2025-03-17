from collections import defaultdict  
import os  
import json  
from tabulate import tabulate  # 用于表格输出  
from colorama import Fore, Style  

eval_category_dict = {  
    "unary": {  
        "Points-unary": ["Existence", "Quantity", "Size Property"],  
        "Line Segment-unary": ["Existence", "Quantity", "Size Property"],  
        "Angle-unary": ["Existence", "Quantity", "Size Property"],  
        "Triangle-unary": ["Existence", "Quantity", "Size Property"],  
        "Circle-unary": ["Existence", "Quantity", "Size Property"],  
        "Polygon-unary": ["Existence", "Quantity", "Size Property"],  
        "Arc-unary": ["Existence", "Quantity", "Size Property"],  
        "Sector-unary": ["Existence", "Quantity", "Size Property"],  
    },  
    "binary": {  
        "Points": ["Points", "LineSegment", "Angle", "Triangle", "Circle", "Polygon"],  
        "LineSegment": ["LineSegment", "Angle", "Triangle", "Circle", "Polygon"],  
        "Angle": ["Angle", "Triangle", "Circle", "Polygon"],  
        "Triangle": ["Triangle", "Circle", "Polygon"],  
        "Circle": ["Circle", "Polygon"],  
        "Polygon": ["Polygon"],  
    }  
}  

# 全局索引字典  
index_to_category = {}  

def fullfill_metrics(count_flag=True):  
    metrics = defaultdict(dict)  

    for key in eval_category_dict.keys():  
        metrics[key] = {}  

        for category, subcategories in eval_category_dict[key].items():  
            metrics[key][category] = {}  
            for subcategory in subcategories:  
                metrics[key][category][subcategory] = 0  
    
    return metrics  

def collectq_ctgrs(folder):  
    """  
    Collect the category of questions in a directory and its subdirectories.  
    """  
    counts = fullfill_metrics()  # 初始化计数器  
    for root, _, files in os.walk(folder):  # 使用 os.walk 遍历文件夹及其子文件夹  
        for file in files:  
            if file.endswith(".json"):  # 只处理 JSON 文件  
                file_path = os.path.join(root, file)  # 获取文件的完整路径  
                with open(file_path, "r") as f:  
                    data = json.load(f)  
                    problems = data['problems']  
                    for item in problems:  
                        problem = item['problem']  
                        if problem['Answer'] == "wrong prerequisite.":  
                            continue  
                        if len(problem['Category']) == 1:  
                            # 说明是 unary  
                            counts['unary'][problem['Category'][0]][problem['SubCategory']] += 1  
                        else:  
                            # 说明是 binary  
                            counts['binary'][problem['Category'][0]][problem['Category'][1]] += 1  
    return counts  

def print_unary_table(counts):  
    """  
    Print the unary counts in a tabular format  
    """  
    global index_to_category  
    current_index = 1  # 每次调用时重置索引  
    print(Fore.RED + "Unary Categories:" + Style.RESET_ALL)  
    table = []  
    headers = ["Category"] + eval_category_dict["unary"]["Points-unary"]  # 属性列标题  
    for category, subcategories in counts['unary'].items():  
        row = [category]  # 当前行的第一个元素是类别  
        for subcategory in eval_category_dict["unary"]["Points-unary"]:  
            if subcategory == "Size Property" and (category == "Points-unary" or category == "Polygon-unary"):  
                row.append(" / ")  
            else:  
                count = subcategories[subcategory]  
                index = f"U{current_index}"  # 添加 U 前缀表示 unary  
                index_to_category[index] = (category, subcategory)
                index = ''  
                row.append(f"{count} {index}")  # 添加数目和索引  
                current_index += 1  
        table.append(row)  
    print(tabulate(table, headers=headers, tablefmt="grid"))  
    

def print_binary_table(counts):  
    """  
    Print the binary counts in an upper triangular tabular format  
    """  
    global index_to_category  
    current_index = 1  # 每次调用时重置索引  
    print(Fore.RED + "Binary Categories:" + Style.RESET_ALL)  
    categories = list(eval_category_dict["binary"].keys())  # 获取所有类别  
    table = []  
    headers = [""] + categories  # 第一列为空，用于行标题  
    for i, row_category in enumerate(categories):  
        row = [row_category]  # 当前行的第一个元素是行类别  
        for j, col_category in enumerate(categories):  
            if j >= i:  # 只填充上三角部分  
                count = counts['binary'][row_category].get(col_category, 0)  
                index = f"B{current_index}"  # 添加 B 前缀表示 binary  
                index_to_category[index] = (row_category, col_category)  
                index = ''
                row.append(f"{count} {index}")  # 添加数目和索引  
                current_index += 1  
            else:  
                row.append("")  # 下三角部分为空  
        table.append(row)  
    print(tabulate(table, headers=headers, tablefmt="grid"))  
    

def find_category_by_index(index):  
    """  
    根据索引找到对应的 category  
    """  
    return index_to_category.get(index, "Index not found")  

def find_problems_by_category(category, file):  
    """  
    根据 category 找到 template 中对应的问题并输出  
    """  
    with open(file, "r") as f:  
        problems = json.load(f)  
        matching_problems = []  
        for problem in problems:  
            if len(problem['Category']) == 1:  
                # Unary category  
                if problem['Category'][0] == category[0] and problem['SubCategory'] == category[1]:  
                    matching_problems.append(problem)  
            else:  
                # Binary category  
                if problem['Category'][0] == category[0] and problem['Category'][1] == category[1]:  
                    matching_problems.append(problem)  
        return matching_problems  

def collect_template_ctgrs(file):  
    # read template  
    with open(file, "r") as f:  
        problems = json.load(f)  
        counts = fullfill_metrics()  
        for problem in problems:  
            if len(problem['Category']) == 1:  
                # 说明是 unary  
                counts['unary'][problem['Category'][0]][problem['SubCategory']] += 1  
            else:  
                # 说明是 binary  
                counts['binary'][problem['Category'][0]][problem['Category'][1]] += 1  

    return counts  

def index_to_template(index, file):  
    index = str(index).upper() 
    category = find_category_by_index(index)  
    if category != "Index not found":  
        problems = find_problems_by_category(category, file)  
        return problems  
    else:  
        return "Index not found"  

# 示例调用  
if __name__ == "__main__":  
    folder = "new"  # 替换为您的 JSON 文件夹路径  
    counts_q = collectq_ctgrs(folder)  
    print_unary_table(counts_q)  
    print_binary_table(counts_q)  

    file = "template_questions_list.json"  
    counts_t = collect_template_ctgrs(file)  
    print_unary_table(counts_t)  
    print_binary_table(counts_t)  

    # 示例：根据索引找到对应的 category  
    while True:  
        index = input("Enter an index: ")  

        problems = index_to_template(index, file)  
        if problems != "Index not found":  
            print("Problems:")  
            for problem in problems:  
                print(problem)  
        else:  
            print("Index not found")  
            break  