LOCALE_DIR=invoice_generator/locale
POT_DIR=$LOCALE_DIR/en
POT_DOMAIN=django


get_pot_file() {
    echo $LOCALE_DIR/$1/LC_MESSAGES/$POT_DOMAIN.po
}


get_langs() {
    find $LOCALE_DIR -mindepth 1 -maxdepth 1 -type d ! -path "$POT_DIR" -printf "%f\n"
}
