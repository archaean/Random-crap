drop table classes_csv;


create table classes_csv (class VARCHAR(50), relation VARCHAR(20), 
                          value VARCHAR(50), modifier VARCHAR(50));
                          
truncate table classes_csv;

--MySQL script for loading csv file
--load has to be run from console?
--$ mysql -u [username] -p --local-infile
--mysql> use warhammer
load data local infile 'classes.csv' into table classes_csv fields 
terminated by ','
enclosed by '"'
lines terminated by '\n';

select * from classes_csv;

select distinct class from classes_csv order by class;
select distinct relation from classes_csv order by relation;
select distinct value from classes_csv where relation like '%Skills%' order by value;
select distinct value from classes_csv where relation like '%Career Exits%' order by value;
