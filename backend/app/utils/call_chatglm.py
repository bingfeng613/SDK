from zhipuai import ZhipuAI
client = ZhipuAI(api_key="8babc8325830424282e2a20c49440559.IXVO0sk5LUHWFSl6") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
    ],
)
print(response.choices[0].message)

