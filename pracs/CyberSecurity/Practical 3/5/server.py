import urllib.parse
import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):

    # you can ignore this function, its simply a helper function that converts sql results to html tables
    def query_to_table(self, cur, header, cls=b''):
        names = list(map(lambda x: x[0], cur.description))
        res = cur.fetchall()
        out = b"<p align='center'><table>"
        if header:
            out += b"<tr class='"+cls+b"'>"
            for i in range(len(names)):
                out += b"<th class='"+cls+b"'>" + names[i].capitalize().encode() + b"</th>"
            out += b"</tr>"
        for row in res:
            out += b"<tr class='"+cls+b"'>"
            for elm in row:
                out += b"<td class='"+cls+b"'>" + str(elm).encode() + b"</td>"
            out += b"</tr>"
        out += b"</table></p>"
        return out

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        cur = self.conn.cursor() # database cursor

        # login events
        if self.path == '/login':
            username = urllib.parse.unquote_plus(body[9:].decode('utf-8'))
            cur.execute("select * from users where username='" + username + "';")
            response = self.query_to_table(cur, True)
            cur.execute("select private.wallet from users left join private on private.userid = users.id where username='" + username + "';")
            response += self.query_to_table(cur, True)

            self.wfile.write(response)
    
        # class statistics
        if self.path == '/stats':

            cur.execute('select grade from users;')
            response = b"<b>Anonymous grades: </b>" + self.query_to_table(cur, False, b'transpose')
            cur.execute('select "Wite your own query here";')
            response += b"<b>Average class grade: </b>" + self.query_to_table(cur, False)
            cur.execute('select "Wite your own query here";')
            response += b"<b>Fines by college: </b>" + self.query_to_table(cur, False)

            self.wfile.write(response)

        # student list
        if self.path == '/list':
            cur.execute('select firstname, lastname, college from users;')
            self.wfile.write(self.query_to_table(cur, True))


if __name__ == '__main__':
    Handler.protocol_version = 'HTTP/1.0'
    Handler.conn = sqlite3.connect('secret.db') # connection to database

    try:
        httpd = HTTPServer(('', 12345), Handler)
        print ('started httpd...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        httpd.socket.close()
        Handler.conn.close()
