import time
import json
def app(environ, start_response):

    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%H:%M:%S", named_tuple)

    data = json.dumps({'time': time_string, "url": environ["HTTP_HOST"]})
    bdata = bytes(data, 'utf-8')

    start_response("200 OK", [
        ("Content-type", "application/json")
    ])
    return [bdata]