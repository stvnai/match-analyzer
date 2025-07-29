import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import Engine
from werkzeug.security import check_password_hash

load_dotenv()

def get_sqlalchemy_engine():
    dbname= os.getenv("DB_NAME")
    user= os.getenv("DB_USER")
    password= os.getenv("DB_PASS")
    host= os.getenv("DB_HOST")
    port= os.getenv("DB_PORT")

    db_url= f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"

    return create_engine(
        db_url,
        echo=False,
        future=True,
        pool_size=5,
        max_overflow=2,
        pool_timeout=60,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={
            "connect_timeout":30,
            "application_name":"match_analyzer",
            "options": "-c statement_timeout=30000"
        }
    )

try:
    ENGINE= get_sqlalchemy_engine()
    print("Connected")
except Exception as e:
    ENGINE = None
    print(f"Something goes wrong connecting with database: {e}.")



def auth_user(username:str, password:str, engine:Engine=ENGINE):
    if ENGINE is None:
        print("No database engine available.")
        return None
    
    query= text(
        """ SELECT user_id, password_hash
            FROM users
            WHERE username= :username
            LIMIT 1
        """
    )

    values= {"username":username}

    try:
        with engine.connect() as conn:
            result= conn.execute(query, values)
            user_credentials= result.fetchone()
            user_id= user_credentials[0]
            stored_hash= user_credentials[1]

            if user_credentials:
                if check_password_hash(stored_hash, password):
                    return user_id
            else:
                return None

    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None


def get_user_by_id(user_id, engine:Engine=ENGINE):

    if engine is None:
        print("No database engine available")
        return None
    
    query= text(
        """
        SELECT user_id, username
        FROM users
        WHERE user_id = :user_id        
        """
    )

    values= {"user_id": user_id}

    try:
        with engine.connect() as conn:
            result= conn.execute(query, values)
            user_data= result.fetchone()
            return user_data
        
    except Exception as e:
        print(f"Error retrieving data from user: {e}")
        return None
        


