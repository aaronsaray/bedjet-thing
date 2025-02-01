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
            ssids = self.wifi.getAvailableSsids()

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

        app.run(debug=True, port=80)
