import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import re
import xlwt
import time

# 存放正则规则
findLink = re.compile(r'<a href="(.*?)">')
# 图片的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 忽略换行符
# 影片的片名的规则
findTitle = re.compile(r'<span class="title">(.*?)</span>')
# 影片评分的规则
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 评论人数的规则
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 概述相关的规则
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 影片相关内容的规则
findDb = re.compile(r'<p class="">(.*?)</p>', re.S)  # 忽视换行符


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1、爬取网页
    datalist = getData(baseurl)
    print(datalist)
    savepath = "豆瓣电影Top250.xls"
    # 2、逐一解析数据
    # 3、保存数据
    saveData(datalist, savepath)


# 爬取网页函数
def getData(baseurl):
    datalist = []
    # askURL 需要调用 25 次，达到 250 条数据都要拿到，所以用循环
    for i in range(0, 10):  # 0 - 10 页，抓取 10 次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的页面源码
        # 解析每一个网页
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_="item"):
            # print(item) # 测试查看电影全部信息
            data = []  # 用户保存一部电影的所有信息
            item = str(item)
            # 获取影片的链接
            link = re.findall(findLink, item)[0]  # 利用正则查找你要找的内容，findLink 是全局变量，存放正则规则
            # print(link)
            data.append(link)  # 添加链接
            # 获取影片的图片
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片
            # 获取影片的名字
            titles = re.findall(findTitle, item)  # 片名可能有一个中文名，没有外国名，也有可能有
            if (len(titles)) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号
                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名留空
            # 获取影片的评分
            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加影片评分
            # 获取评论人数
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评论人数
            # 获取影片概述
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")  # 留空
            bd = re.findall(findDb, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub("/", " ", bd)  # 替换 /
            data.append(bd.strip())  # 去掉前后的空格
            datalist.append(data)  # 把处理好的一部电影添加到 datalist
        time.sleep(1)
        a = '*' * 10 * i
        b = '.' * (10 - i) * i
        c = (i / 10) * 100
        print("\r{:^3.0f}%[{}->{}]".format(c, a, b), end="")
        # print(len(datalist))
    # print("\r{:^3.0f}%[{}->{}]".format(c, a, b), end="")
    return datalist


# 得到指定一个 URL 的网页内容
def askURL(url):
    # 用户代理，告诉代理，我们是什么类型的机器，什么样的浏览器
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
    request = urllib.request.Request(url=url, headers=head)
    html = ""
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    # try:
    #     response = urllib.request.urlopen(request)
    #     html = response.read().decode("utf-8")
    # print(html)
    # except urllib.error.URLError as e:
    #     # hasattr() 函数用于判断对象是否包含对应的属性。
    #     if hasattr(e, "code"):
    #         print(e.code)
    #     if hasattr(e, 'reason'):
    #         print(e.reason)
    return html


# 保存数据函数
def saveData(datalist, savepath):
    #  使用 Workbook 创建一个对象,utf-8 可以输入中文，style... 是否压缩，不常用
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 参数 1 是文档名字，参数 2 是覆盖写入
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    # 定义一个元组，写入到表中
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评论数", "概况", "相关信息")
    for i in range(0, 8):  # 循环遍历把上面的 col 写入到表中
        sheet.write(0, i, col[i])  # 列名
    for i in range(1, 251):  #
        data = datalist[i - 1]
        for j in range(0, 8):
            sheet.write(i, j, data[j])
        book.save(savepath)


if __name__ == "__main__":
    main()
    time.sleep(1)
