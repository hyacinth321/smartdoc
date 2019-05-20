import webbrowser,sys,re

# C:\Users\Administrator\Desktop\file\smartdoc\code.py
# C:\Users\Administrator\Desktop\file\smartdoc\srs.txt

file_code_addr,file_srs_addr = sys.argv[1],sys.argv[2]
gen_code_html,gen_srs_html = "code.html","srs.html"
dict_rq,dict_ra,dict_tc,dict_link,srs = {},{},{},{},{}

f_code_txt = open(file_code_addr,'r')
f_srs_txt = open(file_srs_addr,'r')
f_code_html = open(gen_code_html,'w')
f_srs_html = open(gen_srs_html,'w')

name_func =''
line_num = 0

# code_find_link(line,rq,dict_rq,srs)
# 用于为#{see ..}生成链接
def code_find_link(line,name,dict_name,srs_name):
	id_name = re.findall((name+r"\d"),line)
	if not id_name[0] in dict_name:
		dict_name[id_name[0]] = 1
	else:
		dict_name[id_name[0]] += 1

	num = dict_name[id_name[0]]
	while num>=1:
		name = id_name[0]+"_"+str(num)
		num-=1
		if not name in dict_link:
			dict_link[name]= ''
	
	if name_func!='':
		dict_link[name] = name_func+"_"+str(line_num)	

	id_whole = id_name[0]+"_"+str(dict_name[id_name[0]])
	link = gen_srs_html+"#"+id_name[0]

	line=re.sub("#{see "+id_name[0]+"}","<a href='"+link+"' id='"+id_whole+"'>"+"#{see "+id_name[0]+"}"+"</a>",line)
	return line

#code.py
def write_code_content(line):
	global name_func,line_num
	if name_func!='':
		line_num+=1

	if line.find("def")!=-1:
		name_func = re.findall(".*def(.*):.*",line)[0]
		# 已经把#{see rq1}存入字典，它的值为‘’，每次当发现def后，可以把该字典中value为‘’的值修改为获得的name
		for key in dict_link:
			if dict_link[key]=='':
				dict_link[key]=name_func+"_"+str(line_num)	
	if line.find("return")!=-1:
		name_func=''
		line_num = 0

	if line.find("#{see rq")!=-1:
		line = code_find_link(line,'rq',dict_rq,srs)

	if line.find("#{see ra")!=-1:
		line = code_find_link(line,'ra',dict_ra,srs)

	if line.find("#{see tc")!=-1:
		line = code_find_link(line,'tc',dict_tc,srs)

	return line

# srs_part(line,rq,dict_rq,srs)
# 用于为#{see ..}生成链接
# 将内容添入table显示在html页面
def srs_part(line,name,dict_name,srs_name):
	id_name = re.findall((name+r"\d"),line)
	# 生成table
	if name == 'rq':
		line = re.sub("@Requirement","""
			<table align="center" border="1" width="80%" bgcolor="#e9faff" cellpadding="2">
			<tr align="center">
           		<td>Name</td>
           		<td>id</td>
            	<td>description</td>
            	<td>link</td>
        	</tr>
        	<tr align="center">
				<td>Requirement</td>
			""",line)
	elif name == 'ra':
		line = re.sub("Rationale","""
				</td>
			</tr>
			<tr align="center">
				<td>Rational</td>
			""",line)
	else:
		line = re.sub("TestCase","""
				</td>
			<tr align="center">
				<td>TestCase</td>
			""",line)
	line = line.replace("[id","<td>[id")
	line = line.replace("[description","</td><td>[description")

	# 修改id链接
	srs[id_name[0]]=''
	link = gen_code_html+"#"+id_name[0]
	select = """</td><td><form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="srs.html">please select</option>"""
	i = 1
	while (i <= dict_name[id_name[0]] ):
		link = gen_code_html+"#"+id_name[0]+"_"+(str(i))
		name = id_name[0]+"_"+(str(i))
		select += '<option value="'+link+'">'+dict_link[name]+'</option>'
		i+=1
	select += '</select></form></td></tr>'
	line +=select
	return line

#srs.txt
def write_srs_content(line):
	# 代码精简
	if line.find("[id=rq")!=-1:
		line = srs_part(line,'rq',dict_rq,srs)
		
	elif line.find("[id=ra")!=-1:
		line = srs_part(line,'ra',dict_ra,srs)

	elif line.find("[id=tc")!=-1:
		line = srs_part(line,'tc',dict_tc,srs)

	elif line.find("Priority")!=-1:
		line = line.replace("Priority","""
			<tr align="center">
				<td>Priority</td>
			""")
		# 用于预防description的长度过长超出id所在的那行
		line = line.replace("[","""<td colspan="3">""")
		line = line.replace("]","</td></tr></table>")


	return line

 # 若srs中不存在id，修改dict_link中id对应的链接
 # 但此时已经生成code.html，并关闭html(html.close())
 # 该方法目前可加可不加
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
# 通过srs.html中的id，将code.html不存在于srs_id中的id的对应链接修改为wrong.html
def update_code(file):
	file_data = ''
	new_str = 'href="www.baidu.com"'
	with open(file, "r") as f:
		for line in f:
			if line.find("#{see rq")!=-1:
				id_name = re.findall(("rq"+r"\d"),line)
				if id_name[0] in line:
					old_str = "href='srs.html#"+id_name[0]+"'"
					if not id_name[0] in srs:
						line = line.replace(old_str,new_str)
			if line.find("#{see ra")!=-1:
				id_name = re.findall(("ra"+r"\d"),line)
				if id_name[0] in line:
					old_str = "href='srs.html#"+id_name[0]+"'"
					if not id_name[0] in srs:
						line = line.replace(old_str,new_str)
			if line.find("#{see tc")!=-1:
				id_name = re.findall(("tc"+r"\d"),line)
				if id_name[0] in line:
					old_str = "href='srs.html#"+id_name[0]+"'"
					if not id_name[0] in srs:
						line = line.replace(old_str,new_str)
			file_data += line
	with open(file,"w") as f:
		f.write(file_data)

# 生成code.html
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

# 生成srs.html
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
	read_code(f_code_txt,f_code_html) # 可不用
	update_code(gen_code_html)