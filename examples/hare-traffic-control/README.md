Display a simple map showing airplanes in-flight

In order to run

You need to have a service account's credentials in your path, so run:

	export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service/account/credentials.json"

Then start data collection from the cloud, picking the beginning of your time period:

python htc.py 2019-06-01

Runs at:

	http://localhost:11156/

