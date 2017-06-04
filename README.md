# Logs Analysis Project

this program analyse a logs of a newspaper site and give some useful information about the website.

## How to use

1. you need to have python3 on your machine and postgresql DBMS.
2. you should create `news` database and relevant tables.
3. create error view as mentioned below.
4. open the terminal and move to where the program located.
5. run `python analyse.py` then choose the number of question you want it's answer.
6. `output.txt` file contians simple of interactive with the program.

## View

create this view via psql command before running the program

``` sql
CREATE VIEW errors AS
SELECT log.time::DATE, count(status) total,
sum(case when status != '200 OK' then 1 else 0 end) error
FROM log
GROUP BY log.time::DATE;
```
