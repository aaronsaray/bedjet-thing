try:
  import usocket as socket
except:
  import socket
import gc


class WebServer:
    def __init__(self, status_led):
        self.status_led = status_led
        self.socket = ''
        self.run()

    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', 80))
            self.socket.listen(5)
        except OSError as e:
            print('Failed to open socket')
            print(e)
            return
        
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

    def handle_response(self, request, connection):
        response = 'I am a web page'
        connection.send('HTTP/1.1 200 OK\n')
        connection.send('Content-Type: text/html\n')
        connection.send('Connection: close\n\n')
        connection.sendall(response)
        connection.close()
