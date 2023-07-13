#!/usr/bin/env bash

function save_and_echo {
    echo $1
    echo "$1" >> operation_history.txt
}
input=""
results=""

save_and_echo "Welcome to the basic calculator!"

while true; do
    save_and_echo "Enter an arithmetic operation or type 'quit' to quit:"

    input=$(read -r input; echo "$input")
    echo "$input" >> operation_history.txt

    if [ "$input" == "quit" ]; then
        save_and_echo "Goodbye!"
        break
    elif [[ $input =~ ^-?([0-9]+|[0-9]+.[0-9]+)\ [+\-\/*^]\ -?([0-9]+|[0-9]+.[0-9]+)$ ]]; then
        results=$(echo "scale=2;$input" | bc -l)
        save_and_echo $results
    else
        save_and_echo "Operation check failed!"
    fi
done
