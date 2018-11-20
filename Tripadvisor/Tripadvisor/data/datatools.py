import pandas
import xlrd as xlrd


# 获取数据


def to_excel(from_path, to_path, sheet_name):
    writer = pandas.ExcelWriter(to_path)

    data_str = open(from_path, encoding='utf-8').read()
    df = pandas.read_json(data_str, orient='records')
    df = df.drop(columns=['images', 'image_urls'])
    print(df.head())
    df.to_excel(writer, sheet_name=sheet_name)

    writer.save()

def main():
    from Tripadvisor.start import section

    name = section.get('name')

    ch_path = './data/json/{}_zhCN.json'.format(name)
    en_path = './data/json/{}_en.json'.format(name)
    to_excel(ch_path, './data/excel/{}_zhCN.xls'.format(name), '中文评论')
    to_excel(en_path, './data/excel/{}_en.xls'.format(name), '英文评论')
