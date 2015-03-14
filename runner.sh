YAML_FILE=$1
CLEAN=$2


output=$(python yaml_parser.py $YAML_FILE)

errcode=$?
eval $(echo $output)
if [ ! $errcode -eq 0 ] # Test error code, we want it to be zero
  then
  echo $error
  exit -1
fi

if [ "$CLEAN" == "clean" ]
  then
  rm -r $NAME
  exit 0
fi

if [ ! -e $NAME ]
  then
  mkdir $NAME
fi

echo "Getting comic page"
#main_page=$(curl -s $URL)
main_page=$(cat tests/test_files/Nisekoi.html)
echo "Comic page obtained"
for i in $VOLS
do
  # Oh god this line.  So what this does is takes the string representation of
  # a volume variable (e.g. 'V1') and gives the chapter list associated with it
  # (e.g. '*V1* 1 2 3 4')
  x=$(eval echo $(echo $i))
  # pull out everything inside of the stars
  volname=$(echo $x | sed -r "s/\*(.+)\*.*/\1/")
  # pull out everything after the stars
  chaplist=$(echo $x | sed -r "s/\*.+\*(.+)/\1/")
  echo $main_page | python chapter_link_extractor.py "$chaplist"

done