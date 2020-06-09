import re

line = '127.0.0.1 - rj [13/Nov/2019:14:43:30] "GET HTTP/1.0" 200'
m = re.search(r'(?P<IP>\d+\.\d+\.\d+\.\d)', line) #Dessa maneira eu consigo colocar o nome na regex
print(m.group("IP"))

r = r'(?P<IP>\d+\.\d+\.\d+\.\d)'

r += r' - (?P<User>\w+) '

r += r'\[(?P<Time>\d\d/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})\]'

log_regex = re.compile(r)

m = re.search(r, line)
print(m.group('Time'))
print(m.group('User'))
print(m.group('IP'))

print(m)

print(log_regex.search(line).group("IP"))



