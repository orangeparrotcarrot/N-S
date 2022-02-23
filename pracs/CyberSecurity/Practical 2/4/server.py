import urllib.parse
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        path = urllib.parse.unquote(path)

        if path == '/':
            return 'index.html'

        # accept everything
        if re.search(r'(.*?)', path):
            return self.directory + path

        self.send_error(404)
        return 'index.html'

if __name__ == '__main__':
    Handler.protocol_version = 'HTTP/1.0'
    Handler.names = []
    Handler.messages = []
    try:
        httpd = HTTPServer(('', 12345), Handler)
        print ('started httpd...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        httpd.socket.close()
