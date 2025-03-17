import json  
import os  
import time
import argparse
from tqdm import tqdm
from colorama import Fore, Style 
def load_json(file_path, id=None):  
    """读取JSON文件并返回数据"""  
    if os.path.getsize(file_path) == 0:  # 检查文件是否为空  
        # red output 文件为空
        print(Fore.RED + f"{file_path} is empty." + Style.RESET_ALL)
        return {"fid": id, "problems": []}  # 返回默认值  
    with open(file_path, "r", encoding="utf-8") as f:  
        return json.load(f)  
def is_number(s):  
    try:  
        float(s)  # 尝试将字符串转换为浮点数  
        return True  
    except ValueError:  
        return False 
def save_questions(data, output_path):  
    """将更新后的数据保存到指定路径"""  
    with open(output_path, 'w', encoding='utf-8') as f:  
        json.dump(data, f, ensure_ascii=False, indent=4)  

def update_image_and_pid(problem, image_path, new_pid):  
    """更新问题的Image路径和pid"""  
    problem["problem"]["Image"] = image_path  
    problem["pid"] = new_pid  
def modify_question_from_template(question, elements):
    # 根据模板的问题，查找对应元素所在位置，点对点修改
    original_question = question 

    for i, element in enumerate(elements):
        print("待更改元素: ", element)
        new_elem = input("***修改元素为：(按回车表示不修改): ")

        if new_elem != '':
            if all(elem.replace(" ", "") not in new_elem for elem in elements[i+1:]):
                # 获取原始元素的前导和尾随空格  
                left_spaces = len(element) - len(element.lstrip())  
                right_spaces = len(element) - len(element.rstrip())  
                
                # 构建新元素，保持原有的空格  
                new_element = ' ' * left_spaces + new_elem + ' ' * right_spaces  
                
                # 替换问题中的元素  
                question = question.replace(element, new_element) 
            else:
                action = input("元素替代存在包含关系，请手动输入或选择其他组合（回车）")
                if action == '':
                    return modify_question_from_template(question, elements)
                else:
                    question = action.strip()
                    break
                
    print(Fore.YELLOW +f"{question}，需手动修改？" + Style.RESET_ALL)

    return question


def modify_answer():
    action = input("***g. not given, p. wrong prerequisite, y. yes, n. no, 或自行输入合法答案：").strip().lower()
    print("Answer: ", end="")
    if action == 'g':
        print(Fore.GREEN + "not given."+ Style.RESET_ALL)
        return "not given."
    elif action == 'p':
        print(Fore.GREEN + "wrong prerequisite."+ Style.RESET_ALL)
        return "wrong prerequisite."
    elif action == 'y':
        print(Fore.GREEN + "yes."+ Style.RESET_ALL)
        return "yes."
    elif action == 'n':
        print(Fore.GREEN + "no."+ Style.RESET_ALL)
        return "no."
    elif action == 'a' or action == 'b' or action == 'c' or action == 'd' or action == 'e' or action == 'f':
        print(Fore.GREEN + f"{action.capitalize()}."+ Style.RESET_ALL)
        return f'{action.capitalize()}.'
    # 接下来判断是否为数字
    elif is_number(action):
        print(Fore.GREEN + f"{action}."+ Style.RESET_ALL)
        return action + '.'
    else:
        print("无效输入，请重新输入。")
        return modify_answer()
def modify_problem(problem, template_question, template_elements):  
    """允许用户修改问题或答案"""  
    act_ls = []
    while True:  
        action = input("***需要对问题进行何种操作？a. 直接从模板修改问题 b. 修改答案 c. 直接输入新问题 ig. 此问题忽略(回车退出)").strip().lower()
        act_ls.append(action)
        if action == 'c':  
            new_question = input("请输入新的问题: ")  
            problem["Question"] = new_question  
            problem["Answer"] = modify_answer()
        elif action == 'b':  
            problem["Answer"] = modify_answer()
        elif action == 'a':
            problem["Question"] = modify_question_from_template(template_question, template_elements)
            problem["Answer"] = modify_answer()
        elif action == 'ig':
            return None
        elif action == '':  
            break  
        else:  
            print("无效输入，请重新输入。")  
        # 如果a和bc都执行过，自动退出循环
        if 'a' in act_ls or 'c' in act_ls:
            break
    return problem


def handle_problem_deletion_or_addition(problem, template_qeustion, template_elements):  
    """处理问题的删除或添加"""  
    problems = [problem]
    while True:  
        modify_action = input("***是否需要删除、添加问题？ a. 删除本问题 b. 添加新问题 (按回车表示本步骤结束): ").strip().lower() 
        if modify_action == 'a':  
            problems.remove(problem)  
            print("问题已删除。")  
        elif modify_action == 'b':  
            # 输出当前问题信息  
            new_problem = {  
                "Question": modify_question_from_template(template_qeustion, template_elements), 
                "Answer": modify_answer(), 
            }  
            problems.append(new_problem)
            print("新问题已添加。") 
        elif modify_action == '':  
            break  
        else:  
            print("无效输入，请重新输入。")  
    return problems
def find_ID_QAs(problems_raw, ID):  
    """查找指定ID的问题和答案"""  
    problems = []
    for problem in problems_raw:  
        if problem["problem"]["ID"] == ID:  
            problems.append(problem["problem"])
    return problems
def process_questions(data, template, output_path, tid, fid):  
    """处理所有问题"""  
    problems_raw = data.get("problems", [])  
    image_path = problems_raw[0]["problem"]["Image"] if problems_raw else ""
    
    results = load_json(output_path, fid)
    idx = results["problems"][-1]["pid"] if results["problems"] else 0
    for item in tqdm(template):
        # 绿色输出当前是第几个问题
        idx_old = idx
        question_id = item["ID"] 
        if question_id < tid:
            continue
        question = item["Question"]  
        question_type = item["Type"]  
        category = item["Category"]  
        subcategory = item["SubCategory"]  
        
        print(Fore.GREEN + f"********Processing: {question_id}/{len(template)}********" + Style.RESET_ALL)
        
        print(Fore.YELLOW + 'Template: '+question + Style.RESET_ALL)
        # 查找指定ID的问题和答案
        problems = find_ID_QAs(problems_raw, question_id) 
        len_id = len(problems)
        if len_id == 0:
            print(f"ID为{question_id}的问题不存在。")
            while True:
                action = input("***是否需要手动输入问题？a. 手动输入问题,按回车表示不需要手动输入: ").strip().lower()
                if action == 'a':
                    problem = {
                        "Image": image_path,  # 这里可以替换为实际的图像路径  
                        "Question": modify_question_from_template(question, item["Element_instance"]),
                        "Type": question_type,  
                        "Category": category,  
                        "SubCategory": subcategory,  
                        "ID": question_id,  
                        "Answer": modify_answer(),  
                    }
                    results["problems"].append(
                        {
                            "pid": idx + 1,  
                            "problem": problem,  
                        }
                    )
                    idx += 1
                elif action == '':
                    break   

        for i, QA in enumerate(problems): 
            # print(problems)
            print(Fore.BLUE + f'Processing: {i+1}/{len_id}' + Style.RESET_ALL)
            problem = {  
                        "Image": image_path,  # 这里可以替换为实际的图像路径  
                        "Question": QA["Question"],  
                        "Type": question_type,  
                        "Category": category,  
                        "SubCategory": subcategory,  
                        "ID": question_id,  
                        "Answer": QA["Answer"],  
                    }
            print('Question: '+ problem["Question"])
            print('Answer: '+ Fore.RED + problem["Answer"] + Style.RESET_ALL)
            problem = modify_problem(problem, question, item["Element_instance"])
            if problem == None:
                print('本个模板问题已忽略。')
                break
            if (i != len_id - 1 and problem['Question'] == QA['Question'] and problem['Answer'] == QA['Answer']) or (i == len_id - 1):
                problems = handle_problem_deletion_or_addition(problem, question, item["Element_instance"])
                for new_problem in problems:
                    problem = {
                        "Image": image_path,  # 这里可以替换为实际的图像路径  
                        "Question": new_problem["Question"],  
                        "Type": question_type,  
                        "Category": category,  
                        "SubCategory": subcategory,  
                        "ID": question_id,  
                        "Answer": new_problem["Answer"],  
                    }
                    results["problems"].append(
                        {
                            "pid": idx + 1,  
                            "problem": problem,  
                        }
                    )
                    idx += 1
            else:
                results["problems"].append(
                        {
                            "pid": idx + 1,  
                            "problem": problem,  
                        }
                    )
                idx += 1

        while True:
            if idx_old == idx:
                break
            
            print('-'*50)
            for QA in results["problems"][idx_old:idx]:
                print('Question: '+ Fore.BLUE + QA["problem"]["Question"] + Style.RESET_ALL)
                print('Answer: '+ Fore.RED + QA["problem"]["Answer"] + Style.RESET_ALL)

            review = input(f"共生成{idx-idx_old}个问题，需要更改本模板的第几个问题？(回车表示不需要)")
            # 如果输入的不是数字或者空集合，则重新要求输入
            while review != '' and not is_number(review):
                review = input(f"共生成{idx-idx_old}个问题，需要更改本模板的第几个问题？(回车表示不需要)")


            if review != '':
                review = int(review)
                
                QA = results["problems"][idx_old+review-1]
                QA["problem"]["Question"] = modify_question_from_template(question, item["Element_instance"])
                QA["problem"]["Answer"] = modify_answer()
                
            else: 
                break
        print(Fore.GREEN + f"已处理 {idx} 个问题。" + Style.RESET_ALL)
        with open(output_path, 'w', encoding='utf-8') as file:  
            json.dump(results, file, indent=4, ensure_ascii=False)  
            

if __name__ == "__main__":  
    # 设置命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--fid', type=int, default=4, help='问题ID')
    parser.add_argument('--tid', type=int, default=1, help='模板ID')
    args = parser.parse_args()
    
    file_name = "questions_ver0101_" + str(args.fid) + ".json"
    template_path = "template_questions_list.json"

    
    file_path_old = os.path.join("raw", file_name)
    output_path = os.path.join("new", file_name)
    # 新建output_path文件
    if not os.path.exists(output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("")
    data = load_json(file_path_old)  
    template = load_json(template_path)
    process_questions(data, template, output_path, args.tid, args.fid)