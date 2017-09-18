# Use tabs before command, Makefiles don't work with spaces.
# If you really have nothing better to do, here you go:
# https://stackoverflow.com/q/2131213/4148708

dep_install:
	@echo 'Installing Python3 dependencies with pip3 for current user..'
	pip3 install --user -r requirements.txt 

run:
	@echo 'Starting Flask application..'
	source ./secrets.sh && /usr/bin/env python3 app.py

clean:
	@echo 'Cleaning up pycache..'
	-rm -rfv __pycache__
