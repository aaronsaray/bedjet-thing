from bedjet_thing.microdot import Microdot, send_file

class App:
    def __init__(self):
        self.start_microdot()

    def debug(self, message):
        print('DEBUG: ', end='')
        print(message)

    def start_microdot(self):
        self.debug('starting microdot')

        app = Microdot()

        @app.get('/')
        async def index(request):
            return send_file('web/index.html')

        app.run(debug=True, port=80)
