import jieba  # 分词，一个句子分成很多词
from matplotlib import pyplot as plt  # 绘图，创建图形，在图形中创建绘图区域，绘制线条等
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图像处理
import numpy as np  # 矩阵运算，矢量算数运算等等，机器学习喜欢用
import sqlite3  # 数据库

# 数据库查询
con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = "select instroduction from movie250"
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
# print(text)
cur.close()
con.close()

# 进行分词
cut = jieba.cut(text)
# print(cut)    # cut 返回一个可迭代的数据类型对象，只需要每次都取即可
string = ' '.join(cut)
print(string)

# 绘图设置
img = Image.open(r'./static/assets/img/tree.jpg')  # 打开图片，r 防止\转移
img_array = np.array(img)  # 将图片转换为数组，方便 np 库计算。
wc = WordCloud(  # 词云参数设置
    background_color='pink',  # 设置背景颜色
    mask=img_array,  # 设置背景图片
    font_path="msyh.ttc"  # 若是有中文，这句代码必须添加，不然会出现方框，不出现汉字
)
wc.generate_from_text(string)  # 从哪个文本按照 wc 的设置生成

# 绘制图片
fig = plt.figure(1)  # 可以将该 1 理解为窗口的属性 id，即该窗口的身份标识。
plt.imshow(wc)  # 按照 wc 显示图片
plt.axis('off')  # 不显示坐标轴
# plt.show()  # 显示生成的图片，但直接显示，没有保存功能
plt.savefig(r'./static/assets/img/word.jpg', dpi=500)
