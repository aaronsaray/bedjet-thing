from bedjet_thing.microdot import Microdot, send_file
from bedjet_thing.debug import Debug

class App:
    def __init__(self, wifi):
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
        async def get_favicon(request, path):
            return send_file('web/favicon.ico', max_age=86400)

        @app.get('/assets/<path:path>')
        async def get_asset(request, path):
            if '..' in path:
                return 'Not found', 404
            return send_file('web/assets/' + path, max_age=86400)

        @app.get('/htmx/initial-load.html')
        async def get_initial_load(request):
            ssids = self.wifi.get_available_ssids()

            listOfSsids = ''
            if len(ssids) == 0:
                listOfSsids = '<div style="text-align: center; font-weight: bold; color: red">No WiFi is within range or discoverable.</div>'
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

            with open('web/htmx/initial-load.html') as f:
                replacedText = f.read().replace('<!--wifi-list-->', listOfSsids)
                return replacedText, 200;

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

        app.run(debug=True, port=80)
