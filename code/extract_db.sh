for table in $(cat ../conf/all_datasets.txt); do
    sqlite3 -header -tsv ../results/m4efad.db "SELECT * FROM ${table};" > ../results/${table}.tsv
done

for table in $(cat ../conf/datasets.txt); do
    sqlite3 -header -csv ../results/m4efad.db "separator '\t'; SELECT * FROM ${table};" > ../results/${table}.tsv
done
  separator '\t'; SELECT * FROM wolkes;
  ^--- error here

