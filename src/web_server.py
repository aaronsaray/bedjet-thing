try:
  import usocket as socket
except:
  import socket
import gc


class WebServer:
    def __init__(self, status_led):
        self.status_led = status_led
        self.socket = ''
        self.server = ''
        print('Starting server')
        self.run()

    def configure_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', 80))
            self.socket.listen(5)
        except OSError as e:
            print('Failed to open socket')
            print(e)

    def run(self):
        self.configure_server()
        self.status_led.done()

        while True:
            try:
                if gc.mem_free() < 102000:
                    gc.collect()
        
                connection, addr = self.socket.accept()
                connection.settimeout(3.0)

                request = connection.recv(1024)
                connection.settimeout(None)
                request = str(request)

                print('Incoming request')
                print(request)

                self.handle_response(request, connection);

            except OSError as e:
                connection.close()
                print('Connection closed error')
                print(e)

    def get_content(self, file):
        with open(file, 'rb') as f:
            c = f.read()
            f.close()
        return c

    def handle_response(self, request, connection):
        headers = request.split('\n')
        filename = headers[0].split()[1]

        # I know this is pretty bad
        if filename == '/':
            content = self.get_content('web/first.html')
            contentType = 'text/html'
        elif filename == '/htmx.min.js':
            content = self.get_content('web/htmx.min.js')
            contentType = 'text/javascript'
        elif filename == '/logo-full.png':
            content = self.get_content('web/logo-full.png')
            contentType = 'image/png'
        elif filename == '/stars-bg.jpg':
            content = self.get_content('web/stars-bg.jpg')
            contentType = 'image/jpeg'
        elif filename == '/favicon.ico':
            content = self.get_content('web/favicon.ico')
            contentType = 'image/x-icon'
        else:
            content = self.get_content('web' + filename)
            contentType = 'text/html'

        connection.send('HTTP/1.1 200 OK\n')
        connection.send('Content-Type: ' + contentType + '\n')
        connection.send('Connection: close\n\n')
        connection.sendall(content)
        connection.close()
