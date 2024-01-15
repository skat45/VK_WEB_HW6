from urllib.parse import parse_qs, parse_qsl


def application(environ, start_response):
    output = [str.encode(environ['REQUEST_METHOD']) + b'\n']

    post_resp = parse_qs(environ['wsgi.input'].read())
    if environ['REQUEST_METHOD'] == 'POST':
        output.append(str.encode('Post data:\n'))
        for post in post_resp:
            output.append(post)
            output.append(str.encode(" = "))
            output.append(post_resp[post][0])
            output.append(str.encode('\n'))

    get_resp = parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            output.append(str.encode('Get data:\n'))
            for get in get_resp:
                output.append(str.encode(' = '.join(get)))
                output.append(str.encode('\n'))

    start_response('200 OK', [('Content-type', 'text/plain')])
    return output
