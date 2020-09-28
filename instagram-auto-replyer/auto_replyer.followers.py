import os, time, errno, pickle, stdiomask
import re
import getpass
import json
import csv
import yaml
import sys
import selenium
from selenium import webdriver as driver
from urllib.request import urlopen
from optparse import OptionParser
from selenium import webdriver


def login_instagram():
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)

        username_bar = driver.find_element_by_name("username")
        username_bar.send_keys(login_id)

        password_bar = driver.find_element_by_name("password")
        password_bar.send_keys(password)
        time.sleep(2)

        login_button = driver.find_element_by_class_name("L3NKy")
        login_button.click()
    except:
        pass

def userProfile():
  try:
    followingButtonXpath = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
    following_button = driver.find_element_by_xpath(followingButtonXpath).text
    print("Total Following: " + following_button)
  except:
    following_button = " "
    print("Total Following: " + following_button)
  try:
    postButtonXpath = '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span'
    post_button = driver.find_element_by_xpath(postButtonXpath).text
    print("Total posts: " + post_button)
  except:
    post_button = " "
    print("Total posts: " + post_button)
  try:
    fullNameXpath = '/html/body/div[1]/section/main/div/header/section/div[2]/h1'
    full_name = driver.find_element_by_xpath(fullNameXpath).text
    print("Full Name: " + full_name)
  except:
    full_name = " "
    print("Full Name: " + full_name)
  return full_name, post_button, following_button

def followerButton():
  try:
    follButtonXpath = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'
  except KeyError:
    ## xpath alternatif, sebagai antisipasi apabila Instagram mengganti API nya.
    follButtonXpath = '/html/body/div[1]/section/main/div/ul/li[2]/span'
    print("followerButton Xpath alt 2")
  except KeyError:
    follButtonXpath = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'
  except:
    sys.stderr.write("the Xpath of this element (followerButton) has changed \n")
    pass
  follower_button = driver.find_element_by_xpath(follButtonXpath)
  # printfoll = follower_button.get_attribute('title')
  printfoll = follower_button.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span')
  printfoll = follower_button.get_attribute('title').text
  print("yey1")
  print(printfoll)
  ## Split nilai dari jumlah followers apabila lebih dari 999, karena akan muncul koma bila nilainya ribuan, jutaan, dst.
  follValue = printfoll.split(',')
  print("yey2")
  # print(follValue[0])
  # print(follValue[1])
  ## Kumpulkan hasil dari nilai yang displit itu menjadi satu.
  try:
    follvalue0 = follValue[0]
    follvalue1 = follValue[1]
    follvalue2 = follValue[2]
    follvalue = str(follvalue0 + follvalue1 + follvalue2)
    print("Total followers: " + follvalue)
    follower_button.click()
    return follvalue
  except IndexError:
    follvalue0 = follValue[0]
    follvalue1 = follValue[1]
    follvalue = str(follvalue0 + follvalue1)
    print("Total followers: " + follvalue)
    follower_button.click()
    return follvalue
  except IndexError:
    follvalue0 = follValue[0]
    follvalue = str(follvalue0)
    follvalue = follvalue0
    print("Total followers: " + follvalue)
    follower_button.click()
    return follvalue
  except:
    sys.stderr.write("Followers index out of range \n")
  print("yey3")

## Mengambil username-username yang ada pada list follower akun yang usernamenya dicrawl
def follGet(indexOfFollower):
  follmax = 300
  count = 0
  while indexOfFollower <= follmax:
    str_indexOfFollower = str(indexOfFollower)
    try:
      follXpath = '/html/body/div[4]/div/div[2]/ul/div/li[' + str_indexOfFollower + ']/div/div[1]/div[2]/div[1]/a'
    except KeyError:
      ## xpath alternatif, sebagai antisipasi apabila Instagram mengganti API nya
      follXpath = '/html/body/div[4]/div/div[2]/ul/div/li[' + str_indexOfFollower + ']/div/div[2]/div[1]/div/div/a'
    except:
        pass
        sys.stderr.write("the Xpath of this element (follGet) has changed \n")
    finally:
      follower_name = driver.find_element_by_xpath(follXpath)
      follvalue = (follower_name.text)
      time.sleep(0.2)
      count += 1
      return follvalue
    if count > follmax:
      break
    else:
      pass

####################### THIS IS WHERE THE PROGRAM BEGINS #######################
driver = driver.Chrome("C:\\Windows\\webdriver\\chromedriver.exe")
counter = 1
infinity = 0x40000
maxCrawl = infinity
check = False
timeout = False
follGetError = False
timeoutValue = 10
timeoutCounter = 0
crawlCounter = 0
scroll = 0
folllist = []
follidlist = []
filename = "crawled_username.csv"

login_id = 'tyogotest1' #input('Put your IG account here! ')
password = 'username' #getpass.getpass('Put your IG password here! ')
usernames_target = login_id

login_instagram()
time.sleep(5)
try:
  user_target = usernames_target
except:
  sys.stderr.write("There is no username to crawl. The list is empty. \n")
  driver.close()
  sys.exit()

## Looping mengambil data username dari list followers pada profil instagram dari username yang ada pada list usernames_target
  ## Mengambil username yang ada pada usernames_target. Index yang menentukan username keberapa yang diambil diperoleh dari variabel "crawlCounter" yang dimulai dari angka 0 (pertama).
  ## Mengecek username yang ada di file "crawled_username.csv", apabila username sudah ada pada file tersebut, username tersebut tidak akan dicrawl lagi. Variabel "filename" harap dideklarasikan sebagai "crawled_username.csv" di awal program.
try:
  with open(filename, 'r') as csvread:
    reader = csv.reader(csvread)
except:
  with open('crawled_username.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile)
  with open(filename, 'r') as csvread:
    reader = csv.reader(csvread)
for row in reader:
  if user_target in row:
    print("This username is already crawled")
    crawlCounter += 1
    check = True
  else:
    check = False
  if check == True:
    continue
  elif check == False:
    pass
  
  ## Masuk ke url dari profil instagram dari username yang akan dicrawl, untuk mengumpulkan data user.
driver.get('https://www.instagram.com/' + user_target + '/')
  ## Variabel "crawlCounter" ditambahkan dengan angka 1 agar index yang diberikan untuk mengambil "usernames_target" berikutnya tepat.
crawlCounter += 1
  ## Tambahkan waktu delay lagi selama 5 detik untuk mensimulasikan interaksi orang pada saat membuka profil instagram.
time.sleep(5)

  ## Panggil fungsi followerButton() untuk mendapat nilai dari jumlah follower akun instagram yang dicrawl dan menekan tombol "followers" agar list follower keluar dan bisa diakses.
try:
  follower_button=followerButton()
except:
  sys.stderr.write("This account is private or doesn't exist \n")
  driver.close()
    # sys.exit()

  ## Jalankan userProfile() untuk mendapatkan nama lengkap, jumlah post, dan jumlah following dari username. 
full_name, post_button, following_button = userProfile()
  ## Convert nilai dari jumlah folower yang ada pada variabel follower_button menjadi integer agar bisa dimasukkan menjadi argument yang menandakan jumlah total username pada saat mengambil username yang ada pada list follower.
follower_value = int(follower_button)
  
  ## Apabila username tersebut tidak memiliki follower, break untuk lanjut ke username berikutnya.
if follower_value == 0:
  sys.stderr.write("This username has no follower \n")
    
else:
  pass
  ## Tambahkan waktu delay selama 3 detik untuk mensimulasikan interaksi orang pada saat membuka list follower.
time.sleep(3)

  ## Scroll list follower hingga kurang lebih sesuai dengan limit maksimal username yang dicrawl yang ada pada fungsi follGet() (untuk 300 followers kira-kita 100x maximal scroll)
fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
for scroll in range(0,100):
  driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
  time.sleep(0.2)
print("scrolling finish")
time.sleep(1)
  
  ## Loop crawling username dari list follower dengan parameter yang berupa urutan dari pertama hingga terakhir (argument follower_value)
for i in range(1, follower_value):
    ## Jalankan follGet() dan masukkan "i" sebagai parameter dari fungsi tersebut. "i" akan berupa angka yang akan diproses oleh follGet() menjadi index untuk menentukan xpath dari username yang akan diambil.
  try:
    USERstr = str(follGet(i))
    follGetError = False
    ## If there is an error when collecting usernames from followers list, set follGetError to True and break
  except:
    sys.stderr.write("error occured \n")
    follGetError = True
    break
  print(str(i)+USERstr)
  if USERstr == "None":
    break
  else:
    pass
    
  folllist.append(USERstr)

  if follGetError == False:
    print(folllist)
    folllistRow1 = folllist[0]
    folllist = folllist[1:follower_value]
  else:
    pass
  
  ## Append username yang sudah di crawled ke database "crawled_username.csv"
  with open('crawled_username.csv', 'a+', newline='') as csvwrite:
    wr = csv.writer(csvwrite)
    wr.writerow([user_target])

  ## Buat file csv baru yang nama filenya berdasarkan username yang dicrawl. Selain itu, sertai pula di dalamnya data-data lain yang tadi telah dikumpulkan.
  with open('followers(' + user_target + ').csv', 'w', newline='') as csvfile:
      wr = csv.writer(csvfile)
      wr.writerow(["Root"] + ["Username"] + ["Full Name"] + ["Total Posts"] + ["Total Followers"] + ["Total Following"] + ["Followers"])
      wr.writerow([login_id] + [user_target] + [full_name] + [post_button] + [follower_button] + [following_button] + [folllistRow1])
      for follower in folllist:
        wr.writerow([""]+[""]+[""]+[""]+[""]+[""]+[follower])
  
  ## Buka window baru untuk menghindari error saat crawling berikutnya
  driver.execute_script("window.open('');")
  ## Tutup window yang terbuka saat sesi crawl ini
  try:
    driver.switch_to.window(driver.window_handles[1])
    driver.execute_script("window.close('');")
  except:
    pass
  try:
    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script("window.close('');")
  except:
    pass
  
  ## Bersihkan folllist dengan cara mereset listnya menjadi kosong
  folllist=[]

## Bersihkan usernames_target, untuk memastikan list tersebut kosong pada saat akan menjalankan program ini lagi. Lalu, tutup ChromeDriver nya.
usernames_target=[]
time.sleep(3)
driver.close()