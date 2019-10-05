Display a simple map showing airplanes in-flight

In order to run

You need to have a service account's credentials in your path, so run:

	export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service/account/credentials.json"

Then start data collection from the cloud, picking the beginning of your time period:

    python htc.py date [replay-speed]
    
    parameters:
     date: expects format yyyy-mm-dd, it is the date you want to replay (must be between june-2017 and june-2019)
     replay-speed: integer corresponding to the speed-up factor (ex: 2)

Runs at:

	http://localhost:11156/
Runs at:

	http://localhost:11156/

