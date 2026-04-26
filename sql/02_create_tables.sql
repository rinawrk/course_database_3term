USE hr_department_db;

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100) NOT NULL,
    work_experience INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    department_id INT NOT NULL,
    CONSTRAINT fk_employees_departments
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE children (
    birth_certificate_number INT PRIMARY KEY,
    child_name VARCHAR(100) NOT NULL,
    birth_year YEAR NOT NULL,
    gender VARCHAR(10) NOT NULL,
    employee_id INT NOT NULL,
    CONSTRAINT fk_children_employees
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);