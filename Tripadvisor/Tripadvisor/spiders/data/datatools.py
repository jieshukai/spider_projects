import pandas
import xlrd as xlrd


# 获取数据
def to_excel(from_path, to_path, sheet_name):
    data_str = open(from_path, encoding='utf-8').read()
    df = pandas.read_json(data_str, orient='records')
    df = df.drop(columns=['images', 'image_urls', 'image_paths'])
    print(df.head())
    df.to_excel(to_path, sheet_name=sheet_name)


if __name__ == '__main__':
    ch_path = './json/zhujiajiao_china.json'
    en_path = './json/zhujiajiao_en.json'
    to_excel(ch_path, './excel/zhujiajiao_china.xls', '中文评论')
    to_excel(en_path, './excel/zhujiajiao_en.xls', '英文评论')
