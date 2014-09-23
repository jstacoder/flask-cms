#!/bin/bash

export RESULT="$1";

if [ "$1" == "" ]; then
    export RESULT="new";
fi


echo $RESULT;
echo $2;


echo $@;
