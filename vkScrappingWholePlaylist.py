import time, os, sys, requests
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from browsermobproxy import Server
from urllib.parse import urlparse
from selenium.webdriver.common.action_chains import ActionChains

# Запрещенные символы в названии файла
FORBIDDEN_CHARS = '/\\\?%*:|"<>!.'

# Путь до chromedriver.exe
CHROME_PATH = None

# Путь до browsermob-proxy.bat
PROXY_SERVER_PATH = None

# Удаление запрещенных символов в именах файла
def checkFORBIDDEN_CHARS(s):
    for char in s:
        if char in FORBIDDEN_CHARS:
            s=s.replace(char, '')
    return s

# Скачивание файла по url
def download_file(url, track, path):
	track = checkFORBIDDEN_CHARS(track)
	local_filename = url.split('/')[-1]
	r = requests.get(url, stream=True)
	name = '{0}.mp3'.format(checkFORBIDDEN_CHARS(track))
	#path = "downloaded_tracks"
	if not os.path.exists(path):
		os.makedirs(path)
	new_filename = path + "/" + name
	#if not os.path.exists(new_filename):
	print('Downloading {0} ...'.format(track))
	with open(new_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk:
				f.write(chunk)
	print('{0} have been downloaded!'.format(track))			
	return name

# Авторизация по логину и паролю
def autorization(login, pswrd):
	username = driver.find_element_by_id('email')
	password = driver.find_element_by_id('pass')
	username.send_keys(login)
	password.send_keys(pswrd)
	driver.find_element_by_id("login_button").click()

# Проверка url на mp3 файл и возвращение url при его наличии
def checkUrl(url):
	end_idx = url.find(".mp3?extra=")
	if  end_idx == -1:
	    return None
	else:
	    return url[:end_idx+4]

# Находим в DOM название песни 
def parseSongName():
	return driver.find_element_by_class_name('audio_page_player_title_performer').text +\
		driver.find_element_by_class_name('audio_page_player_title_song').text

# Скачивание первых песен n из плейлиста
def downloadNfirstTracks(n):
	# Первый клик по кнопке "плэй", а последующие на кнопке "следующий трек"
	dowload_directory = "downloaded_tracks"
	try: 
		buttonPlay = driver.find_element_by_css_selector(".audio_pl_snippet_play.round_button")
		dowload_directory = driver.find_element_by_css_selector(".audio_pl_snippet__info_title.audio_pl__title").text
		dowload_directory = checkFORBIDDEN_CHARS(dowload_directory)
	except exceptions.NoSuchElementException as e: 
		buttonPlay = driver.find_element_by_css_selector(".audio_page_player_ctrl.audio_page_player_play._audio_page_player_play")
		
	buttonPlay.click()
	# Необходимо подождать загрузки песни, что бы реквест с url появился в прокси сервере
	time.sleep(1)
	list_of_song_names = [parseSongName()]

	for i in range(n-1):
		#button.click()
		buttonPlay.send_keys(Keys.ALT, "l")
		time.sleep(3)
		print(i, parseSongName())
		list_of_song_names.append(parseSongName())

	list_of_urls = []
	i = 0

	for ent in proxy.har['log']['entries']:
		url = checkUrl(ent['request']['url'])
		if url:
			download_file(url, list_of_song_names[i], dowload_directory) 
			list_of_urls.append(url)
			i = i + 1

def checkIfNone(String):
	if String is None:
		raise TypeError
	else:
		return	String	

# глобальная область видимости
while True:
	try:
		VK_PLAYST_URL              = checkIfNone(input('Type your vk playlist url       : '))
		LOGIN                      = checkIfNone(input('Type emal or phone number       : '))
		PASSWORD                   = checkIfNone(input('Type your password              : '))
		NUMBER_OF_SONG_TO_DOWNLOAD = int(checkIfNone(input('Type number of songs to donwload: ')))
	except ValueError:
		print("Not a number, plz try again!")
		continue
	except TypeError:
		print("Empty argument, plz try again!")
		continue
	else:
		break

try:
	server = Server(PROXY_SERVER_PATH)

	server.start()
	proxy = server.create_proxy()
	proxy.new_har()
	 
	chrome_options = webdriver.ChromeOptions()
	url = urlparse(proxy.proxy).path
	chrome_options.add_argument('--proxy-server=%s' % url)
	driver = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=chrome_options)

	driver.get(VK_PLAYST_URL)
	autorization(LOGIN, PASSWORD)
	# необходимо подождать загрузки страницы
	time.sleep(1)
	downloadNfirstTracks(NUMBER_OF_SONG_TO_DOWNLOAD)
except exceptions.WebDriverException as e:
	print("Invalid playlist url or incorrect login/password!")
	print(e)
finally:
	driver.quit()
	server.stop()