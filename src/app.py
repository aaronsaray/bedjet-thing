from src.microdot import Microdot, send_file

class App:
    def __init__(self, wifi_connection):
        self.wifi_connection = wifi_connection
        self.start_microdot()

    def debug(self, message):
        print('DEBUG: ', end='')
        print(message)

    def start_microdot(self):
        self.debug('starting microdot')

        app = Microdot()

        @app.route('/')
        async def index(request):
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
                                <a href="#" hx-get="/htmx/initial-load-not-found" hx-target="main">Refresh</a>
                            </div>
                        </div>
            """
            end_part = """
                    </div>
                </section>
            """

            self.wifi_connection.active(True)
            ssid_collection = ''
            ssids = set()

            for ssid, *_ in self.wifi_connection.scan():
                decoded = ssid.decode('utf-8')
                if decoded:
                    ssids.add(decoded)

            self.wifi_connection.active(False)

            self.debug(ssids)

            for s in ssids:
                if s == 'MyWiFi2' or s == 'MonkFish': # need to figure out how to escape shit
                    ssid_collection = ssid_collection + """
                        <a href="#" hx-on:click="
                            document.getElementById('ssid').value = '{0}';
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
                        <form hx-get="/api/wifi-auth" hx-swap="outerHTML" hx-indicator="#wifi-auth-button">
                            <div id="form-container">
                                <label for="ssid">SSID:</label> 
                                <input type="text" readonly name="ssid" id="ssid" />
                                <label for="password">WiFi Password:</label>
                                <input type="password" name="password" id="password" autofocus required />
                                <button type="submit" id="wifi-auth-button">Connect</button>
                                <div id="cancel">
                                    <a href="#" id="go-back" hx-on:click="document.querySelector('dialog').close()">Cancel</a>
                                </div>
                            </div>
                        </form>
                    </dialog>
                    """

            return start_part + internal + end_part;

        @app.route('/favicon.ico')
        async def favicon(request, path):
            return send_file('web/favicon.ico', max_age=86400)

        @app.route('/assets/<path:path>')
        async def web(request, path):
            if '..' in path:
                return 'Not found', 404
            return send_file('web/assets/' + path, max_age=86400)

        app.run(debug=True, port=80)

        self.debug('microdot running')


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

#     def do_clear_settings(self):
#         response = """
#             <p style="color: white">Clearing settings...</p>
#             <p style="color: white">Please connect to the ESP32 WiFi again.</p>
#             <script>
#                 setTimeout(() => {
#                     window.location.href = 'http://192.168.4.1';
#                 }, 5000);
#             </script>
#         """
#         self.clear_settings = True
#         self.reset = True
#         return response


#     def get_wifi_authenticate(self, request):
#         pattern = re.compile('ssid=(.*?)&password=(.*?)\s')

#         match = re.search(pattern, request)
#         ssid = match.group(1)
#         password = match.group(2)
#         if self.wifi_connect(ssid, password):
#             content = """
#                 <div class="padding: 1rem">
#                     <div style="color: green; font-weight: bold">
#                         Successfully connected.
#                     </div>
#                     <p>
#                         Please wait a moment. Disconnecting from BedJet32 and returning to the previous connection.
#                     </p>
#                 </div>
#                 <script>
#                     setTimeout(() => {{
#                         window.location.href="http://{0}";
#                     }}, 10000);
#                 </script>
#             """.format(self.ip)
#         else:
#             content = """
#                 <form hx-get="/api/wifi-auth" hx-swap="outerHTML" hx-indicator="#wifi-auth-button">
#                     <div style="color: red; font-weight: bold; margin-bottom: 1rem">
#                         Can not connect. Perhaps the password is incorrect?
#                     </div>
#                     <div id="form-container">
#                         <label for="ssid">SSID:</label> 
#                         <input type="text" readonly name="ssid" id="ssid" value="{0}" />
#                         <label for="password">WiFi Password:</label>
#                         <input type="password" name="password" id="password" autofocus required />
#                         <button type="submit" id="wifi-auth-button">Connect</button>
#                         <div id="cancel">
#                             <a href="#" id="go-back" hx-on:click="document.querySelector('dialog').close()">Cancel</a>
#                         </div>
#                     </div>
#                 </form>        
#             """.format(ssid)

#         return content

#     def get_wifis_list_content(self):
#         self.wifi_connection.active(True)
#         ssid_collection = ''
#         ssids = set()

#         for ssid, *_ in self.wifi_connection.scan():
#             decoded = ssid.decode('utf-8')
#             if decoded:
#                 ssids.add(decoded)

#         for s in ssids:
#             ssid_collection = ssid_collection + """
#                 <a href="#" hx-on:click="
#                     document.querySelector('#ssid').value = '{0}';
#                     document.querySelector('dialog').showModal();
#                 ">
#                     {0}
#                 </a>
#             """.format(s)

#         if ssid_collection == '':
#             result = '<div style="text-align: center; font-weight: bold; color; red">No WiFi is within range or discoverable.</div>'
#         else:
#             dialog = """
#                 <dialog>
#                     <form hx-get="/api/wifi-auth" hx-swap="outerHTML" hx-indicator="#wifi-auth-button">
#                         <div id="form-container">
#                             <label for="ssid">SSID:</label> 
#                             <input type="text" readonly name="ssid" id="ssid" />
#                             <label for="password">WiFi Password:</label>
#                             <input type="password" name="password" id="password" autofocus required />
#                             <button type="submit" id="wifi-auth-button">Connect</button>
#                             <div id="cancel">
#                                 <a href="#" id="go-back" hx-on:click="document.querySelector('dialog').close()">Cancel</a>
#                             </div>
#                         </div>
#                     </form>
#                 </dialog>
#                 """
#             result = ssid_collection + dialog

#         return '<div id="wifi-list">{0}</div>'.format(result)
    
    
#     def wifi_connect(self, ssid, password):
#         print('Trying to connect to:', ssid)
        
#         self.wifi_connection.connect(ssid, password)
        
#         for _ in range(100):
#             if self.wifi_connection.isconnected():
#                 print('\nConnected! Network information:', self.wifi_connection.ifconfig())
#                 self.write_credentials(ssid, password)
#                 self.reset = True;
#                 self.ip = self.wifi_connection.ifconfig()[0]
#                 return True
#             else:
#                 print('.', end='')
#                 time.sleep_ms(100)
        
#         print('\nConnection failed!')
        
#         self.wifi_connection.disconnect()
        
#         return False
    
#     def write_credentials(self, ssid, password):
#         settingsFile = 'bedjet.json'
#         content = json.dumps({'ssid': ssid, 'password': password})
#         file = open(settingsFile, 'w')
#         file.write(content)
#         file.close()
