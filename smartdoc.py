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

f_code_txt = open(file_code_addr,'r')
f_srs_txt = open(file_srs_addr,'r')
f_code_html = open(gen_code_html,'w')
f_srs_html = open(gen_srs_html,'w')

#code.py
def write_code_content(line):
	if line.find("#{see rq")!=-1:
		id_name_rq = re.findall(r"rq\d",line)
		print(id_name_rq)
		if not id_name_rq[0] in dict_rq:
			dict_rq[id_name_rq[0]] = 1
		else:
			dict_rq[id_name_rq[0]] += 1
		id_whole = id_name_rq[0]+"_"+str(dict_rq[id_name_rq[0]])
		link = gen_srs_html+"#"+id_name_rq[0]
		line = "<a href='"+link+"' id='"+id_whole+"'>"+line+"</a>"
	if line.find("#{see ra")!=-1:
		id_name_ra = re.findall(r"ra\d",line)
		print(id_name_ra)
		if not id_name_ra[0] in dict_ra:
			dict_ra[id_name_ra[0]] = 1
		else:
			dict_ra[id_name_ra[0]] += 1
		id_whole = id_name_ra[0]+"_"+str(dict_ra[id_name_ra[0]])
		link = gen_srs_html+"#"+id_name_ra[0]
		line = "<a href='"+link+"' id='"+id_whole+"'>"+line+"</a>"
	if line.find("#{see tc")!=-1:
		id_name_tc = re.findall(r"tc\d",line)
		print(id_name_tc)
		if not id_name_tc[0] in dict_tc:
			dict_tc[id_name_tc[0]] = 1
		else:
			dict_tc[id_name_tc[0]] += 1
		id_whole = id_name_tc[0]+"_"+str(dict_tc[id_name_tc[0]])
		link = gen_srs_html+"#"+id_name_tc[0]
		line = "<a href='"+link+"' id='"+id_whole+"'>"+line+"</a>"
	return line
#srs.txt
def write_srs_content(line):
	if line.find("[id=rq")!=-1:
		id_name_rq = re.findall(r"rq\d",line)
		link = gen_code_html+"#"+id_name_rq[0]
		line = re.sub(r"rq\d","<a href='"+link+"' id='"+id_name_rq[0]+"'>"+id_name_rq[0]+"</a>",line)
		select = """<form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="code.html">请选择</option>"""
		i = 1
		while (i <= dict_rq[id_name_rq[0]] ):
			link = gen_code_html+"#"+id_name_rq[0]+"_"+(str(i))
			select += '<option value="'+link+'">'+(str(i))+'</option>'
			i+=1
		select += '</select></form>'
		line +=select
	if line.find("[id=ra")!=-1:
		id_name_ra = re.findall(r"ra\d",line)
		link = gen_code_html+"#"+id_name_ra[0]
		line = re.sub(r"ra\d","<a href='"+link+"' id='"+id_name_ra[0]+"'>"+id_name_ra[0]+"</a>",line)
		select = """<form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="code.html">请选择</option>"""
		i = 1
		while (i <= dict_ra[id_name_ra[0]] ):
			link = gen_code_html+"#"+id_name_ra[0]+"_"+(str(i))
			select += '<option value="'+link+'">'+(str(i))+'</option>'
			i+=1
		select += '</select></form>'
		line +=select
	if line.find("[id=tc")!=-1:
		id_name_tc = re.findall(r"tc\d",line)
		link = gen_code_html+"#"+id_name_tc[0]
		line = re.sub(r"tc\d","<a href='"+link+"' id='"+id_name_tc[0]+"'>"+id_name_tc[0]+"</a>",line)
		select = """<form action="" method="get" style="margin:0px;"><select name="jump" id="jumo" onchange="MM_jump('window',this)"><option value="code.html">请选择</option>"""
		i = 1
		while (i <= dict_tc[id_name_tc[0]] ):
			link = gen_code_html+"#"+id_name_tc[0]+"_"+(str(i))
			select += '<option value="'+link+'">'+(str(i))+'</option>'
			i+=1
		select += '</select></form>'
		line +=select
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
	write_function(html)
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