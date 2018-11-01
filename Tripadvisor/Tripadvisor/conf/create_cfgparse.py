import configparser

parser = configparser.ConfigParser()
parser.read_dict(
    {
        'waitan': {
            'name': 'waitan',
            'verbose_name': '上海外滩',
            'language': 'zhCN',
            'start_url': 'https://www.tripadvisor.cn/Attraction_Review-g308272-d311595-Reviews-The_Bund_Wai_Tan-Shanghai.html',
            'page_num': 1,


        },
        'zhujiajiao': {
            'name': 'zhujiajiao',
            'verbose_name': '朱家角',
            'language': 'zhCN',
            'start_url': 'https://www.tripadvisor.cn/Attraction_Review-g308272-d1805650-Reviews-Zhujiajiao_Ancient_Town-Shanghai.html',
            'page_num': 1,

        },
        'fazujie': {
            'name': 'fazujie',
            'verbose_name': '法国租界',
            'language': 'zhCN',
            'start_url': 'https://www.tripadvisor.cn/Attraction_Review-g308272-d1143615-Reviews-Former_French_Concession-Shanghai.html',
            'page_num': 1,

        },
        'yuyan': {
            'name': 'yuyuan',
            'verbose_name': '上海豫园',
            'language': 'zhCN',
            'start_url': 'https://www.tripadvisor.cn/Attraction_Review-g308272-d324259-Reviews-Yu_Garden_Yuyuan-Shanghai.html',
            'page_num': 1,

        },
        'center_shanghai': {
            'name': 'center_shanghai',
            'verbose_name': '上海金融中心',
            'language': 'zhCN',
            'start_url': 'https://www.tripadvisor.cn/Attraction_Review-g308272-d1196260-Reviews-Shanghai_World_Financial_Center-Shanghai.html',
            'page_num': 1,

        },
        'disneyland': {
            'name': 'disneyland',
            'verbose_name': '上海迪士尼',
            'language': 'zhCN',
            'start_url': 'https://www.tripadvisor.cn/Attraction_Review-g308272-d10383031-Reviews-Shanghai_Disneyland-Shanghai.html',
            'page_num': 1,

        },

    })
if __name__ == '__main__':
    with open('spider.cfg', 'w', encoding='utf-8') as f:
        parser.write(f)
