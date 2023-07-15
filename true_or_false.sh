#!/usr/bin/env bash

function main_menu {
    echo ""
    echo "0. Exit"
    echo "1. Play a game"
    echo "2. Display scores"
    echo "3. Reset scores"
    echo "Enter an option:"

    option=$(read -r option; echo "$option")
}

function login_user {
    curl --output ID_card.txt http://127.0.0.1:8000/download/file.txt >> /dev/null

    username=$(cat ID_card.txt | grep -oP '(?<="username": ")[^"]+')
    password=$(cat ID_card.txt | grep -oP '(?<="password": ")[^"]+')

    curl --cookie-jar cookie.txt --user "$username:$password" http://127.0.0.1:8000/login >> /dev/null
}

function save_score {
    if [ ! -f scores.txt ]; then
        touch scores.txt
    fi

    echo "User: $1, Score: $2, Date: $(date +'%Y-%m-%d')" >> scores.txt
}

function play_game {
    login_user

    echo "What is your name?"
    name=$(read -r name; echo "$name")
    answers=0
    playing=true

    while $playing; do
        question=$(curl --silent --cookie cookie.txt http://127.0.0.1:8000/game)

        echo ""
        echo $(echo $question | grep -oP '(?<="question": ")[^"]+')
        echo "True or False?"

        answer=$(read -r answer; echo "$answer")
        correct_answer=$(echo $question | grep -oP '(?<="answer": ")[^"]+')

        if [ "$answer" == "$correct_answer" ]; then
            echo "Awesome!"
            ((answers=answers + 1))
        else
            save_score $name $(($answers * 10))

            echo "Wrong answer, sorry!"
            echo "$name you have $answers correct answer(s)."
            echo "Your score is" $(($answers * 10)) "points."

            playing=false
        fi
    done
}

function display_scores {
    if [ -f scores.txt ]; then
        echo "Player scores"
        cat scores.txt
    else
        echo "File not found or no scores in it!"
    fi
}

function reset_scores {
    if [ -f scores.txt ]; then
        rm scores.txt
        echo "File deleted successfully!"
    else
        echo "File not found or no scores in it!"
    fi
}


echo "Welcome to the True or False Game!"

while true; do
    main_menu

    case $option in
        0)
            echo "See you later!"
            break
            ;;
        1)
            play_game
            ;;
        2)
            display_scores
            ;;
        3)
            reset_scores
            ;;
        *)
            echo "Invalid option!"
            ;;
    esac
done
