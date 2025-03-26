import json  

def check_numbers_in_jsonl(file_path):  
    with open(file_path, 'r') as file:  
        for line in file:  
            record = json.loads(line.strip())  
            # 检查提问是否包含指定的句子  
            if 'Answer the question with an integer.' in record.get('Question', '') or 'Answer the question with a float.' in record.get('Question', ''):  
                answer = record.get('Answer', '')  
                answer = answer.replace(' ', '')  # 去除空格
                answer = answer.replace('.', '')  # 去除逗号
                try:
                    answer = eval(answer)  # 尝试将字符串转换为 Python 对象
                except:
                    if answer == 'wrongprerequisite' or answer == 'notgiven':  
                        continue
                    print(f"ID: {record['pid']} - Answer: {answer} is NOT an integer.")  
                    continue

def check_yes_or_no_in_jsonl(file_path):
    with open(file_path, 'r') as file:  
        for line in file:  
            record = json.loads(line.strip())  
            # 检查提问是否包含指定的句子  
            if 'Answer the question with \"yes\" or \"no\".' in record.get('Question', ''):  
                answer = record.get('Answer', '')  
                answer = answer.replace(' ', '')  # 去除空格
                answer = answer.replace('.', '')  # 去除逗号
                if answer != 'yes' and answer != 'no' and answer != 'wrongprerequisite' and answer != 'notgiven':
                    print(f"ID: {record['pid']} - Answer: {answer} is NOT yes or no.")  
                    continue

def check_choice_in_jsonl(file_path):
    with open(file_path, 'r') as file:  
        for line in file:  
            record = json.loads(line.strip())  
            # 检查提问是否包含指定的句子  
            if 'Answer the question with \"A\"' in record.get('Question', ''):  
                answer = record.get('Answer', '')  
                answer = answer.replace(' ', '')  # 去除空格
                answer = answer.replace('.', '')  # 去除逗号
                if answer != 'A' and answer != 'B' and answer != 'C' and answer != 'D' and answer != 'E' and answer != 'wrongprerequisite' and answer != 'notgiven':   
                    if 'If not' in record.get('Question', ''):
                        # 如果是其他类型的题目，是yes no也可以接受
                        if answer != 'yes' and answer != 'no':
                            print(f"ID: {record['pid']} - Answer: {answer} is NOT A, B, C, D, E.")  
                            continue
                    else:
                        print(f"ID: {record['pid']} - Answer: {answer} is NOT A, B, C, D, E.")  
                    continue
def check_problem_format(file_path):
    with open(file_path, 'r') as file:  
        for line in file:  
            record = json.loads(line.strip())  
            # 检查提问是否包含指定的句子  
            if 'answer the question with ' not in record.get('Question', '').lower():  
                print(f"ID: {record['pid']} - Question: {record.get('Question', '')} is NOT a problem format.")


# 调用函数并传入文件路径  
print('*'*20+'Checking numbers'+'*'*20)
check_numbers_in_jsonl('test.jsonl')  
print('*'*20+'Checking yes or no'+'*'*20)
check_yes_or_no_in_jsonl('test.jsonl')
print('*'*20+'Checking choice'+'*'*20)
check_choice_in_jsonl('test.jsonl')
print('*'*20+'Checking problem format'+'*'*20)
check_problem_format('test.jsonl')