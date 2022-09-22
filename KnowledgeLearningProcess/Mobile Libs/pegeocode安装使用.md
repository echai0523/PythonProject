
# pegeocode安装使用

- 安装
    - pip install pgeocode


- 获取经纬度、邮箱编号···等
    - nomi = pgeocode.Nominatim('au')
        - code = nomi.query_postal_code(str(int))
            - code.latitude  # 纬度
            - code.longitude # 经度
    - dist = pgeocode.GeoDistance('au')
        - dist.query_postal_code(str(int))



