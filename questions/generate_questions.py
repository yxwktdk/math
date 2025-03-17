from openai import OpenAI
import base64
import json  
import ast
import os
from tqdm import tqdm
# 忽略所有warnings.warn
import warnings
warnings.filterwarnings("ignore")
from pydantic import BaseModel
class QAFormat(BaseModel):  
    Question: str  
    Answer: str 
class QAs(QAFormat):
    QAs: list[QAFormat]
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def generate_questions(data, image_id, client):  
    image_path = f"/home/trunk/RTrunk0/yangxw/math_data/images/image_{image_id}.png"
    image_path_re = f"images/image_{image_id}.png"
    print(f"-------------------Processing {image_path_re}-------------------")
    result_json = f"questions_ver0101_{image_id}.json"
    idx = 0
    # 初始化结果列表  
    results = {  
        "fid": 1,  
        "problems": []  
    }  
    base64_image = encode_image(image_path)

    # 遍历每个问题  
    for item in tqdm(data):  
        try:  
            # 提取问题相关信息  
            question = item["Question"]  
            question_type = item["Type"]  
            category = item["Category"]  
            subcategory = item["SubCategory"]  
            question_id = item["ID"]  

            # 创建第一个提示字符串  
            prompt1 = (  
                "You are a helpful assistant. Forget all previous instructions and focus only on the current task."  
                + f'I will input a geometric image and provide a question template. '  
                + f'Your task is to strictly follow the template to generate 0-4 questions and corresponding answers. '  
                + f'Notice that: '  
                + f'1. The generated questions must strictly follow the subject and structure of the template. '  
                + f'   - Only replace the geometric elements (e.g., points, line segments, triangles) in the template with elements present in the image, do not change other parts of the question. (e.g., replace "line AB" with "line AC", do not change other parts of the question). '  
                + f'   - Do not change the subject of the question (e.g., do not change "triangle" to "line segment"). '  
                + f'2. If the geometric elements in the template do not exist in the figure, reduce the number of questions. '  
                + f'   - If the element exists, generate more than 1 question, up to 4 questions based on the template, the more is the better. '  
                + f'3. The answer to the generated questions does not need to be determined. Use the following rules: '  
                + f'   - If the subject in the question does not exist or the prerequisite is wrong, answer "wrong prerequisite". '  
                + f'   - If the subject exists but the answer is not explicitly provided in the image, answer "not given". '   
                + f'4. Do not change the meaning or structure of the template. Only replace the geometric elements with those present in the image. On the basis of this, make the answer cover more types of template standard answers.'  
                + f'5. Keep the questions concise and complete. '
                + f'Example: '  
                + f'Input: Template: "Is triangle ABC present in this figure? Answer the question with \\"yes\\" or \\"no\\"." Image: [image] '  
                + f'Output: [{{"Question":"Is triangle DEF present in this figure? Answer the question with \\"yes\\" or \\"no\\".","Answer":"yes."}}, '  
                + f'{{"Question":"Is triangle AEF present in this figure? Answer the question with \\"yes\\" or \\"no\\".","Answer":"no."}}] '  
            )  

            # 调用第一个 API  
            response = client.beta.chat.completions.parse(  
                model="gpt-4o-mini",  
                messages=[  
                    {  
                        "role": "system",  
                        "content": prompt1,  
                    },  
                    {  
                        "role": "user",  
                        "content": [  
                            {  
                                "type": "text",  
                                "text": question,  
                            },  
                            {  
                                "type": "image_url",  
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},  
                            },  
                        ],  
                    },  
                ],  
                response_format=QAs,  
            )  

            # 解析响应  
            QAlist = response.choices[0].message.parsed.QAs  
            # print(QAlist)

            # 第二个提示词：验证生成的问题并修复  
            validation_prompt = (  
                f"You are a helpful assistant. Your task is to validate and, if necessary, fix generated questions based on a provided template. "  
                f"Here is the template: {question} "  
                f"Validation rules: "  
                f"1. The generated question must follow the subject and structure of the template. "  
                f"2. Only the geometric elements (e.g., points, line segments, triangles) can be replaced with elements present in the image. "  
                f"3. Do not allow changes to the subject of the question (e.g., do not change 'triangle' to 'line segment'). "  
                f"4. The meaning and structure of the template must remain unchanged. "  
                f"5. If a question is invalid, fix it by replacing the incorrect parts with valid geometric elements. "  
                f"Examples: "  
                f"Example 1: Template: 'What is the length of the line segment AC?' Answer the question with an integer. "  
                f"Generated Questions: "  
                f"  - 'What is the length of the line segment AB? Answer the question with an integer. ' -> valid "  
                f"  - 'What is the length of the line segment AC? ' -> invalid, add 'Answer the question with an integer.' "  
                f"  - 'What is the measure of the angle C? Answer the question with an integer. ' -> invalid, replace with 'What is the length of the line segment AO?' "  
                f"Example 2: Template: 'Is triangle ABC present in this figure?' Answer the question with 'yes' or 'no'. "  
                f"Generated Questions: "  
                f"  - 'Is triangle DEF present in this figure? Answer the question with 'yes' or 'no'. ' -> valid "  
                f"  - 'Is triangle XYZ present in this figure?' -> invalid,add 'Answer the question with 'yes' or 'no'.' "
                f"  - 'Is line segment AB present in this figure?' -> invalid, replace with 'Is triangle ABC present in this figure?' "  
            )  

            # 调用第二个 API 验证和修复问题  
            validation_response = client.beta.chat.completions.parse(  
                model="gpt-4o-mini",  
                messages=[  
                    {  
                        "role": "system",  
                        "content": validation_prompt,  
                    },  
                    {  
                        "role": "user",  
                        "content": [
                            {"type": "text", "text": 'The template is '+question},
                            {"type": "text", "text": 'Generated questions are'+str(QAlist)}
                        ],  
                    },  
                ],  
                response_format=QAs,
            )  

            # 获取验证后的问题  
            validated_QAs = validation_response.choices[0].message.parsed.QAs  

            # print(f"Validated QAs: {validated_QAs}")

            # 将验证后的问题存入结果  
            for QA in validated_QAs:  
                results["problems"].append(  
                    {  
                        "pid": idx + 1,  
                        "problem": {  
                            "Image": image_path_re,  # 这里可以替换为实际的图像路径  
                            "Question": QA.Question,  
                            "Type": question_type,  
                            "Category": category,  
                            "SubCategory": subcategory,  
                            "ID": question_id,  
                            "Answer": QA.Answer,  
                        },  
                    }  
                )  
                idx += 1 

        

        except Exception as e:  
            # 捕获异常并记录错误信息  
            print(f"Error processing item with ID {item['ID']}: {e}")  
            results["problems"].append({  
                "pid": idx + 1,  
                "problem": {  
                    "Image": image_path,  
                    "Question": question,  
                    "Type": question_type,  
                    "Category": category,  
                    "SubCategory": subcategory,  
                    "ID": question_id,  
                    "Answer": "Error occurred during processing"  
                }  
            })  
            idx += 1  

        # 保存结果到文件  
        with open(result_json, 'w', encoding='utf-8') as file:  
            json.dump(results, file, indent=4, ensure_ascii=False)  
        
    return results  

if __name__ == '__main__':

    images_folder = "/home/trunk/RTrunk0/yangxw/math_data/images"
    template_path = "template_questions_list.json"
    with open(template_path, 'r', encoding='utf-8') as file:  
        data = json.load(file)  
    client = OpenAI(
        api_key="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"
        )
    # image_path = "D:\senior\science\math\question\self\images\image_771.png"
    # 寻找文件夹下所有png图片
    image_list = []
    for root, dirs, files in os.walk(images_folder):
        for file in files:
            if file.endswith(".png"):
                image_list.append(file)
    # 排序并输出
    image_list.sort()
    print(image_list)
    for image in image_list:
        image_path = os.path.join(images_folder, image)
        # 获取'image_23.png'后的数字
        image_id = int(image.split('_')[-1].split('.')[0])
        
        results = generate_questions(data, image_id, client)
    
