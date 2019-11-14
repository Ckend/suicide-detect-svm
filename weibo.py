import json
import requests
import time
import os
from lxml import etree

"""
爬取微博评论
"""

headers = {
    'Referer': 'https://weibo.com/1648007681/yark9qWbM?type=comment',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'Cookie': 'SINAGLOBAL=9892234271124.58.1530001641635; un=83493903@qq.com; wvr=6; Ugrow-G0=cf25a00b541269674d0feadd72dce35f; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWFGHQnjQwxo1UeQZrojLpG5JpX5KMhUgL.Fo2c1he0e0e7ShB2dJLoI0qLxKqLBoqL1hnLxK-LBKBLBo2LxKML1-2L1hBLxKqLBKnLB.BLxKqLBo-LBoMLxK.L1--L1Knt; ALF=1605249851; SSOLoginState=1573713852; SCF=Aq26dvknsLHBaB6Ar2gzGVXL075H95RYI5t01wG3s02B4JExgHRF9voIs-K1sYtLT9_1Rnc89DX1IrIZ4WpxnSI.; SUB=_2A25wyIfsDeRhGedI41ES8y3MzziIHXVTv_4krDV8PUNbmtBeLUiskW9NVrhEHgtmpQOmEbyTeZvEH40Nfhy92RW8; SUHB=0cSWtwgWyuPs5i; YF-V5-G0=125128c5d7f9f51f96971f11468b5a3f; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=7326068956788.363.1573713866589; ULV=1573713866648:88:8:1:7326068956788.363.1573713866589:1573230743326; wb_view_log_1683333044=2560*10801; YF-Page-G0=753ea17f0c76317e0e3d9670fa168584|1573718511|1573718470; webim_unReadCount=%7B%22time%22%3A1573718517272%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D',
}


# 下载图片
def download_pic(url, nick_name):
    pic_file_path = os.path.join(os.path.abspath(''), 'pic')
    # 当前路径+pic
    if not url:
        return
    if not os.path.exists(pic_file_path):
        os.mkdir(pic_file_path)
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(pic_file_path + f'/{nick_name}.jpg', 'wb') as f:
            f.write(resp.content)
    time.sleep(2)

# 写入留言内容
def write_comment(comment, pic_url, nick_name):
    f = open('comment.txt', 'a', encoding='utf-8')
    for index, i in enumerate(comment):
        if ':' not in i and '回复' not in i and i != '':
            # 去除评论的评论
            w_comment = "".join(i.split('：')[1:])
            print(w_comment)
            w_comment = i.strip().replace('\n', '')
            # 写入评论
            f.write(w_comment.replace('等人', '').replace('图片评论', '')+'\n')
            # 获得头像
            download_pic(pic_url[index], nick_name[index])

if __name__ == '__main__':

    params = {
        'ajwvr': 6,
        'id': '3424883176420210',
        'page': 1,
        '_rnd': int(round(time.time() * 1000))
    }
    URL = 'https://weibo.com/aj/v6/comment/big'

    for num in range(1,25,1):
        print(f'====== 正在读取第 {num} 页 ========')
        params['page'] = num
        params['_rnd'] = int(round(time.time() * 1000))
        print(params['_rnd'])
        resp = requests.get(URL, params=params, headers=headers)
        resp = json.loads(resp.text)
        if resp['code'] == '100000':
            html = resp['data']['html']
            html = etree.HTML(html)
            data = html.xpath('//div[@node-type="comment_list"]')
            for i in data:
                # 评论人昵称
                nick_name = i.xpath('.//div[@class="WB_text"]/a[1]/text()')
                # 评论内容
                text = i.xpath('.//div[@class="WB_text"]')
                text = [i.xpath('string(.)') for i in text]
                # 头像地址
                pic_url = i.xpath('.//div[@class="WB_face W_fl"]/a/img/@src')

                print(len(nick_name),len(text),len(pic_url))
                # 写入文件并下载头像
                write_comment([i.strip() for i in text], pic_url, nick_name)
        time.sleep(5)