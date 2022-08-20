# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/20 10:05

input: 
output: 
Short Description: 
    - 逻辑：(https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/variance-standard-deviation-sample/a/population-and-sample-standard-deviation-review)
        - 1. 求均值
        - 2. 从每个分数中减去平均值
        - 3. 对每个偏差进行平方
        - 4. 平方偏差之和
        - 总体标准差
            - 5. 求方差，平方偏差之和除以个数
        - 样本标准差
            - 5. 求方差，平方偏差之和除以(个数-1)
        - 6. 对第 5 步的结果求平方根
Change History:

"""
import math


def sd(ar, sample=False):
    # 求和
    ar_sum = 0
    for a in ar:
        ar_sum += 0
    # 1. 求平均值
    mean_value = ar_sum / len(ar)
    print("平均值：", mean_value)
    # 2. 求偏差
    deviation_value = [a - mean_value for a in ar]
    print("偏差：", deviation_value)
    # 3. 每个偏差进行平方
    deviation_square = [deviation ** 2 for deviation in deviation_value]
    print("偏差平方：", deviation_square)
    # 4. 添加平方偏差
    deviation_square_sum = 0
    for d_s in deviation_square:
        deviation_square_sum += d_s
    print("平方偏差和：", deviation_square_sum)

    if sample:
        # 5. 求(方差-1) 并 对(方差-1)求平方根
        result_value = math.sqrt(deviation_square_sum / (len(ar) - 1))
        print("结果：", result_value)
    else:
        # 5. 求方差 并 对方差求平方根
        result_value = math.sqrt(deviation_square_sum / len(ar))
        print("结果：", result_value)

    return result_value


a = [1, 6, 7, 3, 9]
print(sd(a, True))
print(sd(a, False))




