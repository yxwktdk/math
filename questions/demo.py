import base64
from openai import OpenAI

client = OpenAI(
  api_key="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"
)
# client = OpenAI(
#   api_key="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"
# )
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "/home/yangxw/math/image_771.png"

# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in this image?",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)

print(response.choices[0].message)
# from openai import OpenAI
# import base64

# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')
# image_path = "/home/yangxw/math/image_771.png"
# base64_image = encode_image(image_path)
# # client = OpenAI(
# #   api_key="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"
# # )
# client = OpenAI(
#   api_key="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"

# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[  
#     {"role": "user", "content": "Who are you?"},
# ]
# )
# # completion = client.chat.completions.create(
# #   model="gpt-4o-mini",
# #   store=True,
# #   messages=[
# #     {"role": "user", "content": [
# #         {"type":"text", "text":"What's in this image?"},
# #         {"type":"image_url", "image_url":f"data:image/png;base64,{base64_image}"}
# #     ]}
# #   ]
# # )

# print(completion.choices[0].message)
