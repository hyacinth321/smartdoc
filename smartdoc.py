import webbrowser
file_code_addr = "C:\\Users\\gk\\Desktop\\smartdoc\\code.py"
file_srs_addr = "C:\\Users\\gk\\Desktop\\smartdoc\\srs.txt"
gen_code_html = "code.html"
gen_srs_html = "srs.html"

'''可以写个方法传参，然后生成网页'''
f_code_txt = open(file_code_addr,'r')
f_srs_txt = open(file_srs_addr,'r')
f_code_html = open(gen_code_html,'w')
f_srs_html = open(gen_srs_html,'w')

content_code = ''
for line in f_code_txt.readlines():
	content_code=content_code+line


content_srs = f_srs_txt.read()
web_code = """
<html>
<head>code</head>
<body>
%s
</body>
</html>
"""%(content_code)
web_srs = """
<html>
<head>srs</head>
<body>
%s
</body>
</html>
"""%(content_srs)
f_code_html.write(web_code)
f_srs_html.write(web_srs)
print(content_code)
print(content_srs)
f_code_txt.close()
f_srs_txt.close()
f_code_html.close()
f_srs_html.close()
webbrowser.open(gen_code_html,new=1)
webbrowser.open(gen_srs_html,new=1)

def write_result(str,addr):
	write_content = '1'
	
def lines(file):
	for line in file:yield line
	yield '\n'