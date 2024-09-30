# 导入自动化模块
from DrissionPage import ChromiumPage
# 导入格式化输出模块
from pprint import pprint
# 导入csv模块
import csv
# 导入时间模块
import time
# 创建文件对象
f = open('data.csv', mode='w', encoding='utf-8', newline='')
# 字典写入的方法
csv_writer = csv.DictWriter(f, fieldnames=[
     '职位',
     '薪资',
     '公司',
     '城市',
     '区域',
     '街道',
     '学历',
     '经验',
     '领域',
     '规模',
     '福利',
 ])
# 写入表头
csv_writer.writeheader()
# 实例化浏览器对象
dp = ChromiumPage()
# 监听数据包地址
dp.listen.start('/search/positions')
# 获取输入
city = input('请输入要爬取的城市：')
p = int(input('请输入要爬取的页码数：'))
# 城市编码
city_code_dict = {
    '上海': 538, '北京': 530, '广州': 763, '深圳': 765, '天津': 531,
    '武汉': 736, '西安': 854, '成都': 801, '南京': 635, '杭州': 653,
    '重庆': 551, '厦门': 682, '大连': 600, '无锡': 636
}
city_code = city_code_dict[city]

# 访问网站
# 数据分析 kwCLO66RII0PJP0
# python
dp.get(f'https://zhaopin.com/sou/jl{city_code}/kwCLO66RII0PJP0/p2')
# https://sou.zhaopin.com/?jl={city_code}&kw=数据分析&p={p}
# 设置延时等待
time.sleep(2)
# 下滑页面到底部
dp.scroll.to_bottom()
# 点击上一页
dp.ele('css:.soupager__btn').click()
for page in range(1, p+1):
    print(f'正在采集第{page}页的数据内容')
    # 下滑页面到底部
    dp.scroll.to_bottom()
    # 等待数据包加载
    resp = dp.listen.wait()
    # 获取响应的数据
    json_data = resp.response.body
    """解析数据"""
    # 字典取值, 提取职位信息所在列表
    job_list = json_data['data']['list']
    # for循环遍历, 提取列表里面元素
    for index in job_list:
        dit = {
            '职位': index['name'],
            '薪资': index['salary60'],
            '公司': index['companyName'],
            '城市': index['workCity'],
            '区域': index['cityDistrict'],
            '街道': index['streetName'],
            '学历': index['education'],
            '经验': index['workingExp'],
            '领域': index['industryName'],
            '规模': index['companySize'],
            '福利': ' '.join(index['jobKnowledgeWelfareFeatures']),
        }
        # 写入数据
        csv_writer.writerow(dit)
        print(dit)
    # 点击下一页按钮
    dp.ele('css:.soupager a:last-of-type').click()

# 导入数据处理模块
import pandas as pd
# 导入可视化配置项
from pyecharts import options as opts
# 导入可视化饼图方法
from pyecharts.charts import Pie
# 导入可视化数据(随机生成)
from pyecharts.faker import Faker
# 读取csv文件
df = pd.read_csv('data.csv')

x = df['学历'].value_counts().index.to_list()
y = df['学历'].value_counts().to_list()


c = (
    Pie()
    .add(
        "",
        [
            list(z)
            # 传入数据内容
            for z in zip(
                x,
                y,
            )
        ],
        center=["40%", "50%"],
    )
    # 设置全局配置
    .set_global_opts(
        # 设置可视化标题
        title_opts=opts.TitleOpts(title="北京关于Python招聘学历要求分布"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    # 导出可视化效果, 保存html文件
    .render("pie_北京关于Python招聘学历要求分布.html")
)


x = df['经验'].value_counts().index.to_list()
y = df['经验'].value_counts().to_list()


c = (
    Pie()
    .add(
        "",
        [
            list(z)
            # 传入数据内容
            for z in zip(
                x,
                y,
            )
        ],
        center=["40%", "50%"],
    )
    # 设置全局配置
    .set_global_opts(
        # 设置可视化标题
        title_opts=opts.TitleOpts(title=f"{city}招聘经验要求分布"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    # 导出可视化效果, 保存html文件
    .render(f"pie_{city}招聘经验要求分布.html")
)
