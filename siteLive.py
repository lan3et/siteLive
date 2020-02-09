import requests
import threading
import hashlib
from retrying import retry
from readability import Document
import aiohttp
import asyncio
requests.packages.urllib3.disable_warnings()


live_site = []
almost_live_site = []
nearly_dead_site = []
dead_site = []
not_web_site = []
keywords_404 = ['404.css', '404.js', '404', 'not found']


@retry(stop_max_attempt_number=10)
async def check_state(url):
	headers = {'Accept': '*/*','Accept-Language': 'en-US,en;q=0.8','Cache-Control': 'max-age=0','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36','Connection': 'keep-alive','Referer': url}
	if ':' in url:
		print(url)
		if url.split(':')[1] == '80' and url.split(':')[1] == '443':
			url = url.replace(':443','').replace(':80','')
			print(url)
	try:
		async with aiohttp.ClientSession() as session:
			if 'https' in url:
				async with session.get(url + '/dx8hjdgoperjf', verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
					print(res.status)
			else:
				async with session.get('http://' + url + '/dx8hjdgoperjf', verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
					print(response.status)
			if response.status == 400:
				if 'https' not in url:
					if 'http' not in url:
						url = 'https://'+url
						async with session.get(url + '/dx8hjdgoperjf', verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
							print(response.status)
						if response.status != 400:
							check_state(url)
						else:
							dead_site.append(url)#+'---------------'+Document(response.text()()).title())
					else:
						url.replace('http','https')
						async with session.get(url + '/dx8hjdgoperjf', verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
							print(response.status)
						if response.status != 400:
							check_state(url)
						else:
							dead_site.append(url)#+'---------------'+Document(response.text()()).title())
				elif 'https' in url:
					url.replace('https://','')
					async with session.get('http://' + url + '/dx8hjdgoperjf', verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
						print(response.status)
					if requests.status != 400:
						check_state(url)
					else:
						dead_site.append(url)
			elif response.status == 200:
				for key in keywords_404:
					if key in response.text():
						live_site.append(url)
					else:
						CL = response.headers['Content-Length']
						m = hashlib.md5()
						text = response.text().encode(encoding='utf-8')
						m.update(text)
						hash_text = m.hexdigest()
						if 'https' in url:
							async with session.get(url + '/ljgfdsnvcxjkfds', verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
								print(response.status)
						else:
							async with session.get('http://' + url + '/ljgfdsnvcxjkfds', verify_ssl=False, allow_redirects=False,timeout=4, headers=headers) as response:
								print(response.status)
							if response.status == 200:
								CL2 = response.headers['Content-Length']
								i = hashlib.md5()
								text = response.text().encode(encoding='utf-8')
								i.update(text)
								hash_text2 = i.hexdigest()
								if hash_text == hash_text2 or abs(int(CL) - int(CL2)) < 5:
									nearly_dead_site.append(url)#+'---------------'+Document(response.text()).title())
								else:
									almost_live_site.append(url)#+'---------------'+Document(response.text()).title())
							elif response.status == 301 or response.status == 302:
								live_site.append(url)#+'---------------'+Document(response.text()).title)
							elif response.status in [403, 404, 415]:
								almost_live_site.append(url)#+'---------------'+Document(response.text()).title())
							elif response.status == 500:
								nearly_dead_site.append(url)#+'---------------'+Document(response.text()).title())
							elif response.status in [501, 502, 503, 504]:
								if 'https' in url:
									async with session.get(url, verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
										print(response.status)
								else:
									async with session.get('http://' + url, verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
										print(response.status)
								if response.status == 200:
									CL3 = response.headers['Content-Length']
									n = hashlib.md5()
									text = response.text().encode(encoding='utf-8')
									n.update(text)
									hash_text3 = n.hexdigest()
									if hash_text == hash_text3 or abs(CL - CL3) < 5:
										nearly_dead_site.append(url)#+'---------------'+Document(response.text()).title())
									else:
										almost_live_site.append(url)#+'---------------'+Document(response.text()).title())
								elif response.status == 301 or response.status == 302:
									live_site.append(url)#+'---------------'+Document(response.text()).title())
								elif response.status in [403, 404, 415]:
									almost_live_site.append(url)#+'---------------'+Document(response.text()).title())
								elif response.status == 500:
									nearly_dead_site.append(url)#+'---------------'+Document(response.text()).title())
								elif response.status in [501, 502, 503, 504]:
									dead_site.append(url)#+'---------------'+Document(response.text()).title())
								else:
									not_web_site.append(url)#+'---------------'+Document(response.text()).title())
			elif response.status == 404:
				if 'https' in url:
					async with session.get(url, verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
						print(response.status)
				else:
					async with session.get('http://' + url, verify_ssl=False, allow_redirects=False, timeout=4, headers=headers) as response:
						print(response.status)
				if response.status ==200:
					live_site.append(url)#+'---------------'+Document(response.text()).title())
				if response.status in [301,302]:
					async with session.get(response.headers['Location'], verify_ssl=False, allow_redirects=False, timeout=4, headers=headers) as response2:
						print(response2.status)
					if response2.status == 200:
						live_site.append(url + '---------------' + Document(response.text()).title())
					if response2.status in [301,302]:
						async with session.get(response2.headers['Location'], verify_ssl=False, allow_redirects=False, timeout=4, headers=headers) as response3:
							print(response3.status)
						live_site.append(url)#+'---------------'+Document(response3.text()).title())
				elif response.status in [403, 404, 415]:
					almost_live_site.append(url)#+'---------------'+Document(response.text()).title())
				elif response.status == 500:
					nearly_dead_site.append(url)#+'---------------'+Document(response.text()).title())
				elif response.status in [501, 502, 503, 504]:
					if 'https' in url:
						async with session.get(url, verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
							print(response.status)
					else:
						async with session.get('http://' + url, verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response:
							print(response.status)
					if response.status in [200, 301, 302]:
						live_site.append(url)
					elif response.status in [403, 404, 415]:
						almost_live_site.append(url)#+'---------------'+Document(response.text()).title())
					elif response.status == 500:
						nearly_dead_site.append(url)#+'---------------'+Document(response.text()).title())
					elif response.status in [501, 502, 503, 504]:
						dead_site.append(url)#+'---------------'+Document(response.text()).title())
					else:
						not_web_site.append(url)#+'---------------'+Document(response.text()).title())
				else:
					not_web_site.append(url)#+'---------------'+Document(response.text()).title())
			elif response.status == 401 or response.status == 415:
				almost_live_site.append(url)#+'---------------'+Document(response.text()).title())
			elif response.status == 301 or response.status == 302:
					async with session.get(response.headers['Location'],verify_ssl=False, allow_redirects=False, timeout=4,headers=headers) as response2:
						print(response2.status)
					if response2.status == 200:
						live_site.append(url)#+'---------------'+Document(response2.text()).title())
					elif response2.status in [301,302]:
						nearly_dead_site.append(url)#+'---------------'+Document(response2.text()).title())
					elif 'https' in response.headers['Location']:
						check_state(response.headers['Location'])
					#else:
			elif response.status == 304:
				live_site.append(url)#+'---------------'+Document(response.text()).title())
			elif response.status == 403 or response.status == 500:
				nearly_dead_site.append(url)#+'---------------'+Document(response.text()).title())
			elif response.status in [501, 502, 503, 504]:
				dead_site.append(url)#+'---------------'+Document(response.text()).title())
			else:
				not_web_site.append(url)#+'---------------'+Document(response.text()).title())
	except Exception as e:
		print('requset to ' + url + ' is worng')
		not_web_site.append(url)#+'---------------'+Document(response.text()).title())


def read_file(filename):
	with open(filename, 'r') as f:
		return f.readlines()


# def go_threading(nums, urls):
# threads = []
# for i in nums:
# 	if int(urls[i].split(':')[1]) != 80 and int(urls[i].split(':')[1]) != 443:
# 		print(urls[i].split(':')[1])
# 		print(urls[i])
# 		t = threading.Thread(target=check_state, args=(urls[i].replace('\n', '').replace('\r', ''),))
# 		threads.append(t)
# 	else:
# 		t = threading.Thread(target=check_state, args=(urls[i].replace('\n', '').replace('\r', '').split(':')[0],))
# 		threads.append(t)
# 		print('**********'+urls[i].replace('\n', '').replace('\r', '').split(':')[0])
# print('\033[1;32m[STRAT..]\n')
# for i in nums:
# 	threads[i].start()
# for i in nums:
# 	threads[i].join()
# print('\n\033[1;32m[DONE..]')


def write_file(site_state, state_name):
	with open(state_name + '.txt', 'a',encoding="utf-8") as f:
		for i in site_state:
			f.write(i + '\n')

def clean_data():
	clean = []
	dirty = []
	with open('not_web_site.txt','r',encoding="utf-8") as f:
		datas = f.readlines()
		for data in datas:
			if '404' not in data and '400' not in data and 'Error report' not in data:
				clean.append(data)
			else:
				dirty.append(data)
	f.close()
	with open('live_site.txt','a',encoding="utf-8") as s:
		for data in clean:
			s.write(data)
	s.close()
	with open('cleaned_not_web_site.txt', 'a', encoding="utf-8") as m:
		for data in dirty:
			m.write(data)
	m.close()

# async def run(nums):
#     semaphore = asyncio.Semaphore(500) # 限制并发量为500
#     to_get = [hello(url.format(),semaphore) for _ in range(1000)] #总共1000任务
#     await asyncio.wait(to_get)


def call_back(content):
	print(content)

if __name__ == '__main__':
	urls = list(set(read_file(input('Please input your filename:'))))
	nums = range(len(urls))
	print(nums)
	print(urls)
	#go_threading(nums, urls)
	loop = asyncio.get_event_loop()
	for i in nums:
		if int(urls[i].split(':')[1]) != 80 and int(urls[i].split(':')[1]) != 443:
			c = check_state(urls[i].replace('\n', '').replace('\r', ''))
			task = asyncio.ensure_future(c)
			task.add_done_callback(call_back)
			loop.run_until_complete(task)	
		else:
			c = check_state(urls[i].replace('\n', '').replace('\r', '').split(':')[0])
			task = asyncio.ensure_future(c)
			task.add_done_callback(call_back)
			loop.run_until_complete(task)
	#semaphore = asyncio.Semaphore(500)
	write_file(live_site, 'live_site')
	write_file(almost_live_site, 'almost_live_site')
	write_file(nearly_dead_site, 'nearly_dead_site')
	write_file(dead_site, 'dead_site')
	write_file(not_web_site, 'not_web_site')
	clean_data()
