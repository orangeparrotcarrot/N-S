from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import hashlib, time

usernames = ["admin", "chris", "greg", "john", "test"]
passwords = ["12345qwert", "ncc1701d", "zxcvbn", "1qaz2wsx", "ncc1701d"]
max_login_retries = []
retry_period = 300.0
newpasswords = []
timeCheck = {}


class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers['Authorization'] == None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('no auth header received', 'UTF-8'))
            pass
        elif self.verify(self.headers['Authorization']):
            self.do_HEAD()
            self.wfile.write(bytes('Welcome valid user!<br><br>Here is your secret bitcoin private key: KworuAjAtnxPhZARLzAadg9WTVKjY4kckS8pw38JrD33CeVYUuDm.<br><br>Happy spending!', 'UTF-8'))
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(bytes(self.headers['Authorization'], 'UTF-8'))
            self.wfile.write(bytes(' not authenticated', 'UTF-8'))
            print('.', end='', flush=True)
            pass

    def verify(self, data):
        address = self.client_address[0]
        raw_data = base64.b64decode(data[6:]).decode('UTF-8')
        username = raw_data.split(':')[0]
        password = raw_data.split(':')[1]
        if address in timeCheck:
            if timeCheck[address] < time.time():
                timeCheck.pop(address)
            else:
                print(f'locked out until {timeCheck[address]}')
                return False
        for i in range(len(usernames)):
            password = hashlib.sha3_256(password).hexdigest()
            if (username[i] == username) and (newpasswords[i] == password):
                print(usernames[i]+' has logged in!')
                return True
        max_login_retries.append(1)
        if len(max_login_retries) > 3:
            timeCheck[address] = time.time() + retry_period
            print(f'too many attempts. locked out until {timeCheck[address]}.\n time now: {time.time()}')
        return False

    def log_message(self, format, *args):
        return

def main():
   try:
      for i in passwords:
          newpasswords.append(hashlib.sha3_256(i).hexdigest())
      httpd = HTTPServer(('', 12345), Handler)
      print ('started httpd...')
      httpd.serve_forever()
   except KeyboardInterrupt:
      print ('^C received, shutting down server')
      httpd.socket.close()

if __name__ == '__main__':
    main()
