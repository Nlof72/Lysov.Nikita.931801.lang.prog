import requests
import json

url = 'http://127.0.0.1:8080'

print('\nGET')

print('\ntime in server zone -\t' + requests.get(url).text)

print('\ntime in server zone -\t' + requests.get(url+'/America/Chihuahua').text)

print('\nCheck on error in GET')

print('\ntime in server zone -\t' + requests.get(url+'/Etc/GMT+30').text)


print('\nPOST')
data = {'tz_start': 'America/Chihuahua', 'type': 'date'}
print('\ndate -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'America/Chihuahua', 'type': 'time'}
print('\ntime -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'type': 'time'}
print('\ntime(No parametr) -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'type': 'date'}
print('\ntime(No parametr) -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'America/Chihuahua', 'tz_end': 'Australia/Darwin', 'type': 'datediff'}
print('\nTime difference -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_end': 'America/Chihuahua', 'tz_start': 'Australia/Darwin', 'type': 'datediff'}
print('\nTime difference -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Etc/GMT-12', 'tz_end': 'Etc/GMT+12', 'type': 'datediff'}
print('\nTime difference -\t' + requests.post(url=url, data=json.dumps(data)).text) #разница в -день

data = {'tz_start': 'Etc/GMT+12', 'tz_end': 'Etc/GMT-12', 'type': 'datediff'}
print('\nTime difference -\t' + requests.post(url=url, data=json.dumps(data)).text) #разница в +день

data = {'tz_start': 'Etc/GMT+12', 'tz_end': 'Etc/GMT+12', 'type': 'datediff'}
print('\nTime difference -\t' + requests.post(url=url, data=json.dumps(data)).text)

print('\nCheck on error in POST')

data = {'tz_end': 'Etc/GMT+12', 'type': 'datediff'}
print('\nWithout start argument -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Etc/GMT+12', 'type': 'datediff'}
print('\nWithout end argument -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'America/Chihuahu', 'tz_end': 'Australia/Darwin', 'type': 'datediff'}
print('\nUnknown time zone in first argument  -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'America/Chihuahua', 'tz_end': 'Australia/Darwi', 'type': 'datediff'}
print('\nUnknown time zone in second argument -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'type': 'datediff'}
print('\nWithout all arguments -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Etc/GMT+12', 'tz_end': 'Etc/GMT+12'}
print('\nWithout type -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Etc/GMT+12', 'tz_end': 'Etc/GMT+12'}
print('\nWithout json.dump() -\t' + requests.post(url=url, data=data).text)