#! /usr/bin/env bash

function main_menu {
    echo ""
    echo "------------------------------"
    echo "| Hyper Commander            |"
    echo "| 0: Exit                    |"
    echo "| 1: OS info                 |"
    echo "| 2: User info               |"
    echo "| 3: File and Dir operations |"
    echo "| 4: Find Executables        |"
    echo "------------------------------"

    read -r option
}

function file_menu {
    echo ""
    echo "---------------------------------------------------"
    echo "| 0 Main menu | 'up' To parent | 'name' To select |"
    echo "---------------------------------------------------"

    read -r option
}

function edit_file {
    while true; do
        echo "---------------------------------------------------------------------"
        echo "| 0 Back | 1 Delete | 2 Rename | 3 Make writable | 4 Make read-only |"
        echo "---------------------------------------------------------------------"
    
        read -r option
    
        case $option in
            0)
                break
                ;;
            1)
                rm $1
                echo "$1 has been deleted."

                break
                ;;
            2)
                echo "Enter the new file name:"
                
                read -r new_name
                mv "$1" "$new_name"

                echo "$1 has been renamed as $new_name"

                break
                ;;
            3)
                chmod 666 "$1"
                echo "Permissions have been updated."
                ls -l "$1"
                break
                ;;
            4)
                chmod 664 "$1"
                echo "Permissions have been updated."
                ls -l "$1"
                break
                ;;
            *)
                ;;
        esac
    done
}

function file_and_dir_operations {
    while true; do
        echo ""
        echo "The list of files and directories:"

        arr=(*)
    
        for item in "${arr[@]}"; do
            if [[ -f "$item" ]]; then
                echo "F" "$item"
            elif [[ -d "$item" ]]; then
                echo "D" "$item"
            fi
        done

        file_menu
    
        case $option in
            0)
                break
                ;;
            'up')
                cd ..
                ;;
            *)
                if [ $(ls | grep -w "$option") ]; then
                    if [[ -f "$option" ]]; then
                        edit_file $option
                    elif [[ -d "$option" ]]; then
                        cd "$option"
                    fi
                else
                    echo "Invalid input!"
                fi
                ;;
        esac
    done
}

function find_executable {
    echo ""
    echo "Enter an executable name:"

    read -r name

    if [ $(which $name) ]; then
        echo ""
        echo "Located in: $(which $name)"
        echo ""
        echo "Enter arguments:"
    
        read -r arguments
    
        echo $($name $arguments)
    else
        echo ""
        echo "The executable with that name does not exist!"
    fi
}

echo "Hello $USER!"

while true; do
    main_menu

    case $option in
        0)
            echo "Farewell!"
            break
            ;;
        1)
            echo $(uname -o) $(uname -n)
            ;;
        2)
            whoami
            ;;
        3)
            file_and_dir_operations
            ;;
        4)
            find_executable
            ;;
        *)
            echo "Invalid option!"
            ;;
    esac
done
