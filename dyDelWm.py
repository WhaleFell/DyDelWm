#-*- coding=utf-8 -*-

'''
Author: whalefall
Date: 2021-01-22 15:12:09
LastEditTime: 2021-01-22 15:33:05
LastEditors: Please set LastEditors
Description: 抖音去水印批量下载
FilePath: \leaning-pythonc:\Users\Administrator\Desktop\DyDelWm\dyDelWm.py
'''


import requests
import re
from time import time,sleep
#视频存放目录 末尾加\\
video_path=r"C:\\Users\\27341\\Desktop\\dy_video\\"
#txt链接文档存放目录
txt_path=r"C:\\Users\\27341\\Desktop\\dy_url.txt"

#ua就是玄学 要安卓手机才行
header={
		"User-Agent":"Mozilla/5.0 (Linux; Android 8.0.0; EVA-AL10 Build/HUAWEIEVA-AL10;\
		 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89\
		  Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.0.0)",
	}

#获取视频id 传入任意链接都可
def getVideoId(urlShare):
	
	#先访问传入的链接 获取跳转后的链接(针对短链接)
	tUrl=requests.get(url=urlShare,headers=header).url
	#返回的链接应该是 https://www.iesdouyin.com/share/video/视频ID/ 通过正则寻找视频id
	pat=re.compile(r"/video/(\d+)/")
	result=pat.search(tUrl) #寻找的结果
	if result==None:
		print("id获取失败")
		id="0" #失败返回0
	else:
		id=pat.search(tUrl).group(1)
	return id

#返回视频无水印链接和描述和音频地址，传入视频id
def dyVideoUrl(id):

	b_time=time()
	#网页抓的视频接口
	url="https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+str(id)
	#视频接口json解析 取得无水印的视频链接 但是没跳转
	resp=requests.get(url,headers=header).json()
	# print(resp)
	title=resp["item_list"][0]["desc"]
	wm_url=resp["item_list"][0]["video"]["play_addr"]["url_list"][0].replace('playwm','play')
	mp3_url=resp["item_list"][0]["music"]["play_url"]["uri"]
	photo_url=resp["item_list"][0]["video"]["origin_cover"]["url_list"][0]

	#访问无水印链接，获取跳转后的链接要用安卓手机ua访问
	video_url=requests.get(url=wm_url,headers=header).url
	e_time=time()
	print("视频解析成功啦 耗时:",str(round(e_time-b_time,2))+"s")
	return title,video_url,mp3_url,photo_url

#写入视频加上描述
def writeVideo(url,name):
	b_time=time()
	video=requests.get(url,headers=header).content
	
	path=video_path+name+".mp4"
	
	with open(path,"wb") as f:
		f.write(video)
	e_time=time()
	print("视频",name,"下载成功啦 耗时:",str(round(e_time-b_time,2))+"s")

# id=getVideoId("https://v.douyin.com/JMU4Hat/")
# title,video_url,mp3_url,photo_url=dyVideoUrl(id)
# print("视频标题:",title,"\n链接:",video_url,"\n音频链接:",mp3_url,"\n封面图:",photo_url)
# writeVideo(video_url,title)


# 读取txt文件里边的链接 存放在列表urlL中	
with open(txt_path,"r",encoding="utf8") as u:
	urlL=u.readlines()
	# print(data)

i=0
for url in urlL:
	#匹配网址的正则表达式
	pat=re.compile(r"[a-zA-z]+://[^\s]*")
	url=pat.search(url)
	if url==None:
		# print("-----------------匹配失败------------------")
		pass
	else:
		i=i+1
		# print(url.)
		b_time=time()
		#获取id 判断id可用性 失败返回0
		id=getVideoId(url.group(0))
		if id=="0":
			print("id获取失败,下一个")
			print("--------------------------")
			pass
		else:
			print("视频id",id)
			sleep(8) #不能太快不然限制抓取
			title,video_url,mp3_url,photo_url=dyVideoUrl(id)
			writeVideo(video_url,title)
			e_time=time()
			print("下载总耗时:",str(round(e_time-b_time,2))+"s","下载第",i,"个")
			print("--------------------------")




