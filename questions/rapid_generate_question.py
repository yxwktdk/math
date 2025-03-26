# 快速的为图片产生少量问题
from utils import *
from process_question import *
import os
import json
from colorama import Fore, Style 
import argparse
def rapid_process_question(template_file, question_folder, image_id):
    """
    template_file: 模板文件的路径
    question_folder: 问题文件的路径（全部）
    image_id: autogeo图片的id
    """
    image_path = os.path.join('autogeo', 'images', str(image_id) + '.png')
    output_path = os.path.join(question_folder, 'autogeo', 'questions_ver0226_'+str(image_id) + '.json')
    
    while True:
        mode = input(Fore.GREEN + f"正在处理图片{image_id}，Choose mode(a,auto/c,choose):" + Style.RESET_ALL).strip().lower()
        if mode == 'a':
            mode = 'auto'
            break
        elif mode == 'c':
            mode = 'choose'
            break
        else:
            print(Fore.RED + 'Invalid input' + Style.RESET_ALL)
    results = load_json(output_path, image_id)
    idx = len(results["problems"])
    template_id_lst= ['u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7', 'u8', 'u9', 'u10', 'u11', 'u12', 'u13', 'u14', 'u15', 'u16', 'u17', 'u18', 'u19', 'u20', 'u21', 'u22', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16', 'b17', 'b18', 'b19', 'b20', 'b21']
    
    if mode == 'auto':
        template_id = input(Fore.GREEN + f"正在处理图片{image_id}，输入index：" + Style.RESET_ALL).strip().lower()
        # 查看是第几个
        template_id_count = template_id_lst.index(template_id) if template_id in template_id_lst else 0
    
    while mode == 'choose' or template_id_count != len(template_id_lst):
        
        # 输出已有全部问题的分布
        counts_q = collectq_ctgrs(question_folder)
        print_unary_table(counts_q)
        print_binary_table(counts_q)
        # 可以选择问题
        # 彩色输出：正在处理图片{Image_id}
        print(f'已经为图片{image_id}处理{idx}个问题')
        if mode == 'choose':
            template_id = input(Fore.GREEN + f"正在处理图片{image_id}，输入index：" + Style.RESET_ALL)
        else:
            template_id = template_id_lst[template_id_count]
            template_id_count += 1
            print(Fore.GREEN + f"当前处理模板为：{template_id}" + Style.RESET_ALL)
        if template_id == '':
            break
        templates = index_to_template(template_id, template_file)
        if templates == "Index not found":
            print("Index not found")
            continue
        for item in templates:
            idx_old = idx
            question = item["Question"]
            print(Fore.YELLOW + 'Template: '+question + Style.RESET_ALL)
            while True:
                choice = input(Fore.GREEN + 'Do you want to use this template? (a)'+Style.RESET_ALL).strip().lower()
                if choice == '':
                    break
                elif choice == 'a':
                    question_id = item["ID"]
                
                    question_type = item["Type"]
                    category = item["Category"]
                    subcategory = item["SubCategory"]
                    problem = {
                        "Image": image_path,  # 这里可以替换为实际的图像路径  
                        "Question": modify_question_from_template(question, item["Element_instance"]),
                        "Type": question_type,  
                        "Category": category,  
                        "SubCategory": subcategory,  
                        "ID": question_id,                          "Answer": modify_answer(),  
                    }
                    results["problems"].append(
                        {
                            "pid": idx + 1,  
                            "problem": problem,  
                        }
                    )
                    idx += 1
                else:
                    print(Fore.RED + 'Invalid input'+Style.RESET_ALL)
                    continue
            while True:
                if idx_old == idx:
                    break
                print('-'*50)
                for QA in results["problems"][idx_old:idx]:
                    print('Question: '+ Fore.CYAN + QA["problem"]["Question"] + Style.RESET_ALL)
                    print('Answer: '+ Fore.RED + QA["problem"]["Answer"] + Style.RESET_ALL)
                review = input(f"共生成{idx-idx_old}个问题，需要更改本模板的第几个问题？(回车表示不需要)")
                while review != '' and not is_number(review):
                    review = input(f"共生成{idx-idx_old}个问题，需要更改本模板的第几个问题？(回车表示不需要)")


                if review != '':
                    review = int(review)
                    
                    QA = results["problems"][idx_old+review-1]
                    QA["problem"]["Question"] = modify_question_from_template(question, item["Element_instance"])
                    QA["problem"]["Answer"] = modify_answer()
                
                else: 
                    break
        with open(output_path, 'w', encoding='utf-8') as file:  
            json.dump(results, file, ensure_ascii=False, indent=4)   
if __name__ == "__main__":
    # 读取命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--fid', type=int, default=1, help='开始的图片序号')
    args = parser.parse_args()

    template_file = "template_questions_list.json"
    question_folder = "new"
    image_folder = "D:\senior\毕设\math\plane-geometry-data-generator\data\AngleDetectionBenchmark\images\\test"
    # image_folder = "/home/yangxw/math/plane-geometry-data-generator/data/AngleDetectionBenchmark/images/test"
    # 找出文件夹中所有id
    image_ids = []
    for file in os.listdir(image_folder):
        if file.endswith('.png'):
            image_ids.append(int(file.split('.')[0]))
    # 按照数字大小排序
    image_ids.sort()
    # print(image_ids[:100])
    for image_id in image_ids:
        if image_id < args.fid:
            continue
        if not os.path.exists(os.path.join(question_folder, 'autogeo')):
            os.makedirs(os.path.join(question_folder, 'autogeo'))
        file_path = os.path.join(question_folder, 'autogeo', 'questions_ver0226_'+str(image_id) + '.json')
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(os.path.join(question_folder, 'autogeo', 'questions_ver0226_'+str(image_id) + '.json'), 'w', encoding='utf-8') as file:
                empty = {
                    "image_id": image_id,
                    "problems": []
                }
                json.dump(empty, file, ensure_ascii=False, indent=4)
        
        rapid_process_question(template_file, question_folder, image_id)