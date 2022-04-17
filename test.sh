#!/bin/sh

echo -e "\033[0;34mRunning Flake8 Linter...\033[0m"

FLAKE=`flake8 --ignore=W191 app/`
FLAKE_CODE=`echo $?`

if [ "$FLAKE_CODE" -ne "0" ]; then
	echo -e "\033[0;31mFlake8 errors:\033[0m"
	echo -e "$FLAKE"
else
	echo -e "\033[0;32mFlake8 successfull!\033[0m"
fi


echo -e "\n\033[0;34mRunning tests...\033[0m"

PYTEST=`pytest --color=yes --no-header app/*`
PYTEST_CODE=`echo $?`

if [ "$PYTEST_CODE" -ne "0" ]; then
	echo -e "\033[0;31mTest errors:\033[0m"
	echo -e "$PYTEST"
else
	echo -e "\033[0;32mTests successfull!\033[0m"
fi

if [ "$FLAKE_CODE" -ne "0" -o "$PYTEST_CODE" -ne "0" ]; then
	exit 1
fi

exit 0
