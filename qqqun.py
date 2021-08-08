# 导入需要的包
# 爬取qq群的成员信息
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
import csv


# 开始登陆
def login_spider():

    url = 'https://qun.qq.com/'
    # 构建谷歌驱动器
    browser = webdriver.Chrome()
    # 请求url
    browser.get(url)
    # 模拟登陆，首先找到登陆的id，并点击
    browser.find_element_by_css_selector('#headerInfo p a').click()
    # 点击之后会弹出一个登陆框，这时候我们用显示等待来等待这个登陆框加载出来
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#loginWin iframe')
        )
    )
    print('登陆框已加载')
    # 登陆框加载之后，我们发现整个登陆框其实就是另一个网网页
    # 如果在原网页操作这个登陆框的话，是不能操作的
    # 所以我们只需要提取iframe标签的src属性，然后再去访问这个url即可实现
    # 自动登陆
    # 找到iframe标签并获取是如此熟悉
    iframe_url = browser.find_element_by_css_selector('#loginWin iframe').get_attribute('src')
    # 再访问这个url
    browser.get(iframe_url)
    # 找到快捷登陆的头像并点击
    # 首先用显示等待这个头像已经加载完成
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (By.ID, 'qlogin_list')
        )
    )
    browser.find_element_by_css_selector('#qlogin_list a').click()
    print('登陆成功')

    return browser


# 切换句柄操作
def switch_spider(browser):
    # 登陆成功之后，我们就找到群管理的标签并点击,首先等待这个元素加载完成
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, './/ul[@id="headerNav"]/li[4]')
        )
    )
    browser.find_element_by_xpath('.//ul[@id="headerNav"]/li[4]').click()
    # 点击之后，我们找到成员管理标签并点击
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'color-tit')
        )
    )
    browser.find_element_by_class_name('color-tit').click()
    # 打印全部窗口句柄
    # print(browser.window_handles)
    # 打印当前窗口句柄
    # print(browser.current_window_handle)
    # 注意这里点击成员管理之后会自动跳转到一个新窗口打开这个页面
    # 所以我们需要将窗口句柄切换到这个新窗口
    browser.switch_to.window(browser.window_handles[1])
    # 解释一下browser.switch_to.window是获取当前一共有几个窗口
    # 这里是2个
    # browser.switch_to.window这个是指定当前游标切换到哪个窗口
    # 其实也可以这么写
    # all_window = browser.switch_to.window返回的是一个列表
    # browser.switch_to.window(all_window[1])
    # 效果是一样的

    return browser


# 开始采集数据
def start_spider(browser):
    # 声明一个列表存储字典
    data_list = []
    # 切换句柄之后，我们显示等待窗口出来
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'my-all-group')
        )
    )

    # 筛选出我加入的群标签
    lis = browser.find_elements_by_xpath('.//div[@class="my-all-group"]/ul[2]/li')
    # 遍历
    num = 0
    while True:
        try:
            # 按顺序选择群并获取信息
            # 先点击该群获取成员信息
            lis[num].click()
            # 显示等待信息加载完成
            WebDriverWait(browser, 1000).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'list')
                )
            )
            # 获取该群当前有多少人，后面翻页需要
            groupMemberNum = eval(browser.find_element_by_id('groupMemberNum').text)
            # 每一次翻页都会刷新21条信息，所以写个循环
            # 这里加1是因为假如一个群有36人，那么count=1，如果循环的话就不会翻页了
            # 也就是只能抓到一页的数据，大家可以自己想想其中的流程就知道了
            count = groupMemberNum // 21 + 1
            # 这里我只爬取每个群的一部分，如果想爬取全部成员信息
            # 请注释下面的if语句
            if count > 5:
                count = 5
            # 每次循环都进行翻页
            while count:
                count -= 1

                browser.execute_script('document.documentElement.scrollTop=100000')
                time.sleep(2)
            time.sleep(3)
            # 开始获取成员信息
            trs = browser.find_elements_by_class_name('mb')
            if trs:
                # 遍历
                for tr in trs:
                    tds = tr.find_elements_by_tag_name('td')[2:]
                    if len(tds) == 8:
                        # qq网名
                        qq_name = tds[0].text
                        # 群名称
                        group_name = tds[1].text
                        # qq号
                        qq_number = tds[2].text
                        # 性别
                        gender = tds[3].text
                        # qq年龄
                        qq_year = tds[4].text
                        # 入群时间
                        join_time = tds[5].text
                        # 等级（积分）
                        level = None
                        # 最后发言时间
                        end_time = tds[6].text

                        # 声明一个字典存储数据
                        data_dict = {}
                        data_dict['qq_name'] = qq_name
                        data_dict['group_name'] = group_name
                        data_dict['qq_number'] = qq_number
                        data_dict['gender'] = gender
                        data_dict['qq_year'] = qq_year
                        data_dict['join_time'] = join_time
                        data_dict['level'] = level
                        data_dict['end_time'] = end_time

                        print(data_dict)
                    elif len(tds) == 9:
                        # qq网名
                        qq_name = tds[0].text
                        # 群名称
                        group_name = tds[1].text
                        # qq号
                        qq_number = tds[2].text
                        # 性别
                        gender = tds[3].text
                        # qq年龄
                        qq_year = tds[4].text
                        # 入群时间
                        join_time = tds[5].text
                        # 等级（积分）
                        level = tds[6].text
                        # 最后发言时间
                        end_time = tds[7].text

                        # 声明一个字典存储数据
                        data_dict = {}
                        data_dict['qq_name'] = qq_name
                        data_dict['group_name'] = group_name
                        data_dict['qq_number'] = qq_number
                        data_dict['gender'] = gender
                        data_dict['qq_year'] = qq_year
                        data_dict['join_time'] = join_time
                        data_dict['level'] = level
                        data_dict['end_time'] = end_time
                        data_list.append(data_dict)

                        print(data_dict)

            browser.find_element_by_id('changeGroup').click()
            time.sleep(3)
            WebDriverWait(browser, 1000).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'ui-dialog')
                )
            )
            lis = browser.find_elements_by_xpath('.//div[@class="my-all-group"]/ul[2]/li')
            num += 1
        except Exception as e:
            continue

    return data_list


def main():

    browser = login_spider()
    browser = switch_spider(browser)
    data_list = start_spider(browser)

    # 将数据写入json文件
    with open('data_json.json', 'a+', encoding='utf-8') as f:
        json.dump(data_list, f)
    print('json文件写入完成')
	# 这里的编码格式不要写错了，不然会出现乱码，因为群里面的大神名字贼骚
    with open('data_csv.csv', 'w', encoding='utf-8-sig', newline='') as f:
        # 表头
        title = data_list[0].keys()
        # 声明writer
        writer = csv.DictWriter(f, title)
        # 写入表头
        writer.writeheader()
        # 批量写入数据
        writer.writerows(data_list)
    print('csv文件写入完成')


if __name__ == '__main__':

    main()