import requests
from datetime import datetime
from flask import Flask, render_template, request

class APIStatusChecker:
    @staticmethod
    def check_api_status(api_url):
        try:
            response = requests.get(api_url)
            response_code = response.status_code
            is_alive = response.ok
        except requests.exceptions.RequestException:
            response_code = 404  
            is_alive = False
        
        if not is_alive:
            response_code = 404  

        return {
            "QueriedAt": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "ResponseCode": response_code,
            "IsAlive": is_alive
        }

class APIStatusApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.api_status_checker = APIStatusChecker()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def check_api():
            result = None
            if request.method == 'POST':
                api_url = request.form.get('url')
                if api_url:
                    result = self.api_status_checker.check_api_status(api_url)
            
            return render_template('index.html', result=result)

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app_instance = APIStatusApp()
    app_instance.run()
