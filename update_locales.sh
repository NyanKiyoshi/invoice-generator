HERE=$(dirname $0)
. $HERE/locale_utils.sh


extract() {
    pybabel -v extract -F babel.cfg -o $(get_pot_file en) invoice_generator
}


update() {
    lang=$1
    echo updating $lang
    pybabel update -l $lang -o $(get_pot_file $lang) -i $(get_pot_file en)
}


update_langs() {
    for lang in $@; do
        update $lang
    done
}


main() {
    cd $HERE
    langs=$(get_langs)
    extract && update_langs $langs
}

main
