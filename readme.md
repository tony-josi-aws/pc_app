## PC App

PC app to communicate with the device.
### Using virtual enviorment (venv)

Create: `python -m venv <project_name>`

Activate: 

* Windows: `<project_name>/Scripts/activate.bat`
* Linux:   `source <venv>/bin/activate`

Install required python modules from `requirements.txt`: `pip install -r requirements.txt`


#### Run CLI and test command echo
Start simple echo server: 

`python src\server.py`

Start CLI: 

`python src\cli.py`

Connect to server:

`connect 127.0.0.1 20001`

Send commands:

`send <command>`


Deactivate venv: `deactivate`

