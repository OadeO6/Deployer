from datetime import datetime
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

def create_app():
    """
    main app func
    """
    app = Flask(__name__)
    # CORS(app,  origins='*')
    # CORS(app,  resources={r"/*": {"origins":'*'}}, methods=['GET'])
    app.config.from_mapping(SECRET_KEY='dev')

    @app.template_filter()
    def format_datetime(value, format='medium'):
        if format == 'full':
            format="EEEE, d. MMMM y 'at' HH:mm"
        elif format == 'medium':
            format="EE dd.MM.y HH:mm"
        value = value.split(':')[0]
        return datetime.strptime(value, "%Y-%m-%d%H").strftime('%c')

    from web.views import auth_views, app_views, user_views

    app.register_blueprint(auth_views)
    app.register_blueprint(app_views)
    app.register_blueprint(user_views)


    app.url_map.strict_slashes = False

    return app
"""
def run_app():
    app = create_app()
    app.run(host='0.0.0.0', port='5000')
    """
