TOTAL=0
PASSED=0

FILES=$( find . -name "*.py")

for file in $FILES
do
    ((++TOTAL))
    mypy $file --ignore-missing-imports
    if [ $? != 0 ]
    then
	echo "$file failed typecheck!"
    else
	((++PASSED))
	echo "$file passed!"
    fi
    echo "--------------------------------------"
done

echo "Typecheck $PASSED/$TOTAL files passed"
