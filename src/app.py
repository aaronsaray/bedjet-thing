from src.microdot import Microdot, send_file
import time
import machine

class App:
    def __init__(self, wifi_radio, write_credentials):
        self.wifi_radio = wifi_radio
        self.write_credentials = write_credentials
        self.ip = None
        self.restart = False
        self.start_microdot()

    def debug(self, message):
        print('DEBUG: ', end='')
        print(message)

    def start_microdot(self):
        self.debug('starting microdot')

        app = Microdot()

        @app.route('/')
        async def index(request):
            if self.wifi_radio.isconnected():
                return send_file('web/running.html')
            
            return send_file('web/index.html')

        @app.route('/htmx/initial-load')
        async def initial_load(request):
            start_part = """
                <h1>First time configuration. Welcome!</h1>
                <section>
                    <h2>Configure WiFi</h2>
                    <div id="panel">
                        <div id="panel-header">
                            <div>
                                Choose your WiFi connection from the list.
                            </div>
                            <div>
                                <a href="#" hx-get="/htmx/initial-load" hx-target="main">Refresh</a>
                            </div>
                        </div>
            """
            end_part = """
                    </div>
                </section>
            """

            self.wifi_radio.active(True)
            ssid_collection = ''
            ssids = set()

            for ssid, *_ in self.get_wifi().scan():
                decoded = ssid.decode('utf-8')
                if decoded:
                    ssids.add(decoded)

            self.wifi_radio.active(False)

            self.debug(ssids)

            for s in ssids:
                if s == 'MyWiFi2' or s == 'MonkFish': # need to figure out how to escape shit
                    ssid_collection = ssid_collection + """
                        <a href="#" hx-on:click="
                            document.querySelector('#ssid').value = '{0}';
                            document.querySelector('dialog').showModal();
                        ">
                            {0}
                        </a>
                    """.format(s)

            if ssid_collection == '':
                internal = '<div style="text-align: center; font-weight: bold; color: red">No WiFi is within range or discoverable.</div>'
            else:
                internal = '<div id="wifi-list">' + ssid_collection + '</div>' + """
                    <dialog>
                        <form hx-post="/htmx/wifi-auth" hx-indicator="#wifi-auth-button">
                            <div id="form-container">
                                <label for="ssid">SSID:</label> 
                                <input type="text" readonly name="ssid" id="ssid" />
                                <label for="password">WiFi Password:</label>
                                <input type="password" name="password" id="password" autofocus required style="border-radius: none" />
                                <button type="submit" id="wifi-auth-button">Connect</button>
                                <div id="cancel">
                                    <a href="#" id="go-back" hx-on:click="document.querySelector('dialog').close()">Cancel</a>
                                </div>
                            </div>
                        </form>
                    </dialog>
                    """

            return start_part + internal + end_part;

        @app.route('/htmx/wifi-auth', methods=['POST'])
        async def wifi_auth(request):
            ssid = request.form.get('ssid')
            password = request.form.get('password')

            if self.wifi_connect(ssid, password):
                content = """
                    <div class="padding: 1rem">
                        <div style="color: green; font-weight: bold">
                            Successfully connected.
                        </div>
                        <p>
                            Please wait a moment. Disconnecting from BedJetThing and returning to the previous connection.
                        </p>
                    </div>
                    <script>
                        setTimeout(() => {{
                            window.location.href="http://{0}";
                        }}, 10000);
                    </script>
                """.format(self.ip)
            else:
                content = """
                    <div style="color: red; font-weight: bold; margin-bottom: 1rem">
                        Can not connect. Perhaps the password is incorrect?
                    </div>
                    <div id="form-container">
                        <label for="ssid">SSID:</label> 
                        <input type="text" readonly name="ssid" id="ssid" value="{0}" />
                        <label for="password">WiFi Password:</label>
                        <input type="password" name="password" id="password" autofocus required style="border-radius: none" />
                        <button type="submit" id="wifi-auth-button">Connect</button>
                        <div id="cancel">
                            <a href="#" id="go-back" hx-on:click="document.querySelector('dialog').close()">Cancel</a>
                        </div>
                    </div>
                """.format(ssid)

            return content


        @app.route('/favicon.ico')
        async def favicon(request, path):
            return send_file('web/favicon.ico', max_age=86400)

        @app.route('/assets/<path:path>')
        async def web(request, path):
            if '..' in path:
                return 'Not found', 404
            return send_file('web/assets/' + path, max_age=86400)
        
        @app.after_request
        def restart_device(request, response):
            if self.restart:
                self.debug('Restarting...')
                machine.reset()

        app.run(debug=True, port=80)


    def wifi_connect(self, ssid, password):
        self.debug('Trying to connect to: ' + ssid)
        
        self.wifi_radio.active(True)
        self.wifi_radio.connect(ssid, password)
        
        for _ in range(100):
            if self.wifi_radio.isconnected():
                self.debug('Connected to wifi')
                self.debug(self.wifi_radio.ifconfig())
                self.write_credentials(ssid, password)
                self.restart = True;
                self.ip = self.wifi_radio.ifconfig()[0]
                return True
            else:
                time.sleep_ms(100)
        
        self.debug('Unable to connect')        
        
        self.wifi_radio.disconnect()
        self.wifi_radio.active(False)

        return False
    

#     def handle_response(self, request, connection):
#         headers = request.split('\n')
#         filename = headers[0].split()[1]

#         # I know this is pretty bad
#         contentType = 'text/html'
#         page = filename
#         content = ''

#         if filename == '/':
#             if self.has_settings_file:
#                 page = '/running.html'
#             else:
#                 page = '/index.html'
#         elif filename == '/htmx.min.js':
#             contentType = 'text/javascript'
#         elif filename == '/logo-full.png':
#             contentType = 'image/png'
#         elif filename == '/stars-bg.jpg':
#             contentType = 'image/jpeg'
#         elif filename == '/favicon.ico':
#             contentType = 'image/x-icon'
#         elif filename == '/api/wifis':
#             content = self.get_wifis_list_content()
#         elif filename == '/api/clear-settings':
#             content = self.do_clear_settings()
#         elif filename.startswith('/api/wifi-auth'):
#             content = self.get_wifi_authenticate(request)

#         if content == '':
#             content = self.get_content('web' + page)

#         connection.send('HTTP/1.1 200 OK\n')
#         connection.send('Content-Type: ' + contentType + '\n')
#         connection.send('Connection: close\n\n')
#         connection.sendall(content)
#         connection.close()

#         if self.clear_settings:
#             os.remove('bedjet.json')

#         if self.reset:
#             time.sleep(2) # idk if this matters but it makes me feel like the response returns better
#             machine.reset()
