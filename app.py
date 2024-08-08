from flask import Flask
from api.retrieval import retrieval_blueprint
from api.generation import generation_blueprint
from config import config

app = Flask(__name__)
app.config.from_object(config)

# Register the blueprints
app.register_blueprint(retrieval_blueprint, url_prefix="/api")
app.register_blueprint(generation_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
