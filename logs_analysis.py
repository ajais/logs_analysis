#!/usr/bin/env python3
#
# Script generates an analysis of the logs for the newspaper website.

import psycopg2


def get_pop_articles():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select title, count(*) \
              from articles, log \
              where slug=replace(path,'/article/','') \
              and path != '/' \
              group by title \
              order by count(*) desc \
              limit 3")
    POSTS = c.fetchall()
    db.close()
    return POSTS


def get_pop_authors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select name, count(*) \
              from articles, log, authors \
              where authors.id=articles.author \
              and slug=replace(path,'/article/','') \
              and path != '/' \
              group by name \
              order by count(*) desc \
              limit 4")
    POSTS = c.fetchall()
    db.close()
    return POSTS


def get_days_errors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select error_table.* \
              from (select date(time), \
              avg(case when status = '200 OK' then 0 else 1 end) as error \
              from log group by date(time)) as error_table \
              where error >= 0.01")
    POSTS = c.fetchall()
    db.close()
    return POSTS

f = open("output.txt", "w")


f.write('3 most popular articles of all time:\n')
print('3 most popular articles of all time:\n')
pop_art = get_pop_articles()
for i in pop_art:
    f.write('"{}" -- {} views\n'.format(i[0], i[1]))
    print('"{}" -- {} views\n'.format(i[0], i[1]))
f.write('\n')
print('\n')

f.write('Most popular authors of all time:\n')
print('Most popular authors of all time:\n')
pop_auth = get_pop_authors()
for i in pop_auth:
    f.write('{} -- {} views\n'.format(i[0], i[1]))
    print('{} -- {} views\n'.format(i[0], i[1]))
f.write('\n')
print('\n')

f.write('Days where more than 1% of requests lead to errors:\n')
print('Days where more than 1% of requests lead to errors:\n')
days_err = get_days_errors()
for i in days_err:
    f.write('{} -- {}% errors\n'.format(i[0].strftime('%B %d, %Y'),
                                        '{0:.1f}'.format(i[1]*100)))
    print('{} -- {}% errors\n'.format(i[0].strftime('%B %d, %Y'),
                                      '{0:.1f}'.format(i[1]*100)))

f.close()
