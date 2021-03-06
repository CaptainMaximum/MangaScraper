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
  mkdir "$NAME"
  mkdir "$NAME/volumes"
fi

echo "Getting comic page"
#main_page=$(curl -s $URL)
main_page=$(cat tests/test_files/Nisekoi.html)
echo "Comic page obtained"
#echo $main_page | python is_page_valid.py
for i in $VOLS
do
  # Oh god this line.  So what this does is takes the string representation of
  # a volume variable (e.g. 'V1') and gives the chapter list associated with it
  # (e.g. '*V1* 1 2 3 4')
  x=$(eval echo $(echo $i))
  # pull out everything inside of the stars
  volname=$(echo $x | sed -r "s/@(.+)@.*/\1/")
  voldir=$(echo $volname | sed -r "s/ //g")
  echo "Volume name:"
  echo $volname
  # pull out everything after the stars
  chaplist=$(echo $x | sed -r "s/@.+@(.+)/\1/")
  output=$(echo $main_page | python chapter_link_extractor.py "$chaplist")
  eval $(echo $output)
  if [[ ! -e "$NAME/$voldir" ]]
    then
    mkdir "$NAME/$voldir"
    mkdir "$NAME/$voldir/chapters"
  fi

  for j in $CHAPTERS
  do
    chapname=$(echo $j | sed -r "s/.+chapter=([^&]+)&.+/\1/")
    echo $chapname
    chap=$(curl -s $j)
    pics=$(echo $chap | python chapter_picture_extractor.py)
    if [[ -e "$NAME/$voldir/$chapname" ]]
      then
      rm "$NAME/$voldir/$chapname/"*
    fi

    if [[ ! -e "$NAME/$voldir/$chapname" ]]
      then
      mkdir "$NAME/$voldir/$chapname"
    fi

    for pic in $pics
    do
      filename=$(echo $pic | sed -r "s/.+\/([0-9\.]+-[0-9]+).png/\1.jpg/")
      curl $pic -s -o "$NAME/$voldir/$chapname/$filename" &
    done
    wait
    convert "$NAME/$voldir/$chapname/*.jpg" "$NAME/$voldir/chapters/$chapname".pdf
  done
    pdftk $(find "$NAME/$voldir/chapters/"* | sort -V) cat output "$NAME/volumes/$volname".pdf

done