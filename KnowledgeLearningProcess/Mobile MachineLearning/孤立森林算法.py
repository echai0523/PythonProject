import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pmdarima as pm
from fbprophet import Prophet

matplotlib.rcParams['axes.unicode_minus'] = False
# 解决图像显示中文的问题
sns.set(font="Kaiti", style="ticks", font_scale=1.4)


# 判断并返回异常值
def outlier_detection(forecast):
    index = np.where((forecast["y"] <= forecast["yhat_lower"]) |
                     (forecast["y"] >= forecast["yhat_upper"]), True, False)
    return index


if __name__ == "__main__":
    # 数据准备
    data_ini = pd.read_csv('Ar.csv')
    data = pm.datasets.load_gasoline()
    datadf = pd.DataFrame({"y": data_ini['PM2']})
    datadf["ds"] = data_ini['B']
    # 可视化时间序列的变化情况
    datadf.plot(x="ds", y="y", style="b-o", figsize=(14, 7))
    plt.ylabel('样\n本\n值\n', rotation=0, verticalalignment='bottom',
               horizontalalignment='left', labelpad=19, y=0.36)
    plt.grid()
    plt.savefig('时间序列结果.pdf')
    plt.show()

    model = Prophet(growth="linear", daily_seasonality=False,
                    weekly_seasonality=False,
                    seasonality_mode='multiplicative',
                    interval_width=0.95,  # 获取95%的置信区间
                    )
    model = model.fit(datadf)  # 使用数据拟合模型
    forecast = model.predict(datadf)  # 使用模型对数据进行预测
    forecast["y"] = datadf["y"].reset_index(drop=True)
    # 输出前5行已有数据
    forecast[["ds", "y", "yhat", "yhat_lower", "yhat_upper"]].head()
    outlier_index = outlier_detection(forecast)
    outlier_df = datadf[outlier_index]  # 异常数据
    print("异常值的数量为:", sum(outlier_index))

    # 可视化异常值的结果
    fig, ax = plt.subplots()
    # 置信区间可视化
    ax.fill_between(forecast["ds"].values, forecast["yhat_lower"],
                    forecast["yhat_upper"], color='b', alpha=.2,
                    label="95%置信区间")
    # 预测值可视化
    forecast.plot(x="ds", y="yhat", style="b-", figsize=(14, 7),
                  label="预测值", ax=ax)
    # kind="scatter"意思为制作散点图,s控制点的大小
    forecast.plot(kind="scatter", x="ds", y="y", c="k", s=20, label="原始数据", ax=ax)
    # 异常值点可视化
    outlier_df.plot(kind="scatter", x="ds", y="y", s=60, style="rs", ax=ax, label="异常值")
    plt.ylabel('样\n本\n值\n', rotation=0, verticalalignment='bottom', horizontalalignment='left', labelpad=19, y=0.36)
    plt.legend(loc=2)
    plt.grid()
    plt.savefig('时间序列结果预测加异常值检测.pdf')
    plt.show()
