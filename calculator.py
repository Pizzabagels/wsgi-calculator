"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    # args provided.
    sum = "0"
    try:
        sum = int(args[0]) + int(args[1])
        return str(sum)
    except TypeError:
        return "Incorrect values entered"

def subtract(*args):
    sum = "0"
    try:
        sum = int(args[0]) - int(args[1])
        return str(sum)
    except TypeError:
        return "Incorrect values entered"

def multiply(*args):
    sum = "0"
    try:
        sum = int(args[0]) * int(args[1])
        return str(sum)
    except TypeError:
        return "Incorrect values entered"

def divide(*args):
    sum = "0"
    try:
        sum = int(args[0]) / int(args[1])
        return str(sum)
    except TypeError:
        return "Incorrect values entered"


def homepage():
    body = ['<h1>Welcome to the WSGI Calculator</h1>'
            '<p>In order to use this please submit requests in the following format.</p>' 
            '<p>localhost:8080/FUNCTION/number1/number2</p>'
            '<p>Example - http://localhost:8080/add/23/42      => 65</p>'
            '<p>Currently supports add, subtract, multiply, divide.</p>'
            '<ul>']
    body.append('</ul>')
    return '\n'.join(body)

def resolve_path(path):
    funcs = {
        '': homepage,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

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
