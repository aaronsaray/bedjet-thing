try:
  import usocket as socket
except:
  import socket
import gc


class WebServer:
    def __init__(self, status_led, wifi_connection):
        self.status_led = status_led
        self.wifi_connection = wifi_connection
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
        contentType = 'text/html'
        page = filename
        content = ''

        if filename == '/':
            page = '/index.html'
        elif filename == '/htmx.min.js':
            contentType = 'text/javascript'
        elif filename == '/logo-full.png':
            contentType = 'image/png'
        elif filename == '/stars-bg.jpg':
            contentType = 'image/jpeg'
        elif filename == '/favicon.ico':
            contentType = 'image/x-icon'
        elif filename == '/api/wifis':
            content = self.get_wifis_list_content()

        if content == '':
            content = self.get_content('web' + page)

        connection.send('HTTP/1.1 200 OK\n')
        connection.send('Content-Type: ' + contentType + '\n')
        connection.send('Connection: close\n\n')
        connection.sendall(content)
        connection.close()

    def get_wifis_list_content(self):
        self.wifi_connection.active(True)
        ssid_collection = ''
        ssids = set()

        for ssid, *_ in self.wifi_connection.scan():
            decoded = ssid.decode('utf-8')
            if decoded:
                ssids.add(decoded)

        for s in ssids:
            ssid_collection = ssid_collection + """
                <a href="#" hx-on:click="
                    document.querySelector('#ssid').value = '{0}';
                    document.querySelector('dialog').showModal();
                ">
                    {0}
                </a>
            """.format(s)

        if ssid_collection == '':
            result = '<div style="text-align: center; font-weight: bold; color; red">No WiFi is within range or discoverable.</div>'
        else:
            dialog = """
                <dialog>
                    <form hx-get="wifi-auth-success.htmx" hx-swap="outerHTML">
                        <div id="form-container">
                            <label for="ssid">SSID:</label> 
                            <input type="text" readonly name="ssid" id="ssid" />
                            <label for="password">WiFi Password:</label>
                            <input type="text" name="password" id="password" autofocus required />
                            <button type="submit">Connect</button>
                            <div id="cancel">
                                <a href="#" id="go-back" hx-on:click="document.querySelector('dialog').close()">Cancel</a>
                            </div>
                        </div>
                    </form>
                </dialog>
                """
            result = ssid_collection + dialog

        return '<div id="wifi-list">{0}</div>'.format(result)