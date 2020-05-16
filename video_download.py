# encoding: utf-8

import requests
import time
import re
import os
import _thread
from tkinter import *

def downloadFile(name,url):
	headers={'Proxy-Connection':'keep-alive'}
	r=requests.get(url, stream=True,headers=headers)
	length=float(r.headers['content-length'])
	f=open(name,'wb')
	count=0
	count_tmp=0
	time1=time.time()
	# _thread.start_new_thread(update,())
	for chunk in r.iter_content(chunk_size=512):
		if chunk:
			f.write(chunk)
			count+=len(chunk)
			if time.time()-time1>2:
				p=count/length*100
				speed=(count-count_tmp)/1024/1024/2
				count_tmp=count
				# print(name+': '+formatFloat(p)+'%'+' Speed: '+formatFloat(speed)+'M/S')
				status.delete(0.0,END)
				status.insert(0.0,name+': '+formatFloat(p)+'%'+' Speed: '+formatFloat(speed)+'M/S')
				status.grid(row=0,rowspan=3,column=3)
				top.update()

				time1=time.time()
	# 		top.update()
	# 	top.update()
	# top.update()

	f.close()
	status.delete(0.0,END)
	status.insert(0.0,'Finished!')

def formatFloat(num):
	return '{:.2f}'.format(num)

def get_download_list(raw_list): #change .js file into download list
	rule=re.compile('https://gss3\\.baidu\\.com/.{25,30}/tieba-smallvideo/.{25,35}\\.mp4')
	ret=rule.findall(raw_list)
	print(ret)
	return ret

def MAIN(url,anime_name):
	# name=input('write the name of the download list : ')
	# anime_name=input('write the name of the anime : ')
	download_list=open(url,mode='r')
	tp=download_list.read()
	download_list.close()
	# if(input('.js file?(1/0) ')=='1'):
	# if isjs==TRUE:
	download_list=get_download_list(tp)
	# else:
	# 	download_list=tp.split()
	if os.path.isdir(anime_name)==FALSE:
		os.makedirs(anime_name)
	for i in range(len(download_list)):
		downloadFile(anime_name+'/'+str(i+1)+'.mp4',download_list[i])
	return 0

def tomain():
	get_js_file(name_entry.get())
	MAIN('video_list.js',anime_name_entry.get())

def get_js_file(url):
	print('getting url : ',url)
	tp=str(url)
	html_file=requests.get(str(tp)).text
	rule=re.compile('/playdata/.{1,3}/.{2,4}\\.js.{6,11}"></script><script>')
	ret=rule.findall(html_file)[0]
	ret='http://www.imomoe.in'+ret[0:len(ret)-19]
	print('getting url : ',ret)
	js_file=requests.get(ret).text
	with open('video_list.js',mode='w',encoding='utf-8') as f:
		f.write(js_file)

if __name__=='__main__':
	global top
	top=Tk()
	top.colormapwindows()

	try :
		top.iconbitmap('video.ico')
	except TclError:
		print('Icon File not Found!')
	else:
		print('Loading Icon File')
	
	# top.geometry('500x300')
	top.title('video downloader v0.2  -by Eddy')
	
	global name_label
	name_label=Label(top,text="Anime URL")
	
	global name_entry
	name_entry=Entry(top)

	global anime_name_label
	anime_name_label=Label(top,text="Anime Name")

	global anime_name_entry
	anime_name_entry=Entry(top)
	
	start_button=Button(top,width=14,text="Start",command=tomain)
	end_button=Button(top,width=14,text="Exit",command=top.quit)
	help_label=Label(top,text='A tool to download videos on imomoe.in!')

	global status
	status=Text(top,height=10,width=32)
	status.insert(0.0,'Status:')

	name_label.grid(row=0,column=1)
	name_entry.grid(row=0,column=2)
	anime_name_label.grid(row=1,column=1)
	anime_name_entry.grid(row=1,column=2)
	start_button.grid(row=3,column=1)
	end_button.grid(row=3,column=2)
	status.grid(row=0,rowspan=3,column=3)
	help_label.grid(row=2,column=1,columnspan=2)
	top.mainloop()
