import scrapy
import os
from scrapy_splash import SplashRequest

if os.path.exists(os.path.join(os.getcwd(), 'data')):
	pass
else:
	os.mkdir('data')

LUA_SCRIPT = """
treat = require("treat")
function main(splash)
  local url = splash.args.url
  assert(splash:go(url))
  local links = splash:select_all('li.acalog-course a[onclick]')
  count = 0
  local results = {}
  for i, v in ipairs( links ) do
    count = count + 1
    v:click()
    splash:wait(1)
  end
  return splash:html()
  
end
"""

class CourseDescriptionSpider(scrapy.Spider):

	name = 'uscSpider'
	start_urls = ['http://catalogue.usc.edu/content.php?catoid=8&navoid=2161#programs']
	hostname = 'http://catalogue.usc.edu/'

	def parse(self, response):
		rows = response.css('td.block_content div ul')
		rows = rows[4]
		for row in rows.css('li'):
			link = row.css('a::attr("href")').extract()[0]
			degree_name = row.css('a::text').extract()[0]
			#print("-----", link, degree_name)
			link = self.hostname + link
			req = SplashRequest(url = link, callback = self.parseCoursePage, endpoint='execute', args= {'wait':1, 'lua_source': LUA_SCRIPT})
			req.meta['c_name'] = degree_name
			yield req

	def parseCoursePage(self, response):
		print(response.css('title'))
		f = open('data/'+response.meta['c_name'].replace('/',' ')+'.html','wb')
		f.write(response.body)
		f.close()
		
