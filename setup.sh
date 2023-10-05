python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py import_mln_xml ./static/editorial-redux-v5.xml