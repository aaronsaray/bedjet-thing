from bedjet_thing.microdot import Microdot, send_file
from bedjet_thing.debug import Debug

class App:
    def __init__(self):
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
            with open('web/htmx/initial-load.html') as f:
                replacedText = f.read().replace('{{wifi-list}}', 'There are no wifi networks available.')
                return replacedText, 200;

        app.run(debug=True, port=80)
