import webbrowser,sys,re

# C:\Users\Administrator\Desktop\file\smartdoc\code.py
# C:\Users\Administrator\Desktop\file\smartdoc\srs.txt

file_code_addr,file_srs_addr = sys.argv[1],sys.argv[2]
gen_code_html,gen_srs_html = "code.html","srs.html"
dict_rq,dict_ra,dict_tc,dict_link,srs = {},{},{},{},{}
rq_ra,rq_tc={},{}

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

	line=re.sub(r"#\s?{see "+id_name[0]+"}","<a href='"+link+"' id='"+id_whole+"'>"+"#{see "+id_name[0]+"}"+"</a>",line)
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

	if line.find("{see rq")!=-1:
		line = code_find_link(line,'rq',dict_rq,srs)

	if line.find("{see ra")!=-1:
		line = code_find_link(line,'ra',dict_ra,srs)

	if line.find("{see tc")!=-1:
		line = code_find_link(line,'tc',dict_tc,srs)

	return line

# srs_part(line,rq,dict_rq,srs)
# 用于为#{see ..}生成链接
# 将内容添入table显示在html页面
status=[]
store_ra,store_tc = [],[]
def srs_part(line,name,dict_name,srs_name):
	id_name = re.findall((name+r"\d"),line)
	# 
	if name == 'rq':
		# status存储当前表格的rq名，store_tc/ra代表该rq对应的tc/ra名
		# 当读取新一个表，即读取到rq时，list都清空，重新存储
		status.clear()
		store_tc.clear()
		store_ra.clear()
		status.append(id_name[0])
		if not id_name[0] in rq_ra:
			rq_ra[id_name[0]] = ''
			rq_tc[id_name[0]] = ''

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
		store_ra.append(id_name[0])
		line = re.sub("Rationale","""
				</td>
			</tr>
			<tr align="center">
				<td>Rational</td>
			""",line)
	elif name =='tc':
		store_tc.append(id_name[0])
		line = re.sub("TestCase","""
				</td>
			<tr align="center">
				<td>TestCase</td>
			""",line)
	line = re.sub(r"\[id\s?=\s?","<td id='"+id_name[0]+"''>[",line)
	line = re.sub(r"\[description\s?=\s?","</td><td>[",line)

	# 修改id链接
	srs[id_name[0]]=''
	link = gen_code_html+"#"+id_name[0]
	select = """</td><td><form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="srs.html">please select</option>"""
	i = 1
	if not id_name[0] in dict_name:
		dict_name[id_name[0]]=0
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
		# 这里用在创建list_ra与list_tc存储store_ra与store_tc
		# 而不是直接使用store_..，可能与地址有关，
		# 字典中前一个数据的改变会随着后一个数据的变化再变化
		list_ra,list_tc=[],[]
		for i in store_ra:
			list_ra.append(i)
		for i in store_tc:
			list_tc.append(i)
		rq_ra[status[0]] = list_ra
		rq_tc[status[0]] = list_tc
		#rq_ra[status[0]] = store_ra
		#rq_tc[status[0]] = store_tc
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
	new_str = 'href=wrong.html'
	with open(file, "r") as f:
		for line in f:
			if line.find("{see rq")!=-1:
				id_name = re.findall(("rq"+r"\d"),line)
				if id_name[0] in line:
					old_str = "href='srs.html#"+id_name[0]+"'"
					if not id_name[0] in srs:
						if id_name[0] in dict_rq:
							dict_rq.pop(id_name[0])
						line = line.replace(old_str,new_str)
			if line.find("{see ra")!=-1:
				id_name = re.findall(("ra"+r"\d"),line)
				if id_name[0] in line:
					old_str = "href='srs.html#"+id_name[0]+"'"
					if not id_name[0] in srs:
						if id_name[0] in dict_ra:
							dict_ra.pop(id_name[0])
						line = line.replace(old_str,new_str)
			if line.find("{see tc")!=-1:
				id_name = re.findall(("tc"+r"\d"),line)
				if id_name[0] in line:
					old_str = "href='srs.html#"+id_name[0]+"'"
					if not id_name[0] in srs:
						if id_name[0] in dict_tc:
							dict_tc.pop(id_name[0])
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

	# 再加matrix前，由于要用到dict_rq/ra/tc，此时存储是根据code.html，字典中某些数据可能存在与code界面但不存在与srs界面
	# 在此处修改字典中的数据
	update_code(gen_code_html)
	# 加traceable matrix
	num_rq = 0
	for value in dict_rq.values():
		num_rq = num_rq+value

	html.write(make_matrix(dict_ra,num_rq))
	html.write(make_matrix(dict_tc,num_rq))
	html.write("</pre>")
	write_foot(html)
	txt.close()
	html.close()

# 制作traceable matrix
def make_matrix(dict_name,dict_rq_num):
	index_list=[]
	store_list =[]
	num_name = 0
	num_rq=dict_rq_num
	for value in dict_name.values():
		num_name = num_name+1
	table = """
	<table border="1" bgcolor="#e9faff" cellpadding="2" style="margin-left:20%;float:left">
		<caption>traceabl matrix</caption>
		<tr>
			<td></td>
	"""
	for key,value in dict_name.items():
		num = num_name
		table = table+"<td>"+str(key)+"</td>"
	table = table +"</tr>"

	for key,value in dict_rq.items():
		index_list.clear()
		store_list.clear()
		# 通过key查找rq_ra/rq_tc中的['ra1']或['tc1','tc3']
		if dict_name == dict_ra:
			store_list = rq_ra[key]
		if dict_name == dict_tc:
			store_list = rq_tc[key]

		for i in dict_name:
			if i in store_list:
				index_list.append(list(dict_name.keys()).index(i))

		num = value
		dict_name_num = num_name # 存储ra或tc的总条数，变化不影响原值，可再用
		table = table+"<tr><td>"+str(key)+"</td>"
		index=0
		while(dict_name_num>0):
			if index in index_list:
				table = table+"<td>√</td>"
			else:
				table = table+"<td></td>"
			dict_name_num = dict_name_num-1
			index = index+1
		table = table+"</tr>"
		index=0
	table = table+"</table>"
	return table

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
	table {}
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
