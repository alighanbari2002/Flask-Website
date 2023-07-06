cls
set FLASK_APP=server
start cmd /k python -m flask run
@REM explorer http://127.0.0.1:5000
start firefox http://127.0.0.1:5000
