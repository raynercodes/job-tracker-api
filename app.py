from flask import Flask, request
from routes.auth_routes import auth_bp
from routes.company_routes import company_bp
from routes.application_routes import applications_bp
from utils.responses import error_response
from utils.logger import logger

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(company_bp)
app.register_blueprint(applications_bp)

@app.before_request
def log_request():
    logger.info(f"Request started method={request.method} path={request.path}")

@app.errorhandler(ValueError)
def handle_value_error(e):
    logger.warning(f"ValueError path={request.path} error={str(e)}")
    return error_response(str(e), status=400)

@app.errorhandler(Exception)
def handle_internal_error(e):
    logger.exception(f"Unexpected error path={request.path}")
    return error_response(str(e), status=500)



if __name__ == "__main__":
    app.run(debug=True)