import re

csrftoken = re.compile(r'<input\stype\="hidden"\sname\="CSRFToken"\svalue\="(.*)"\s/>')
phone = re.compile(r'^[1-9][1-9]9[1-9][0-9]{7}$')
