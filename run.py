#!/usr/bin/env python

from src.app import app

app.run(debug=app.config['DEBUG'], port=4900)
