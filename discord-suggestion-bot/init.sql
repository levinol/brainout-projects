CREATE SCHEMA brainout
    CREATE TABLE suggestions(
        id SERIAL PRIMARY KEY, 
        author_id VARCHAR(50) NOT NULL, 
        msg_id VARCHAR(50) NOT NULL
    )
    CREATE TABLE submissions(
        id SERIAL PRIMARY KEY, 
        author_id VARCHAR(50) NOT NULL, 
        msg_id VARCHAR(50) NOT NULL,
        in_final BOOlEAN NOT NULL 
    )