from bedjet_thing.microdot import Microdot, send_file
from bedjet_thing.debug import Debug

class App:
    def __init__(self, config, wifi):
        self.config = config
        self.wifi = wifi

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
            if self.wifi.connected_to_wifi:
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
            content = """
                <div id="panel-header">
                    <div>
                        Make sure your BedJet is on and within range.
                    </div>
                </div>
                <div>
                    <button id="bluetooth-connect-button" hx-post="/htmx/connect-to-bluetooth" hx-target="#panel" hx-indicator="#bluetooth-connect-button">Connect to BedJet</button>
                </div>
                <div class="error-message">
                    Unable to connect to BedJet. Is it it on? Within range? A BedJet 3? Not Broken? Have you done a rain dance?
                </div>
            """
            return content

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
