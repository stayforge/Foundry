import os

from os import environ as env
from dotenv import load_dotenv
from app import create_app
from authlib.integrations.flask_client import OAuth

load_dotenv()

config=os.getenv('FLASK_ENV') or 'development'

app = create_app(config)
app.secret_key = env.get("APP_SECRET_KEY")

oauth=OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

if __name__ == "__main__":
    if config == 'development':
        app.run(host='0.0.0.0', port=5987, debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5987, app)
