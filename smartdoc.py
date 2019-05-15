import webbrowser
import sys
import re

# C:\Users\Administrator\Desktop\file\smartdoc\code.py
# C:\Users\Administrator\Desktop\file\smartdoc\srs.txt

file_code_addr = sys.argv[1]
file_srs_addr = sys.argv[2]
gen_code_html = "code.html"
gen_srs_html = "srs.html"
dict_rq = {}
dict_ra = {}
dict_tc = {}
dict_link = {}
srs ={}

f_code_txt = open(file_code_addr,'r')
f_srs_txt = open(file_srs_addr,'r')
f_code_html = open(gen_code_html,'w')
f_srs_html = open(gen_srs_html,'w')

name_func =''
line_num = 0

#code.py
def write_code_content(line):
	global name_func,line_num
	if name_func!='':
		line_num+=1

	if line.find("def")!=-1:
		name_func = re.findall(".*def(.*):.*",line)[0]
		print(name_func)
		# 已经把#{see rq1}存入字典，它的值为‘’，每次当发现def后，可以把该字典中value为‘’的值修改为获得的name
		for key in dict_link:
			if dict_link[key]=='':
				dict_link[key]=name_func+"_"+str(line_num)	
	if line.find("return")!=-1:
		name_func=''
		line_num = 0

	# 关于line.find("#{see rq/ra/tc")的方法，简化代码
	if line.find("#{see rq")!=-1:
		id_name_rq = re.findall(r"rq\d",line)
		print(id_name_rq)
		if not id_name_rq[0] in dict_rq:
			dict_rq[id_name_rq[0]] = 1
		else:
			dict_rq[id_name_rq[0]] += 1

		num = dict_rq[id_name_rq[0]]
		while num>=1:
			name = id_name_rq[0]+"_"+str(num)
			num-=1
			if not name in dict_link:
				dict_link[name]= ''
		
		if name_func!='':
			dict_link[name] = name_func+"_"+str(line_num)	

		id_whole = id_name_rq[0]+"_"+str(dict_rq[id_name_rq[0]])
		link = gen_srs_html+"#"+id_name_rq[0]

		#只有这一段是第二次的write_code_html需要的
		# 先生成code，获得了存在的id并存入字典，
		# 再从srs生成存在的id，进行比较
		# 比较后code中多余的id需要链接到其他页面（如wrong.html）
		if id_name_ra[0] not in srs:
			link = "wrong.html"

		line = re.sub(r"#{see rq\d","<a href='"+link+"' id='"+id_whole+"'>"+"#{see "+id_name_rq[0]+"}"+"</a>",line)
	if line.find("#{see ra")!=-1:
		id_name_ra = re.findall(r"ra\d",line)
		print(id_name_ra)
		if not id_name_ra[0] in dict_ra:
			dict_ra[id_name_ra[0]] = 1
		else:
			dict_ra[id_name_ra[0]] += 1

		num = dict_ra[id_name_ra[0]]
		while num>=1:
			name = id_name_ra[0]+"_"+str(num)
			num-=1
			if not name in dict_link:
				dict_link[name]=''
		if name_func!='':
			dict_link[name] = name_func+"_"+str(line_num)	

		id_whole = id_name_ra[0]+"_"+str(dict_ra[id_name_ra[0]])
		
		link = gen_srs_html+"#"+id_name_ra[0]

		if id_name_ra[0] not in srs:
			link = "wrong.html"

		line = re.sub(r"#{see ra\d}","<a href='"+link+"' id='"+id_whole+"'>"+"#{see "+id_name_ra[0]+"}"+"</a>",line)
	if line.find("#{see tc")!=-1:
		id_name_tc = re.findall(r"tc\d",line)
		print(id_name_tc)
		if not id_name_tc[0] in dict_tc:
			dict_tc[id_name_tc[0]] = 1
		else:
			dict_tc[id_name_tc[0]] += 1

		num = dict_tc[id_name_tc[0]]
		while num>=1:
			name = id_name_tc[0]+"_"+str(num)
			num-=1
			if not name in dict_link:
				dict_link[name]=''
		if name_func!='':
			dict_link[name] = name_func+"_"+str(line_num)	

		id_whole = id_name_tc[0]+"_"+str(dict_tc[id_name_tc[0]])
		link = gen_srs_html+"#"+id_name_tc[0]

		if id_name_ra[0] not in srs:
			link = "wrong.html"

		line = re.sub(r"#{see tc\d","<a href='"+link+"' id='"+id_whole+"'>"+"#{see "+id_name_tc[0]+"}"+"</a>",line)
	return line
#srs.txt
def write_srs_content(line):
	# 代码精简
	if line.find("[id=rq")!=-1:
		id_name_rq = re.findall(r"rq\d",line)
		srs[id_name_rq[0]]=''
		link = gen_code_html+"#"+id_name_rq[0]
		line = re.sub(r"rq\d","<a href='"+link+"' id='"+id_name_rq[0]+"'>"+id_name_rq[0]+"</a>",line)
		select = """<form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="code.html">请选择需要跳转至的链接</option>"""
		i = 1
		while (i <= dict_rq[id_name_rq[0]] ):
			link = gen_code_html+"#"+id_name_rq[0]+"_"+(str(i))
			name = id_name_rq[0]+"_"+(str(i))
			select += '<option value="'+link+'">'+dict_link[name]+'</option>'
			i+=1
		select += '</select></form>'
		line +=select
	if line.find("[id=ra")!=-1:
		id_name_ra = re.findall(r"ra\d",line)
		srs[id_name_ra[0]]=''
		link = gen_code_html+"#"+id_name_ra[0]
		line = re.sub(r"ra\d","<a href='"+link+"' id='"+id_name_ra[0]+"'>"+id_name_ra[0]+"</a>",line)
		select = """<form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="code.html">请选择需要跳转至的链接</option>"""
		i = 1
		while (i <= dict_ra[id_name_ra[0]] ):
			link = gen_code_html+"#"+id_name_ra[0]+"_"+(str(i))
			name = id_name_ra[0]+"_"+(str(i))
			select += '<option value="'+link+'">'+dict_link[name]+'</option>'
			i+=1
		select += '</select></form>'
		line +=select
	if line.find("[id=tc")!=-1:
		id_name_tc = re.findall(r"tc\d",line)
		srs[id_name_tc[0]]=''
		link = gen_code_html+"#"+id_name_tc[0]
		line = re.sub(r"tc\d","<a href='"+link+"' id='"+id_name_tc[0]+"'>"+id_name_tc[0]+"</a>",line)
		select = """<form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="code.html">请选择需要跳转至的链接</option>"""
		i = 1
		while (i <= dict_tc[id_name_tc[0]] ):
			link = gen_code_html+"#"+id_name_tc[0]+"_"+(str(i))
			name = id_name_tc[0]+"_"+(str(i))
			select += '<option value="'+link+'">'+dict_link[name]+'</option>'
			i+=1
		select += '</select></form>'
		line +=select
	return line

 #code界面的id在对应srs页面中没有对应，产生报错界面
def read_code(txt,html):
	for key1,value1 in dict_rq.items():
		if not key1 in srs:
			i = dict_rq[key1]
			while (i>0):
				dict_link[key1+"_"+str(i)] ='1'
				i-=1
	for key2,value2 in dict_ra.items():
		if not key2 in srs:
			i = dict_ra[key2]
			while (i>0):
				dict_link[key2+"_"+str(i)] ='1'
				i-=1
	for key3,value3 in dict_tc.items():
		if not key3 in srs:
			i = dict_tc[key3]
			while (i>0):
				dict_link[key3+"_"+str(i)] ='1'
				i-=1

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


	# 为了第二次方法的调用
	#txt.close()
	#html.close()


def write_srs_html(txt,html,gen_srs_html):
	write_head(html,'srs')
	write_function(html)
	write_css(html)
	content = '<pre style="word-wrap: break-word; white-space: pre-wrap;">'
	html.write(content)
	for line in txt.readlines():
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
	print(head)
	html.write(head)
def write_function(html):
	function_jump = """
	<script type="text/javascript">
	function MM_jump(targ,selObj) {
		eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
	}
	</script>
	"""
	html.write(function_jump)
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
	read_code(f_code_txt,f_code_html)
	# 如何避免第二次的write_code_html方法
	write_code_html(f_code_txt,f_code_html,gen_code_html)