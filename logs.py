#! /usr/bin/env python3

# Helper Class to hold query as well as title for the query
from logquery import LogQuery
import psycopg2

# Database Name - Provided by UDACITY
database_name = "news"

# First Query Object
q1 = LogQuery(
    "1. What are the most popular three articles of all time?",
    """
        SELECT articles.title, COUNT(*) AS views
        FROM articles INNER JOIN log on log.path
        LIKE CONCAT('%', articles.slug, '%')
        WHERE log.status LIKE '%200%'
        GROUP BY articles.title, log.path
        ORDER BY views DESC LIMIT 3
    """
    )

# Second Query Object
q2 = LogQuery(
    "2. Who are the most popular article authors of all time?",
    """
        SELECT authors.name, COUNT(*) AS views
        FROM authors INNER JOIN articles ON authors.id = articles.author
        INNER JOIN log ON log.path LIKE CONCAT('%', articles.slug, '%')
        WHERE log.status LIKE '%200%' GROUP BY authors.name
        ORDER BY views DESC
    """
    )

# Third Query Object
q3 = LogQuery(
    "3. On which days did more than 1 % of requests lead to errors?",
    """
        SELECT day, percentage FROM (
        SELECT day, ROUND((SUM(req) / (SELECT COUNT(*)
        FROM log WHERE log.time::timestamp::date = day) * 100), 2) AS
        percentage FROM (SELECT log.time::timestamp::date AS day, COUNT(*)
        AS req FROM log WHERE status LIKE '%404%' GROUP BY day) AS perc_log
        GROUP BY day ORDER BY percentage DESC) AS main WHERE percentage >= 1
    """
    )


# Helper function to establish database connection, and return db and cursor
def connect():
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except Exception as e:
        print ("Cannot connect to database\n" + str(e))


# Function to query the database and return the unformatted result
def execute_query(query):
    db, cursor = connect()
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    return res


# Function to display the result in appropriate formatting
def display_query_results(query_title, query_result, suffix=" views"):
    print (query_title)
    for result in query_result:
        print("\t-> " + str(result[0]) + " - " + str(result[1]) + postfix)
    print ('')


# Main
if __name__ == '__main__':

    # Processing Query 1
    popular_articles_res = execute_query(q1.query)
    display_query_results(q1.title, popular_articles_res)

    # Processing Query 2
    popular_author_res = execute_query(q2.query)
    display_query_results(q2.title, popular_author_res)

    # Processing Query 1
    error_res = execute_query(q3.query)
    display_query_results(q3.title, error_res, suffix=" % errors")
