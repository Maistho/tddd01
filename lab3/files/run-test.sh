#Sparar predicerade taggar till predicted-train.conll
python3.4 ../tagger/lab2.py tag ../tagger/suc.model ../data/talbanken-dep-train.conll ../data/predicted-train.conll

#Sparar predicerade taggar till predicted-test.conll
python3.4 ../tagger/lab2.py tag ../tagger/suc.model ../data/talbanken-dep-test.conll ../data/predicted-test.conll

#Tränar på guldstandard
java -jar ../maltparser-1.8.1/maltparser-1.8.1.jar -c gold -i ../data/talbanken-dep-train.conll -m learn

#Parsar testdata med modell från guldstandard
java -jar ../maltparser-1.8.1/maltparser-1.8.1.jar -c gold -i ../data/predicted-test.conll -m parse -o gold.conll

#Tränar på predicerade taggar
java -jar ../maltparser-1.8.1/maltparser-1.8.1.jar -c predicted -i ../data/predicted-train.conll -m learn

#Parsar testdata med modell från predicerade taggar
java -jar ../maltparser-1.8.1/maltparser-1.8.1.jar -c predicted -i ../data/predicted-test.conll -m parse -o predicted.conll

#Utvärderar resultat från guld
python3.4 ../code/lab3.py evaluate ../data/talbanken-dep-test.conll gold.conll

#Utvärderar resultat från predicerat
python3.4 ../code/lab3.py evaluate ../data/talbanken-dep-test.conll predicted.conll
