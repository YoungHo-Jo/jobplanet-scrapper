import requests
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import csv

secret_json_file = open('./secret.json', 'r')
secret_json = json.loads(secret_json_file.read())
secret_json_file.close()

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

driver.get('https://www.jobplanet.co.kr/users/sign_in')

driver.find_element_by_name('user[email]').send_keys(secret_json['id'])
driver.find_element_by_name('user[password]').send_keys(secret_json['pwd'])

driver.find_element_by_class_name('btn_sign_up').click()

print('Input the jobplanet site URL you want to parse(only interview pages...)');
print("(includes ? parameters)")
target = input()
driver.get(target)

f = open('data.csv', 'w+', encoding='utf-8', newline='')
wr = csv.writer(f, delimiter=',')
wr.writerow([
  'category',
  'graduation',
  'register date',
  'interview date',
  'interview title',
  'interview question',
  'interview answer',
  'interview result'
])

for page_number in range(1, 100):
  driver.get('{}&page={}'.format(target, page_number))
  driver.implicitly_wait(3)
  html = driver.page_source
  soup = bs(html, 'html.parser')
  section_group = soup.select('#viewInterviewsList > div > div')
  if len(section_group[0].select('article > p')) != 0: 
    print('secion  group not exists at page_number={}'.format(page_number))
    break

  for i in range(1, 20):
    section = section_group[0].select('section:nth-child({})'.format(i))
    if len(section) == 0:
      continue
    section = section[0]
    title = section.select('div > div.content_top_ty2 > span.txt1')
    interview_date = section.select('div > div.ctbody_col2 > dl > dd.txt1')
    content_title = section.select('div > div.ctbody_col2 > div > div.us_label_wrap')
    interview_question = section.select('div > div.ctbody_col2 > div > dl > dd:nth-child(2)')
    interview_answer = section.select('div > div.ctbody_col2 > div > dl > dd:nth-child(4)')
    interview_result = section.select('div > div.ctbody_col2 > div > div.now_box > div > dl > dd:nth-child(2)')
  
    def get_text(tag):
      return tag[0].text.strip() if len(tag) != 0 else ''

    category = ''
    graduation = ''
    register_date = ''
    title_text = get_text(title)
    if title_text != '':
      tokens = title_text.split('\n')
      category = tokens[0]
      graduation = tokens[2].strip()
      register_date = tokens[5].strip()
      

    d = [
      category,
      graduation,
      register_date,
      get_text(interview_date),
      get_text(content_title),
      get_text(interview_question),
      get_text(interview_answer),
      get_text(interview_result)
    ]
    wr.writerow(d)


f.close()
driver.close()
