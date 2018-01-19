# -*- coding=utf-8 -*-
import json
import re
import requests
from bs4 import BeautifulSoup
import urllib
import os
import pymysql

# 新浪微博爬虫类
class SINABLOG:
    # 初始化方法，定义一些变量
    def __init__(self):
        # 存放每篇日志的信息
        self.stories = []
        # 存放每个博主昵称
        self.blogname = []
        # 指示第几个博主
        self.index = 0
        # 每个博主有多少篇博文
        self.blogcount = []
        # 每个博主的博文页数
        self.blogpages = []
        # 爬取的博文数量
        self.n = []

    # # 从文本中获取要爬取的博客主页地址
    # def getBlog_main_url(self):
    #     fp = open("Blog_main_url")
    #     main_url = []
    #     for line in fp:
    #         if (line != '') & (line != '\n'):
    #             main_url.append(line.rstrip('\n'))
    #     fp.close()
    #     return main_url

    # 获取博主昵称
    def getBlognameCatalog_url(self, main_url):
        maxnum = 10
        for tries in range(maxnum):
            try:
                res = requests.get(main_url)
                res.encoding = 'utf-8'
                break
            except Exception as e:
                if tries < (maxnum - 1):
                    continue
                else:
                    print(Exception, ':', e)
                    print('getBlogname')
                    return -1
        soup = BeautifulSoup(res.text, 'lxml')
        self.blogname.append(soup.select('.info_nm')[0].text.strip())
        # 获取第一页博文目录链接地址
        catalogurl = soup.select('.blognavInfo span a')[1].get('href')
        return catalogurl

    # 获取博文内容中的图片
    def getImage(self, blogurl, title):
        reg = r'real_src="(.+?)"'
        imgre = re.compile(reg)
        maxnum = 10
        for tries in range(maxnum):
            try:
                res = requests.get(blogurl)
                res.encoding = 'utf-8'
                break
            except Exception as e:
                if tries < (maxnum - 1):
                    continue
                else:
                    print(Exception, ':', e)
                    print('getIamge')
                    return -1
        soup = BeautifulSoup(res.text, 'lxml')
        imglist = re.findall(imgre, str(soup.select('.articalContent')[0]))
        if len(imglist) > 0:
            x = 0
            path = '.\BlogImage\{}'.format(self.blogname[self.index] + '\\' + title)
            if not os.path.exists(path):
                os.makedirs(path)
            for imgurl in imglist:
                maxnum = 10
                if os.path.exists('{}\%s.jpg'.format(path) % x):
                    x += 1
                    continue
                for tries in range(maxnum):
                    try:
                        urllib.request.urlretrieve(imgurl, '{}\%s.jpg'.format(path) % x)
                        break
                    except Exception as e:
                        if tries < (maxnum - 1):
                            continue
                        else:
                            print(Exception, ':', e)
                            break
                x += 1
        return 0

    # 获取博文总量
    def getBlogCount(self, catalogurl):
        maxnum = 10
        for tries in range(maxnum):
            try:
                res = requests.get(catalogurl)
                res.encoding = 'utf-8'
                break
            except Exception as e:
                if tries < (maxnum - 1):
                    continue
                else:
                    print(Exception, ':', e)
                    print('getBlogCount')
                    return -1
        soup = BeautifulSoup(res.text, 'lxml')
        # 博文数量
        self.blogcount.append(int(soup.select('.title em')[0].text.lstrip('(').rstrip(')')))
        return 0

    # 获取博文详细内容
    def getBlogDetails(self, i, catalogurl, needimg):
        result = {}
        # 正则匹配博文目录页面
        reg = r'\d+.html'
        blogre = re.compile(reg)

        # 当前页码
        curpage = i//50 + 1
        i = i % 50
        catalogurl = re.sub(blogre, str(curpage) + '.html', catalogurl)
        maxnum = 10
        for tries in range(maxnum):
            try:
                res = requests.get(catalogurl)
                res.encoding = 'utf-8'
                break
            except Exception as e:
                if tries < (maxnum - 1):
                    continue
                else:
                    print(Exception, ':', e)
                    print('getBlogDetals page')
                    return -1
        soup = BeautifulSoup(res.text, 'lxml')
        # 获取每篇博文的发布时间
        timesource = soup.select('.atc_tm')[i].text.strip()
        # 获取博文日志链接地址
        blogurl = soup.select('.atc_title a')[i].get('href')
        maxnum = 10
        for tries in range(maxnum):
            try:
                res2 = requests.get(blogurl)
                res2.encoding = 'utf-8'
                break
            except Exception as e:
                if tries < (maxnum - 1):
                    continue
                else:
                    print(Exception, ':', e)
                    print('getBlogDetails blogurl')
                    return -1
        soup2 = BeautifulSoup(res2.text, 'lxml')
        labellist = soup2.select('h3')
        label = []
        if len(labellist) > 0:
            for l in labellist:
                label.append(l.text)
        result['title'] = soup2.select('.articalTitle h2')[0].text.lstrip('\n').replace('\xa0', '')
        result['author'] = self.blogname[self.index]
        result['time'] = timesource
        result['tag'] = label
        # 如果有分类，则放入
        if len(soup2.select('.blog_class a')) > 0:
            result['class'] = soup2.select('.blog_class a')[0].text
        else:
            result['class'] = ''
        # 得到博文id
        m = re.search('blog_(.*?).html', blogurl)
        blogid = m.group(1)
        commenturl = 'http://blog.sina.com.cn/s/comment_{}_page.html?comment_v=articlenew'.format(blogid)
        comment_num = []
        commentlist = []
        page = 1
        # 获取评论页数，总量
        while 1:
            curl = commenturl.replace('page', str(page))
            maxnum = 10
            for tries in range(maxnum):
                try:
                    res3 = requests.get(curl)
                    res3.encoding = 'utf-8'
                    break
                except Exception as e:
                    if tries < (maxnum - 1):
                        continue
                    else:
                        print(Exception, ':', e)
                        print('getBlogDetails curl')
                        return 1
            jd = json.loads(res3.text)
            comment_num.append(int(jd['data']['comment_num']))
            comment_total_num = int(jd['data']['comment_total_num'])
            for j in range(0, comment_num[page - 1]):
                comment = {'uname': jd['data']['comment_data'][j]['uname'],
                           'body': str(urllib.parse.unquote(jd['data']['comment_data'][j]['cms_body'])),
                           'pubdate': jd['data']['comment_data'][j]['cms_pubdate']}
                comment['body'] = comment['body'].replace('<br>', '\n')
                commentlist.append(comment)
            if sum(comment_num) == comment_total_num:
                break
            page = page + 1
        result['comment_total_num'] = int(comment_total_num)
        result['content'] = str(soup2.select('.articalContent')[0].text).replace('\n', '').replace('%', '')
        result['comment'] = commentlist
        if needimg:
            rstr = r'[\/\\\<\>\:\"\|\*\?\']'
            self.getImage(blogurl, str(re.sub(rstr, '', result['title'])))
        return result

    # 开始方法
    def start(self, mainurl, maxcount, needimg):
        # 将博文信息插入表格bolgcontent
        sql1 = "insert into blogcontent(author,title,tag,class,pubtime,comment_total_num,content) values(\
               %s,%s,%s,%s,%s,%s,%s);"
        # 将每篇博文的评论信息插入表格comment
        sql2 = "insert into comment(bid,user,pubtime,content) values(%s,%s,%s,%s);"
        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "199659", "blog")
        db.set_charset('utf8mb4')
        cu = db.cursor()
        # 为博文信息创建表blogcontent
        sql = "drop table if exists comment;drop table if exists blogcontent;\
            CREATE TABLE blogcontent (\
                bid INT(4) AUTO_INCREMENT,\
                author VARCHAR(20),\
                title VARCHAR(50),\
                tag VARCHAR(50),\
                class VARCHAR(20) DEFAULT NULL,\
                pubtime DATETIME,\
                comment_total_num INT,\
                content LONGTEXT,\
                PRIMARY KEY (bid)\
            )  AUTO_INCREMENT=1;"
        cu.execute(sql)
        # 为每篇博文建立评论表comment
        sql = "\
            CREATE TABLE comment (\
                cid BIGINT AUTO_INCREMENT,\
                bid INT(4),\
                user VARCHAR(20),\
                pubtime DATETIME,\
                content LONGTEXT,\
                PRIMARY KEY (cid),\
                FOREIGN KEY (bid)\
                    REFERENCES blogcontent (bid)\
                    ON DELETE CASCADE ON UPDATE CASCADE\
            )AUTO_INCREMENT=1;"
        cu.execute(sql)

        for main_url in mainurl:
            self.n.append(0)
            catalogurl = self.getBlognameCatalog_url(main_url)
            if catalogurl == -1:
                continue
            if self.getBlogCount(catalogurl) == -1:
                continue
            # 将当前博主的博文爬取下来，j为第几篇
            # maxcount是篇数边界
            if maxcount > self.blogcount[self.index]:
                maxcount = self.blogcount[self.index]
            #for j in range(0, maxcount):
            for j in range(0, maxcount):
                temp = self.getBlogDetails(j, catalogurl, needimg)
                if temp == -1:
                    continue
                self.stories.append(temp)
                self.stories[sum(self.n)]['tag'] = ','.join(self.stories[sum(self.n)]['tag'])
                cu.execute(sql1, (self.stories[sum(self.n)]['author'], self.stories[sum(self.n)]['title'],
                                  self.stories[sum(self.n)]['tag'], self.stories[sum(self.n)]['class'],
                                  self.stories[sum(self.n)]['time'],
                                  self.stories[sum(self.n)]['comment_total_num'],
                                  self.stories[sum(self.n)]['content']))
                db.commit()
                if temp == 1:
                    continue
                for com in range(0, self.stories[sum(self.n)]['comment_total_num']):
                    tmp = self.stories[sum(self.n)]['comment'][com]
                    cu.execute(sql2, (sum(self.n) + 1, tmp['uname'], tmp['pubdate'], tmp['body']))
                    db.commit()
                self.n[self.index] = self.n[self.index] + 1
            self.index = self.index + 1
        # 关闭游标
        cu.close()
        # 关闭数据库连接
        db.close()
        return 0


# 爬取博客放入数据库
def spiderwork(mainurl, maxcount, needimg):
    spider = SINABLOG()
    spider.start(mainurl, maxcount, needimg)

spiderwork(['http://blog.sina.com.cn/u/3688920760'], 5,0)