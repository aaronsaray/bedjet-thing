import machine
import asyncio
from bedjet_thing.microdot import Microdot, send_file
from bedjet_thing.debug import Debug

class App:
    reset_device = False
    clear_config = False

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
                self.reset_device = True

                with open('web/htmx-templates/wifi-auth-success.html') as f:
                    content = f.read()
                    f.close()

                content = content.format(ssid, self.wifi.ip)
            else:
                with open('web/htmx-templates/wifi-auth-failure.html') as f:
                    content = f.read()
                    f.close()

            return content
        
        @app.post('/htmx/connect-to-bluetooth')
        async def connect_to_bluetooth(request):

### This is failing - if successful, it writes. If failure, it hangs. Either way, after the response is returned, nothing else works correctly
### Think it has to do with the double await

############################################################################################################################### HELP???? ######################################################
# It seems to 'work', the file is written, but then it doesn't serve anything after being refreshed (44b files are served... or just pending)
# obviously this has something to do with me not understanding async yet in python
# Perhaps I should just issue a machine.reset()?
############################################################################################################################### HELP???? ######################################################

            if await self.bluetooth.provision():
                with open('web/htmx-templates/bluetooth-provision-success.html') as f:
                    content = f.read()
                    f.close()

                content = content, 200, {'Connection': 'close'}
            else:
                with open('web/htmx-templates/bluetooth-provision-failure.html') as f:
                    content = f.read()
                    f.close()

            return content

        @app.delete('/htmx/reset')
        async def reset_device(request):
            self.reset_device = True
            self.clear_config = True

            with open('web/htmx-templates/reset-notification.html') as f:
                content = f.read()
                f.close()
        
            return content, 200;

        @app.after_request
        async def after_request_handler(request, response):
            if self.reset_device:
                async def worker(): 
                    Debug.log('Clearing and restarting after 3 seconds...')
                    await asyncio.sleep(3)
                    if self.clear_config:
                        self.config.clear()
                    machine.reset()
                
                loop = asyncio.get_event_loop()
                task = loop.create_task(worker())

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
            f.close()
        
        return content, 200;

    def output_bluetooth_functionality(self):
        has_connected = True
        fan_on = False
        bedjet_name = 'BEDJETAX355'
        bedjet_temp = '72'

        if has_connected:
            with open('web/htmx-templates/bluetooth-connected.html') as f:
                content = f.read()
                f.close()
            content = content.replace('<!--fanon-->', 'checked' if fan_on else '').replace('<!--bedjetname-->', bedjet_name).replace('<!--ambientf-->', bedjet_temp)
        else:
            with open('web/htmx-templates/bluetooth-not-connected.html') as f:
                content = f.read()
                f.close()
        
        return content, 200;
