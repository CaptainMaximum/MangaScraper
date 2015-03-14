YAML_FILE=$1

output=$(python yaml_parser.py $YAML_FILE)
errcode=$?
eval $(echo $output)

if [ ! $errcode -eq 0 ] # Test error code, we want it to be zero
  then
  echo $error
  exit -1
fi

echo "Getting comic page"
#main_page=$(curl -s $URL)
echo "Comic page obtained"
for i in $VOLS
do
  x=$(eval echo $(echo $i))
  # pull out everything inside of the stars
  volname=$(echo $x | sed -r "s/\*(.+)\*.*/\1/")
  # pull out everything after the stars
  chaplist=$(echo $x | sed -r "s/\*.+\*(.+)/\1/")
  echo $volname
  echo $chaplist

done