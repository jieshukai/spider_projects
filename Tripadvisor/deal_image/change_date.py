import json

with open('yuyuan_zhCN.json', 'r', encoding='utf-8') as f:
    data = f.read()
data = json.loads(data)
for line in data:
    if line['image_paths']:
        image_path = line['image_paths']
        print(image_path)