from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime, timezone
import requests

from config.config import get_config_by_name
from initialize_functions import initialize_route,initialize_swagger

load_dotenv()


def create_app(config=None) -> Flask:
    """
    Create a Flask application.

    Args:
        config: The configuration object to use.

    Returns:
        A Flask application instance.
    """
    app = Flask(__name__)
    if config:
        app.config.from_object(get_config_by_name(config))

    # Initialize extensions
    # initialize_db(app)

    # Register blueprints
    initialize_route(app)

    # Initialize Swagger
    initialize_swagger(app)

    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}

    @app.route('/')
    def index():
        return render_template('access/index.html')

    @app.route('/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    def proxy(path):
        url = request.args.get('url', '')
        if not url:
            return jsonify({'error': 'URL parameter is required'}), 400
        
        # Get the environment from the request headers
        environment = request.headers.get('X-Environment', 'standard')
        
        # Construct the full URL
        full_url = f"{url}/{path}"
        
        # Handle OPTIONS request for CORS preflight
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Environment,Accept')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            return response
        
        try:
            # Forward the request method and headers
            headers = {
                'Content-Type': request.headers.get('Content-Type', 'application/json'),
                'X-Environment': environment,
                'Accept': request.headers.get('Accept', 'application/json')
            }
            
            # Forward the request body if present
            data = request.get_data() if request.get_data() else None
            
            # Log request details
            print(f"Proxying request to: {full_url}")
            print(f"Method: {request.method}")
            print(f"Headers: {headers}")
            print(f"Data: {data}")
            
            # Make the request to the target API
            response = requests.request(
                method=request.method,
                url=full_url,
                headers=headers,
                data=data,
                timeout=10
            )
            
            # Log response details
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response content: {response.content}")
            
            # Create the response with CORS headers
            proxy_response = make_response(response.content)
            proxy_response.headers.add('Access-Control-Allow-Origin', '*')
            proxy_response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Environment,Accept')
            proxy_response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            
            # Forward the status code
            proxy_response.status_code = response.status_code
            
            return proxy_response
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return jsonify({'error': str(e)}), 500
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    return app
