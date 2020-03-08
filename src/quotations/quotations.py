# encoding:utf-8
'''
Created on 2020年3月8日

@author: Administrator
'''
import datetime
from playsound import playsound
import requests
import os

# 上一个音频文件
last_audio_file = ''
# 自动删除标志
autodeleteflag = True


#
# 根据类型来获取语录
#
def get(type_):

    # 地址
    url = 'https://cdn.ipayy.net/says/api.php'
    # 参数
    params = {"type": type_}
    # 添加请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
    }

    # 获取结果
    res = requests.get(url=url, params=params, headers=headers).text
    # 返回结果
    return res


#
# 获取语录语音文件
#
def get_audio_file(quotation):
    # 百度翻译语音API
    url = 'https://fanyi.baidu.com/gettts?lan=zh&text=' + quotation + '&spd=4&source=web'
    # 下载语音
    result = requests.get(url)
    # 时间戳为文件名
    time_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = 'E:\\temp\\yulu\\' + time_now + '.mp3'

    # wb：以二进制方式写入文件
    with open(filename, 'wb') as f:
        f.write(result.content)

    global last_audio_file
    # 删除上一个音频文件
    if last_audio_file != '' and os.path.exists(last_audio_file) and autodeleteflag:
        os.remove(last_audio_file)

    # 保存为上一个音频文件
    last_audio_file = filename
    # 返回语音文件
    return filename


#
# 朗读语录
#
def read(filename):
    try:
        # 播放音频文件
        playsound(filename)
    except:
        pass


#
# 入口
#
if __name__ == '__main__':
    pass
