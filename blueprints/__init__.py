# app.py
from flask import Flask, request
import json, config, os
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
app.config["APP_DEBUG"] = True

cors=CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)

app.config["JWT_SECRET_KEY"] = "yopiragil"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

jwt = JWTManager(app)


def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        print(claims["id"])
        if claims["status"] == "user":
            return {"status": "FORBIDEN", "message": "Internal Only!"}, 403
        else:
            return fn(*args, **kwargs)

    return wrapper


if os.environ.get("FLASK_ENV", "Production") == "Production":
    app.config.from_object(config.ProductionConfig)
elif os.environ.get("FLASK_ENV", "Production") == "Test":
    app.config.from_object(config.TestConfig)
else:
    app.config.from_object(config.DevelopmentConfig)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else :
        #ternyata cors pake method options di awal buat ngecek CORS dan harus di return kosong 200, jadi di akalin gini deh. :D
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods':'*'}

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning(
            "REQUEST_LOG\t%s",
            json.dumps(
                {
                    "method": request.method,
                    "code": response.status,
                    "url": request.full_path,
                    "request": requestData,
                    "response": json.loads(response.data.decode("utf-8")),
                }
            ),
        )

    else:
        app.logger.error("")
    return response



from blueprints.user.resources import bp_user
from blueprints.auth import bp_auth
from blueprints.order.resources import bp_order

app.register_blueprint(bp_user, url_prefix="/user")
app.register_blueprint(bp_auth, url_prefix="/auth")
app.register_blueprint(bp_order, url_prefix="/order")



db.create_all()
