import requests
from bs4 import BeautifulSoup
import pandas as pd

# 输入xlsx路径，eg: AP-美国-语言项目.xlsx
in_path = r"AP-美国-语言项目.xlsx"
# 输出路径，即保存的路径，eg: r'AP美国学校.xlsx'， 若该路径为in_path同路径，则会覆盖原xlsx
out_path = r'AP美国学校.xlsx'
# 读取项目表格，构建学校list
df = pd.read_excel(r'AP-美国-语言项目.xlsx')
school_list = [s for s in df["学校"]]
# 初始学生人数list为空
name_count_map = dict()

headers = {
    "cookie": "",
    'User-Agent': ""
}

for page in range(1, 644):
    url = f'https://www.niche.com/k12/search/schools-with-ap-program/?page={page}'
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'lxml')
    schools = soup.select(".search-results__list__item")

    for school in schools:
        if school.find('div', class_="search-result__title-wrapper") is None:
            continue
        else:
            name = school.find('div', class_="search-result__title-wrapper").find("h2").get_text()
            students = school.find('ul', class_='search-result-fact-list').find('p').get_text()
            name_count_map[name] = students.replace('Students ', '').replace(',', '')


df['学生人数'] = df['学校'].apply(lambda x: name_count_map.get(x, ''))
df.to_excel(out_path, index=False, encoding='utf-8')

