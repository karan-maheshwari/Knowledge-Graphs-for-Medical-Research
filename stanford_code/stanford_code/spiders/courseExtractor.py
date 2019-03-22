from bs4 import BeautifulSoup
import requests

url = "http://med.stanford.edu/education/masters-programs.html"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')
main_div = soup.find("div", {"class":"border-and-shadow"})
list_of_courses = main_div.findAll("h2", {"class":"black"})

f = open("courses.txt","w+")

for i in list_of_courses:
	f.write(i.text.strip()+"\n")

f.close()