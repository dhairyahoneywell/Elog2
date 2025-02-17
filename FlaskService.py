from threading import Thread

import win32event
import win32service
import win32serviceutil
from flask import Flask, jsonify, request


class FlaskAppService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask App Service"
    _svc_description_ = "A simple Flask API running as a Windows Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.flask_app = Flask(__name__)

        # Hard-coded JSON data
        self.data = {"message": "Hello, World!", "status": "success"}

        # Define Flask routes
        @self.flask_app.route("/", methods=["GET", "POST"])
        def hello_world():
            return "Hello, World!"

        @self.flask_app.route("/api/data", methods=["GET"])
        def get_data():
            return jsonify(self.data)

        @self.flask_app.route("/api/data", methods=["POST"])
        def post_data():
            new_data = request.get_json()
            return jsonify(new_data), 201

        self.thread = Thread(target=self.start_flask)
        self.thread.daemon = True

    def start_flask(self):
        self.flask_app.run(host="0.0.0.0", port=5091, debug=False)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        self.thread.start()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(FlaskAppService)
