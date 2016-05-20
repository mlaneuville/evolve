BASE_CONFIG=config.yaml

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters."
    echo "Usage: $0 folder run_name"
    exit
fi

FOLDER=$1
NAME=$2
NEW_CONFIG=config_$NAME.yaml

if [ -f $FOLDER/$NEW_CONFIG ]; then
    echo "Warning: file already exists, overwrite? [y/n]"
    read overwrite
    if [ $overwrite != "y" ]; then
        exit
    fi
fi

# create new config file
cmd="cp $BASE_CONFIG $NEW_CONFIG"
echo $cmd
$cmd

nline=`grep -in OutFolder $BASE_CONFIG | awk -F: '{print $1}'`
oldname=`grep -in OutFolder $BASE_CONFIG | awk '{print $3}' | awk -F"\"" '{print $2}'`
sed -i "${nline},${nline}s/$oldname/$FOLDER/g" $NEW_CONFIG

mkdir -p $FOLDER

./evolve $NAME
mv $NEW_CONFIG $FOLDER/$NEW_CONFIG
