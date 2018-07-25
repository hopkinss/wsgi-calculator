import  traceback


def add(*args):
    text=f"The sum of {'+'.join(args)} = {sum([int(i) for i in args])}"
    content='<h1>' + text + '</h1>'
    return content

def subtract(*args):
    text=f"The difference of {'-'.join(args)} = {int(args[0])-int(args[1])}"
    content='<h1>' + text + '</h1>'
    return content

def multiply(*args):
    text=f"The product of {'*'.join(args)} = {int(args[0])*int(args[1])}"
    content='<h1>' + text + '</h1>'
    return content

def divide(*args):
    content=""
    try:
        text=f"The quotient of {'/'.join(args)} = {int(args[0])/int(args[1])}"
        content='<h1>' + text + '</h1>'
    except ZeroDivisionError:
        content='<div><img src="divide.jpg" alt="no divide by zero"></div>'
    finally:
        return content
    return content

def operations():
    op_list=['add','subtract','multiply','divide']
    contents = "<!DOCTYPE html><html>"
    contents += '<head><script>function myFunction() {document.getElementById("op1").value;}</script></head>'
    contents += "<body><h4>Perform an operation on the list of numbers</h4>"
    contents += "<p>Navigate to the add,subtract,multiply, or divide pages using the pattern below</p>"
    contents += "<p>[operation]/[value 1]/[value 2]</p>"
    contents += "</body></html>"

    return contents


def resolve_path(path):
    funcs={'':operations,
           'add':add,
           'subtract':subtract,
           'multiply':multiply,
           'divide':divide}

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]
    print(func_name)
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

