USE hr_department_db;

-- Отчет 1. Дети сотрудников выбранного отдела
SELECT
    d.department_name AS 'Отдел',
    e.employee_id AS 'Табельный номер',
    CONCAT(e.last_name, ' ', e.first_name, ' ', e.middle_name) AS 'Сотрудник',
    c.birth_certificate_number AS '№ свидетельства',
    c.child_name AS 'Имя ребенка',
    c.birth_year AS 'Год рождения',
    c.gender AS 'Пол ребенка'
FROM departments d
JOIN employees e ON e.department_id = d.department_id
JOIN children c ON c.employee_id = e.employee_id
WHERE d.department_id = 1
ORDER BY e.last_name, e.first_name, c.child_name;

-- Отчет 2. Сгруппированный список всей базы данных
SELECT
    d.department_name AS 'Отдел',
    CONCAT(e.last_name, ' ', e.first_name, ' ', e.middle_name) AS 'Сотрудник',
    e.work_experience AS 'Стаж',
    e.gender AS 'Пол сотрудника',
    c.child_name AS 'Имя ребенка',
    c.birth_year AS 'Год рождения ребенка',
    c.gender AS 'Пол ребенка'
FROM departments d
LEFT JOIN employees e ON e.department_id = d.department_id
LEFT JOIN children c ON c.employee_id = e.employee_id
ORDER BY d.department_name, e.last_name, e.first_name, c.child_name;