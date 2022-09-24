import mysql.connector
import pandas as pd

def retrieve_paper_info(doi = "https://doi.org/10.1016/j.chs.2003.07.001"):
    # Connect to server
    import mysql.connector
    cnx = mysql.connector.connect(
        host="rm-wz9y2920jvc715m74mo.mysql.rds.aliyuncs.com",
        port=3306,
        user="qidi",
        password="Hahaha000_",
        database="paper_db")

    # Get a cursor
    cur = cnx.cursor()
    # Execute a query
    cur.execute("""
                SELECT title, year, journal, abstract  
                FROM `all_data` 
                WHERE doi = "%s"; 
                """%(doi))

    # Fetch one result
    title, year, journal, abstract = cur.fetchone()
    cnx.close()

    return title, year, journal, abstract

def count_paper():
    # Connect to server
    import mysql.connector
    cnx = mysql.connector.connect(
        host="rm-wz9y2920jvc715m74mo.mysql.rds.aliyuncs.com",
        port=3306,
        user="qidi",
        password="Hahaha000_",
        database="paper_db")

    # Get a cursor
    cur = cnx.cursor()
    # Execute a query
    cur.execute("""
                SELECT year, COUNT(*)
                FROM all_data
                GROUP BY year
                ORDER BY year; 
                """)

    # Fetch one result
    df = pd.DataFrame(cur.fetchall(),columns=["year","count"])
    cnx.close()
    return df

def count_journal():
    # Connect to server
    import mysql.connector
    cnx = mysql.connector.connect(
        host="rm-wz9y2920jvc715m74mo.mysql.rds.aliyuncs.com",
        port=3306,
        user="qidi",
        password="Hahaha000_",
        database="paper_db")

    # Get a cursor
    cur = cnx.cursor()
    # Execute a query
    cur.execute("""
                SELECT journal, COUNT(*)
                FROM all_data
                GROUP BY journal
                ORDER BY journal;
                """)

    # Fetch one result
    df = pd.DataFrame(cur.fetchall(),columns=["journal","count"])
    cnx.close()
    return df

#[print(count_paper())]
