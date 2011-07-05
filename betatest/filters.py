from betatest import *

#define filters
@app.template_filter()
def formattime(s):
	return s.strftime("%Y-%m-%d %H:%M:%S")

@app.template_filter()
def mailto(s):
	return Markup('<a href="mailto:{0}">{0}</a>'.format(s))

@app.template_filter()
def link(s, target = ''):
	if target:
		return Markup('<a href="{0}" target="{1}">{0}</a>'.format(s, target))
	else:
		return Markup('<a href="{0}">{0}</a>'.format(s))

@app.template_filter()
def humantime(s):
	diff = datetime.utcnow() - s
	if(diff.seconds < 10):
		return "just now"
	elif(diff.seconds < 60):
		return str(diff.seconds) + " second" + ("s" if diff.seconds > 1 else "") + " ago"
	mins = (diff.seconds - diff.seconds % 60) / 60
	if(mins < 60):
		return str(mins) + " minute" + ("s" if mins > 1 else "") + " ago"
	hours = (mins - mins % 60) / 60
	if(hours < 24):
		return str(hours) + " hour" + ("s" if hours > 1 else "") + " ago"
	if(diff.days < 14):
		return str(diff.days) + " day" + ("s" if diff.days > 1 else "") + " ago"
	weeks = (diff.days - diff.days % 7) / 7
	if(weeks <= 4):
		return str(weeks) + " week" + ("s" if weeks > 1 else "") + " ago"
	return formattime(s)


@app.template_filter()
def wordcrop(s, word_count):
	part = re.search("^(([^\s]*)\s*){" + str(word_count) + "}", s).group(0)
	if part != s:
		part += "..."
	return part

@app.template_filter()
def charcrop(s, char_count):
	part = s[:char_count]
	if part != s:
		part += "..."
	return part

@app.template_filter()
def search_highlight(s, q):
	if not q:
		return s
	s = s.replace(q, '<span class="highlight">' + q + '</span>')
	return Markup(s)
