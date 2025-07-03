"Project must be adapted for Chakiy business logic"
from flask import Flask
from flask_cors import CORS

import iam.application.services
from healthDehumidifier.interfaces.services import health_api
from iam.interfaces.services import iam_api
from routines.interfaces.services import routine_api
from shared.infrastructure.database import init_db

app = Flask(__name__)

# Configure CORS to allow requests from the frontend
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
     allow_headers=["Content-Type", "X-API-Key", "Accept"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

app.register_blueprint(iam_api)
app.register_blueprint(health_api)
app.register_blueprint(routine_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()
        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()

if __name__ == "__main__":
    app.run(debug=True)
