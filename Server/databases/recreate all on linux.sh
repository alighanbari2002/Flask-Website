rm cure_packages.db
rm patients.db
rm supporters.db
rm users.db
python3 "initialize/cure_packages.db creator.py"
python3 "initialize/patients.db creator.py"
python3 "initialize/supporters.db creator.py"
python3 "initialize/users.db creator.py"
