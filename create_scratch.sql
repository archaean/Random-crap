drop table classes_csv;


create table classes_csv (class VARCHAR(50), relation VARCHAR(20), 
                          value1 VARCHAR(50), modifier VARCHAR(50));
                          
truncate table classes_csv;

--load has to be run from console?
load data local infile 'classes.csv' into table classes_csv fields 
terminated by ','
enclosed by '"'
escaped by '//'
lines terminated by '\n';



select distinct class from classes_csv;
