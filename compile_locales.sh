HERE=$(dirname $0)
. $HERE/locale_utils.sh


compile_langs() {
    pybabel compile -f -D $POT_DOMAIN -d $LOCALE_DIR
}


main() {
    cd $HERE
    compile_langs
}

main
