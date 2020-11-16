from datetime import datetime
from pytz import timezone, UnknownTimeZoneError
from paste import reloader
from paste.httpserver import serve
from tzlocal import get_localzone
import json

def app(environ, start_response):
    # Except error
    if 'error' in environ['PATH_INFO'].lower():
        raise Exception('Detect "error" in URL path')

    local_time = get_localzone()
    if environ['REQUEST_METHOD'] == 'GET':
        set_path = environ['PATH_INFO'][1:]
        serv='The time'
        if set_path:
            try:
                timezone1 = timezone(set_path)
                serv+=' in '+str(set_path)+' time zone is '
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [bytes('Unknown time zone', encoding='utf-8')]
        else:
            serv+=' server is '
            timezone1 = local_time

        # Generate response
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes(serv+datetime.now(tz=timezone1).strftime('%I:%M:%S%p %Z'), encoding='utf-8')]

    elif environ['REQUEST_METHOD'] == 'POST':
        received_data = environ['wsgi.input'].read().decode("utf-8")
        try:
            received_data = json.loads(received_data)
        except:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes('Error in input Data', encoding='utf-8')]

        try:
            type = received_data['type']
        except:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes('Error in type Data', encoding='utf-8')]

        if type == 'date' or type == 'time':
            try:
                zona = received_data['tz_start']
                try:
                    zona = timezone(zona)
                except UnknownTimeZoneError:
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                    return [bytes('UnknownTimeZoneError', encoding='utf-8')]
            except:
                zona = local_time
            start_response('200 OK', [('Content-Type', 'text/plain')])
            if type == 'date':
                return [bytes(json.dumps({'Date': datetime.now(tz=zona).strftime('%d %b %Y'), 'TimeZone': str(zona)}), encoding='utf-8')]
            else:
                return [bytes(json.dumps({'Time': datetime.now(tz=zona).strftime('%I:%M:%S%p %Z'), 'TimeZone': str(zona)}), encoding='utf-8')]

        if type == 'datediff':
            try:
                timezone1 = received_data['tz_start']
                try:
                    timezone2 = received_data['tz_end']
                except:
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                    return [bytes('Missed second or all arguments', encoding='utf-8')]
            except:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [bytes('Missed first or all arguments', encoding='utf-8')]
            try:
                timezone1 = timezone(timezone1).localize(datetime.now())
                try:
                    timezone2 = timezone(timezone2).localize(datetime.now())
                except UnknownTimeZoneError:
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                    return [bytes('Second argument UnknownTimeZoneError', encoding='utf-8')]
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [bytes('first argument UnknownTimeZoneError', encoding='utf-8')]

            a = datetime.astimezone(timezone1)
            b = datetime.astimezone(timezone2)
            if a>=b:
                diff = a-b
                diff = str(diff)
            else:
                diff = b-a
                diff = '-' + str(diff)
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes(json.dumps({'Difference': diff, 'Start_zone': str(received_data['tz_start']), 'End_zone': str(received_data['tz_end'])}), encoding='utf-8')]

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes('Type isn`t identified', encoding='utf-8')]

    else:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes('REQUEST_METHOD isn`t identified', encoding='utf-8')]


if __name__ == '__main__':

    reloader.install()
    serve(app)
