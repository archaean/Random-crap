Random-crap
===========

Make the config:
$ cat warhammer.ini.example > warhammer.ini

Simple load the data:
$ python load_csv.py -c warhammer.ini -d sqlite

Simple generate the classes dot:
$ python gen_class_dot.py -c warhammer.ini -d sqlite

*Open it up in graphviz*
