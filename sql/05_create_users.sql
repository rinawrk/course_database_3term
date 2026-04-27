USE hr_department_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

INSERT INTO users (login, password, role)
VALUES
    ('specialist', 'specialist123', 'specialist'),
    ('head', 'head123', 'head');