CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    email varchar(255) UNIQUE NOT NULL,
    full_name varchar(255) NOT NULL,
    dob DATE NOT NULL,
    password varchar(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scc varchar(10) UNIQUE NOT NULL

);
CREATE TABLE scc_codes(
    id SERIAL PRIMARY KEY,
    scc varchar(10) UNIQUE NOT NULL,
    usage BOOLEAN,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)

);
CREATE TABLE referendums(
    id SERIAL PRIMARY KEY,
    title varchar(255) NOT NULL,
    description TEXT NOT NULL ,
    status BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
CREATE TABLE referendum_options(
    id SERIAL PRIMARY KEY,
    option varchar(255) NOT NULL,
    referendum_id INT,
    FOREIGN KEY (referendum_id) REFERENCES referendums(id),
    vote_count INT DEFAULT 0

);
CREATE TABLE votes(
    id SERIAL PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    option_id INT,
    FOREIGN KEY (option_id) REFERENCES referendum_options(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    referendum_id INT,
    FOREIGN KEY (referendum_id) REFERENCES referendums(id),
    UNIQUE (user_id, referendum_id)

);