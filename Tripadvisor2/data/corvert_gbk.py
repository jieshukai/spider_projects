import json
import pandas

from pytz import unicode

with open('json/yuyan_en.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read().encode('gbk', errors='ignore').decode('gbk'))
df = pandas.DataFrame(data)
print(df)
df.to_csv('yuyan_en_csv.csv', encoding='gbk')
