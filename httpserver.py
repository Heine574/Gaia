from http.server import *
from http import cookies
from pages import *

def registeruser(user, password):
    f = open('data/users.txt')
    data = f.read().split('\n')
    if user == '':
        f.close()
        return '<p>Invalid username.</p>|'
    elif user in data:
        f.close()
        return '<p>Username already exists!</p>|'
    else:
        f.close()
        f = open('data/users.txt', 'a')
        f.write(user + '\n')
        f.close()
        f = open('data/passwords.txt', 'a')
        f.write(password + '\n')
        f.close()
        f = open('data/characters.txt', 'a')
        f.write('Select your character\n')
        f.close()
        return '<p>Username ' + user + ' registered successfully!</p>|'
def login(user, password, returnfile):
    f = open('data/users.txt')
    data = f.read().split('\n')
    f.close()
    if user == '':
        return '<p>Invalid username. <a href="RPGgame.html">Try again.</a></p>|'
    elif user in data:
        f = open('data/passwords.txt')
        passwords = f.read().split('\n')
        f.close()
        if passwords[data.index(user)] == password:
            code = pages[returnfile](user)
            return code + '|'
        else:
            return '<p>Incorrect password! <a href="RPGgame.html">Try again.</a></p>|'
    else:
        return '<p>Invalid username. <a href="RPGgame.html">Try again.</a></p>|'
def newchar(user, name):
    f = open('data/users.txt')
    data = f.read().split('\n')
    if user == '':
        f.close()
        return '<p>Invalid username. <a href="RPGgame.html">Try again.</a></p>|'
    elif user in data:
        f.close()
        f = open('data/characters.txt')
        chars = f.read().split('\n')
        f.close()
        mychars = chars[data.index(user)].split(', ')
        mychars.append(name)
        mychars = ', '.join(mychars)
        chars[data.index(user)] = mychars
        f = open('data/characters.txt', 'w')
        for i in chars:
            f.write(i + '\n')
        f.close()
        return '<p>Character added. <a href="RPGgame.html">Return to login screen.</a></p>|'
    else:
        return '<p>Invalid username. <a href="RPGgame.html">Try again.</a></p>|'
def playchar(user, char, action, location):
    f = open('data/turn.txt')
    turn = f.read().split('\n')
    f.close()
    if char == 'Select your character':
       return '<p>Invalid character; please select another. <a href="RPGgame.html">Return to login screen.</a></p>|' 
    elif char in turn:
        return '<p>Sorry, this character has already done his/her turn; please select another. <a href="RPGgame.html">Return to login screen.</a></p>|'
    else:
        f = open('data/actions.txt', 'a')
        f.write(user + ': ' + char + ': ' + location + ': ' + action + '\n')
        f.close()
        f = open('data/turn.txt', 'a')
        f.write(char + '\n')
        f.close()
        return '<p>Action recorded. <a href="RPGgame.html">Return to login screen.</a></p>|'
def selchar(user, char, location):
    code = RPGgame(user, char, location)
    return code + '|'
def write_file(path, data):
    f = open(path, 'a')
    f.write(data)
    f.close()
    return '<p>File recorded. <a href="RPGgame.html">Return to login screen.</a></p>|'
def parse_info(data):
    data = data.replace('\\', '').split('\r\n')
    cm = {}
    for i in data:
        t = i.split('=')
        cm[t[0]] = t[1]
    ret = '<p>Sorry, no content here :(</p>|'
    if 'registeruser' in cm:
        ret = registeruser(cm['registeruser'], cm['password'])
    if 'login' in cm:
        ret = login(cm['login'], cm['password'], cm['page'])
    if 'newcharname' in cm:
        ret = newchar(cm['user'], cm['newcharname'])
    if 'playcharacter' in cm:
        ret = playchar(cm['user'], cm['playcharacter'], cm['message'], cm['location'])
    if 'selcharacter' in cm:
        ret = selchar(cm['user'], cm['selcharacter'], cm['location'])
    if 'wfile' in cm:
        ret = write_file(cm['file'], cm['data'])
    return ret

class SHTTPRH(SimpleHTTPRequestHandler):
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data = post_data.decode('utf-8')
        print(post_data)
        ret = parse_info(post_data)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(ret.encode('utf-8'))

        f = self.send_head()
        if f:
            f.close()

server_address = ('', 8000)
httpd = HTTPServer(server_address, SHTTPRH)
httpd.RequestHandlerClass.default_request_version = 'HTTP/1.1'
#httpd.RequestHandlerClass.error_message_format = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"\n"http://www.w3.org/TR/html4/strict.dtd">\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html;charset=utf-8">\n<title>Error %(code)d  %(message)s</title>\n</head>\n<body>\n<h1>Error %(code)d</h1>\n<img src="https://http.cat/%(code)d" width="350">\n<p>Error code: %(code)d</p>\n<p>Message: %(message)s.</p>\n<p>Error code explanation: %(code)s - %(explain)s.</p>\n</body>\n</html>'
httpd.serve_forever()
