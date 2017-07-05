#!/usr/bin/env python3
# 
# Script generates an analysis of the logs for the newspaper website.

import psycopg2

def get_pop_articles():
	db=psycopg2.connect("dbname=news")
	c = db.cursor()
	c.execute("select title, count(*) from articles, log where slug=replace(path,'/article/','') and path != '/' group by title order by count(*) desc limit 3")
	POSTS=c.fetchall()
	db.close()
	for line in POSTS:
		print(line)
	return POSTS

def get_pop_authors():
	db=psycopg2.connect("dbname=news")
	c = db.cursor()
	c.execute("select name, count(*) from articles, log, authors where authors.id=articles.author and slug=replace(path,'/article/','') and path != '/' group by name order by count(*) desc limit 4")
	POSTS=c.fetchall()
	db.close()
	for line in POSTS:
		print(line)
	return POSTS

def get_days_errors():
	db=psycopg2.connect("dbname=news")
	c = db.cursor()
	c.execute("select error_table.* from (select date(time), avg(case when status = '200 OK' then 0 else 1 end) as error from log group by date(time)) as error_table where error > 0.01")
	POSTS=c.fetchall()
	db.close()
	for line in POSTS:
		print(line)
	return POSTS


# select date(time), count(*) from log where status ='200 OK' group by date(time) order by date(time)
# select date(time), count(*) from log where status !='200 OK' group by date(time) order by date(time)
get_pop_articles()
print('\n')
get_pop_authors()
print('\n')
get_days_errors()