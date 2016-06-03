import sae
from papery import create_app

core_app = create_app()
application = sae.create_wsgi_app(core_app)
