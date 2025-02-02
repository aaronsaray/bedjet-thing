import machine
from bedjet_thing.microdot import Microdot, send_file
from bedjet_thing.debug import Debug

class App:
    reset_device = False

    def __init__(self, config, wifi, bluetooth):
        self.config = config
        self.wifi = wifi
        self.bluetooth = bluetooth

        # must be the last thing
        self.start_microdot()

    def start_microdot(self):
        Debug.log('Starting microdot')

        app = Microdot()

        @app.get('/')
        async def index(request):
            return send_file('web/index.html')

        @app.get('/favicon.ico')
        async def get_favicon(request):
            return send_file('web/favicon.ico', max_age=86400)

        @app.get('/assets/<path:path>')
        async def get_asset(request, path):
            if '..' in path:
                return 'Not found', 404
            return send_file('web/assets/' + path, max_age=86400)

        @app.get('/htmx/initial-load')
        async def get_initial_load(request):
            
            Debug.log('Initial load debug')
            Debug(self.config)
            Debug(self.config.has_bluetooth)
            Debug.log('Initial load debug end')

            if self.config.has_bluetooth:
                return self.output_bluetooth_functionality()
            elif self.config.has_wifi:
                return self.output_bluetooth_connect()
            else:
                return self.output_wifi_list()

        @app.post('/htmx/wifi-auth')
        async def post_wifi_auth(request):
            ssid = request.form.get('ssid')
            password = request.form.get('password')
            Debug.log('Attempting authentication to ' + ssid + ' with password ' + password)

            if self.wifi.provision(ssid, password):
                request.g.restart = True

                content = """
                    <script>
                        alert("Success fully connected to wifi {0}. You will be redirected to the device on your network now.");
                        window.location.href='http://{1}';
                    </script>
                """.format(ssid, self.wifi.ip)
            else:
                content = """
                    <script>
                        alert('Unable to connect to this wifi connection with this password.');
                        document.querySelector('#password').value = '';
                    </script>
                """

            return content
        
        @app.post('/htmx/connect-to-bluetooth')
        async def connect_to_bluetooth(request):

############################################################################################################################### HELP???? ######################################################
# It seems to 'work', the file is written, but then it doesn't serve anything after being refreshed (44b files are served... or just pending)
# obviously this has something to do with me not understanding async yet in python
# Perhaps I should just issue a machine.reset()?
############################################################################################################################### HELP???? ######################################################

            if await self.bluetooth.provision():
                content = """
                    <div>
                        Please wait...
                    </div>
                    <script>
                        alert("Successfully connected to BedJet. Reloading BedJetThing");
                        window.location.reload();
                    </script>
                """, 200, {'Connection': 'close'}
            else:
                content = """
                    <div id="panel-header">
                        <div>
                            Make sure your BedJet is on and within range.
                        </div>
                    </div>
                    <div>
                        <button onclick="document.querySelector('.error-message').style.display='none'" id="bluetooth-connect-button" hx-post="/htmx/connect-to-bluetooth" hx-target="#panel" hx-indicator="#bluetooth-connect-button">Connect to BedJet</button>
                    </div>
                    <div class="error-message">
                        Unable to connect to BedJet. Is it it on? Within range? A BedJet 3? Not Broken? Have you done a rain dance?<br>
                        Also remember that if you have another BT device connected, it must be disconnected.
                    </div>
                """

            return content

        @app.delete('/htmx/reset')
        async def reset_device(request):
            self.reset_device = True
            self.config.clear()

            with open('web/htmx-templates/reset-notification.html') as f:
                content = f.read()
        
            return content, 200;

        @app.after_request
        def after_request_handler(request, response):
            if self.reset_device:
                Debug.log('Restarting...')
                machine.reset()

        app.run(debug=True, port=80)

    def output_wifi_list(self):
        ssids = self.wifi.get_available_ssids()

        listOfSsids = ''
        if len(ssids) == 0:
            listOfSsids = '<div class="error-message">No WiFi is within range or discoverable.</div>'
        else:
            def toHtml(ssid):
                return """
                    <a href="#" hx-on:click="
                        document.querySelector('#ssid').value = '{0}';
                        document.querySelector('dialog').showModal();
                    ">
                        {0}
                    </a>
                    """.format(ssid.replace("'", "&quot;"))
            listOfSsids = ''.join(map(toHtml, ssids))
            listOfSsids += """
                <dialog>
                    <form hx-post="/htmx/wifi-auth" hx-indicator="#wifi-auth-button" hx-target="#wifi-response">
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
                        <div id="wifi-response"></div>
                    </form>
                </dialog>
            """

        with open('web/htmx-templates/wifi-list.html') as f:
            replacedText = f.read().replace('<!--wifi-list-->', listOfSsids)
        return replacedText, 200;

    def output_bluetooth_connect(self):
        with open('web/htmx-templates/bluetooth-connect.html') as f:
            content = f.read()
        
        return content, 200;

    def output_bluetooth_functionality(self):
        with open('web/htmx-templates/bluetooth-connected.html') as f:
            content = f.read()
        
        return content, 200;
