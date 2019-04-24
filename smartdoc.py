import sys
import re

#file_code_addr = "C:\\Users\\Administrator\\Desktop\\file\\smartdoc\\code.py"
#file_srs_addr = "C:\\Users\\Administrator\\Desktop\\file\\smartdoc\\srs.txt"

file_code_addr = sys.argv[1]
file_srs_addr = sys.argv[2]
gen_code_html = "code.html"
gen_srs_html = "srs.html"

f_code_txt = open(file_code_addr,'r')
f_srs_txt = open(file_srs_addr,'r')
f_code_html = open(gen_code_html,'w')
f_srs_html = open(gen_srs_html,'w')

#code.py
def write_code_content(line):
	if line.find("#{see rq")!=-1:
		id_name = re.findall(r"rq\d",line)
		link = gen_srs_html+"#"+id_name[0]
		line = "<a href='"+link+"' id='"+id_name[0]+"'>"+line+"</a>"
	return line

#srs.txt
def write_srs_content(line):
	if line.find("[id=rq")!=-1:
		id_name = re.findall(r"rq\d",line)
		link = gen_code_html+"#"+id_name[0]
		line = re.sub(r"rq\d","<a href='"+link+"' id='"+id_name[0]+"'>"+id_name[0]+"</a>",line)
	return line

def write_code_html(txt,html,gen_code_html):
	write_head(html,'code')
	write_css(html)
	content = '<pre style="word-wrap: break-word; white-space: pre-wrap;">'
	html.write(content)
	for line in txt.readlines():
		# code.py
		link = write_code_content(line)
		html.write(link)
		link =''
	html.write("</pre>")
	write_foot(html)
	txt.close()
	html.close()

def write_srs_html(txt,html,gen_srs_html):
	write_head(html,'srs')
	write_css(html)
	content = '<pre style="word-wrap: break-word; white-space: pre-wrap;">'
	html.write(content)
	for line in txt.readlines():
		# code.py
		link = write_srs_content(line)
		html.write(link)
		link =''
	html.write("</pre>")
	write_foot(html)
	txt.close()
	html.close()

def write_head(html,title):
	head = """
	<html>
	<head><title>"""+title+"""</title>
	"""
	html.write(head)

def write_css(html):
	css = """
	<style>
	a:link {background-color:#B2FF99;} 
	a:visited {background-color:#FFFF85;}
	a:hover {background-color:#FF704D;}
	a:active {background-color:#FF704D;}
	</style>
	</head>
	<body>
	"""
	html.write(css)

def write_foot(html):
	foot = """
	</body>
	</html>
	"""
	html.write(foot)

if __name__ == '__main__':
	write_code_html(f_code_txt,f_code_html,gen_code_html)
	write_srs_html(f_srs_txt,f_srs_html,gen_srs_html)