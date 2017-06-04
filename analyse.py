#!/usr/bin/env python3

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(dbname="news")


def mostPopularArticles():
    """
    :return: a list of the most 3 popular articles
    """
    db = connect()
    c = db.cursor()
    c.execute("""SELECT '"' || title || '"',
                 count(log.path) || ' views' as num FROM
                 articles, log
                 WHERE log.path LIKE concat('%',articles.slug,'%')
                 GROUP BY title
                 ORDER BY num DESC
                 LIMIT 3""")
    result = c.fetchall()
    db.close()
    return result


def mostPopularAuthors():
    """
    :return: a list of the most popular authors sorted descending
    """
    db = connect()
    c = db.cursor()
    c.execute("""SELECT authors.name, count(log.path)|| ' views' as num
                 FROM articles, log, authors
                 WHERE log.path LIKE concat('%',articles.slug,'%') AND
                 articles.author = authors.id
                 GROUP BY authors.name
                 ORDER BY num DESC""")
    result = c.fetchall()
    db.close()
    return result


def requestsError():
    """
    :return: a list of days when more than 1% of requests lead to errors
    """
    db = connect()
    c = db.cursor()
    c.execute("""SELECT errors.time,
                 round((error::DECIMAL/total)*100.0, 1)|| '% errors' as percent
                 FROM errors
                 WHERE (error::DECIMAL/total)*100.0 > 1.0""")
    result = c.fetchall()
    db.close()
    return result


if __name__ == '__main__':
    while True:
        q = input("What answer do you want?\n"
                  "* enter a numerical value(1, 2 or 3).\n"
                  "1. What are the most popular three articles of all time?\n"
                  "2. Who are the most popular article authors of all time?\n"
                  "3. On which days did more than 1% of requests"
                  " lead to errors?\n")
        if q == '1':
            res = mostPopularArticles()
            break
        elif q == '2':
            res = mostPopularAuthors()
            break
        elif q == '3':
            res = requestsError()
            break
        else:
            print("invalid input please choose again.")

    for item in res:
        print(str(item[0])+' -- '+item[1])
