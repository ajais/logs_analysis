#!/usr/bin/env python3
#
# Script generates an analysis of the logs for the newspaper website.

import psycopg2


def get_pop_articles():
    """ Joins the articles and log tables from the news database to count 
    the number of times each article is displayed and find the 3 most popular. 
    The articles are identified with a unique slug that also appears in the path 
    displayed in the log table. As a result the path can be formatted 
    to match the slug and do the join that way.
    """
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
    """ Joins the authors, articles and log tables from the news database to count 
    the total number of reads per author and rank them. We proceed the same way to 
    join the log and articles table which will give us reads and instead of grouping 
    by article title, we group everything by author.
    """
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
    """ Here we leverage the avg method to generate the occurence of errors 
    for each day as a percentage. And then use it in a subquery to then find 
    the days where the occurence of errors is superior than 1%.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select error_table.* \
              from (select date(time), \
              avg(case when status = '200 OK' then 0 else 1 end) as error \
              from log \
              group by date(time)) as error_table \
              where error >= 0.01")
    POSTS = c.fetchall()
    db.close()
    return POSTS

# Create an output file or overwrite the last created one
f = open("output.txt", "w")

# Output the most popular articles
f.write('3 most popular articles of all time:\n')
print('3 most popular articles of all time:\n')
pop_art = get_pop_articles()
for i in pop_art:
    f.write('"{}" -- {} views\n'.format(i[0], i[1]))
    print('"{}" -- {} views\n'.format(i[0], i[1]))
f.write('\n')
print('\n')

# Output the most popular authors
f.write('Most popular authors of all time:\n')
print('Most popular authors of all time:\n')
pop_auth = get_pop_authors()
for i in pop_auth:
    f.write('{} -- {} views\n'.format(i[0], i[1]))
    print('{} -- {} views\n'.format(i[0], i[1]))
f.write('\n')
print('\n')

# Output the days with more than 1% errors
f.write('Days where more than 1% of requests lead to errors:\n')
print('Days where more than 1% of requests lead to errors:\n')
days_err = get_days_errors()
for i in days_err:
    f.write('{} -- {}% errors\n'.format(i[0].strftime('%B %d, %Y'),
                                        '{0:.1f}'.format(i[1]*100)))
    print('{} -- {}% errors\n'.format(i[0].strftime('%B %d, %Y'),
                                      '{0:.1f}'.format(i[1]*100)))

f.close()
