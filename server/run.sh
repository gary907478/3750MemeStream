#!/bin/bash

echo "Running..."

CONTINUE=1
while [ "$CONTINUE" -ne 0 ]; do
  sleep 1
  echo "connecting"
  mysql -h db.memestream -u root --password=notwaterloo -e "SELECT * FROM ACCOUNT_INFO;" memestreamdb
  CONTINUE=$?
done

FLASK_APP=serverRun.py flask run --host='0.0.0.0' --port=8080

while true; do
  sleep 1
  ping db.memestream
  echo "sleeping"
done

echo "done"
