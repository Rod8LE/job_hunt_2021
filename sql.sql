--Dado una tabla de empleados (id, name, salary, manager_id)
--Crear una consulta que devuelva los empleados que cobran mas que su manager.

SELECT name
FROM empleados
RIGHT JOIN (
    SELECT id, name, salary_manager
    FROM empleados
) AS managers ON managers.id = empleados.manager_id
WHERE salary_manager < salary


--Dado una tabla de empleados (id, name, salary, dept_id) y una tabla de departamentos (id, name).
--Crear una consulta que devuelva los empleados que cobran mas por departamento.


SELECT empleados.name, departamentos.name, salary
FROM empleados
JOIN departamentos ON empleados.dept_id = departamentos.id
ORDER BY salary DESC



-- create a table
CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  age INTEGER
);
-- insert some values
INSERT INTO students VALUES (1, 'Ryan', '1');
INSERT INTO students VALUES (2, 'Joanna', '2');
INSERT INTO students VALUES (3, 'Ryan', '4');
INSERT INTO students VALUES (4, 'Joanna', '6');
INSERT INTO students VALUES (5, 'Ryan', '8');
INSERT INTO students VALUES (6, 'Joanna', '16');

-- fetch some values
SELECT distinct (name),
SUM(age) OVER (partition by name) as plop
FROM students;

-- clean up
DROP TABLE students;
