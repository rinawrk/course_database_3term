USE hr_department_db;

INSERT INTO departments (department_id, department_name)
VALUES
    (1, 'Отдел кадров'),
    (2, 'Бухгалтерия'),
    (3, 'ИТ-отдел');

INSERT INTO employees (
    employee_id,
    last_name,
    first_name,
    middle_name,
    work_experience,
    gender,
    department_id
)
VALUES
    (1001, 'Иванова', 'Мария', 'Сергеевна', 5, 'Ж', 1),
    (1002, 'Петров', 'Алексей', 'Николаевич', 8, 'М', 1),
    (1003, 'Сидорова', 'Елена', 'Викторовна', 12, 'Ж', 2),
    (1004, 'Кузнецов', 'Дмитрий', 'Олегович', 4, 'М', 3),
    (1005, 'Смирнова', 'Анна', 'Игоревна', 7, 'Ж', 3);

INSERT INTO children (
    birth_certificate_number,
    child_name,
    birth_year,
    gender,
    employee_id
)
VALUES
    (5001, 'Ольга', 2015, 'Ж', 1001),
    (5002, 'Иван', 2018, 'М', 1001),
    (5003, 'Максим', 2012, 'М', 1002),
    (5004, 'Алина', 2017, 'Ж', 1003),
    (5005, 'Егор', 2020, 'М', 1004),
    (5006, 'София', 2016, 'Ж', 1005);