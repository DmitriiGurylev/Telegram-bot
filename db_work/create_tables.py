from db_work import pg_connection
from psycopg2 import DatabaseError


def create_tables():
    # """ create DB"""
    # create_db_command = (
    #     f"""
    #     CREATE DATABASE {pg_connection.db_name}
    #     """
    # )
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE twitter_users (
            twitter_user_id SERIAL PRIMARY KEY
        )
        """,
        """ 
        CREATE TABLE service_followers (
                tlg_id INTEGER PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE twitter_user_last_msgs (
                twitter_user_id INTEGER PRIMARY KEY,
                msg_id INTEGER
        )
        """,
        """
        CREATE TABLE service_users_following (
                tlg_id INTEGER,
                twitter_user_id INTEGER,
                PRIMARY KEY (tlg_id, twitter_user_id),
                CONSTRAINT fk_tlg_id FOREIGN KEY(tlg_id) REFERENCES service_followers(tlg_id),
                CONSTRAINT fk_twitter_user_id FOREIGN KEY(twitter_user_id) REFERENCES twitter_users(twitter_user_id)
        )
        """
    )
    try:
        with pg_connection.conn as conn:
            with conn.cursor() as cursor:
                for c in commands:
                    cursor.execute(c)
    except (Exception, DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    create_tables()
