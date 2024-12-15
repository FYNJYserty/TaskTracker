

-- Вставка данных в таблицу пользователей
INSERT INTO user_tt (username, usr_password, first_name, age) VALUES
('john_doe', 'scrypt:32768:8:1$sysGyCDxaKVt23Lr$7a8fd6ea7c99ff9d9cf98333555ef20ce189861e1dbc16b7be7732cbd86cd79cbf331441a7d25888c5ff411ba537d7955e00b5b3a16db09a13d039f7c96f3a00', 'John', 30),
('jane_smith', 'scrypt:32768:8:1$EGK0IKvaBHLMOYBY$1954f53642958fb75f5f988edd603b236be08e61ff881b7a6536d80a94077bcbc01b36584bdbaaaffa6308171c0a5ab6936f3c2866e9a2b14be9c9b1bcf9ebe1', 'Jane', 28),
('alice_jones', 'scrypt:32768:8:1$33p6oFRxfVe4Bepw$5d5ce9649ddd940d30fa713bcfb1b113e351ae855d0d8577fe536c39aec9691bec7b770b365a63afa5d61accabb22d44e749cd6eeedb169ebfb1c684faa6c99e', 'Alice', 35),
('bob_brown', 'scrypt:32768:8:1$kQT9xrAm0WRR9K9m$8da096cf430aa2537c76cb88c3069162724e614593103aa07b891a7bcba2b2907020d892775cae75914111951fbd3d9b8c49a3103e5150b19ef0e37afb6cb266', 'Bob', 40);

-- Вставка данных в таблицу организаций
INSERT INTO organization (org_id, org_name, org_password, description) VALUES
(1, 'Tech Corp', 'orgpass1', 'A leading tech company'),
(2, 'Health Inc', 'orgpass2', 'A health care organization'),
(3, 'Edu Solutions', 'orgpass3', 'An educational services provider');

-- Вставка данных в таблицу проектов
INSERT INTO project (proj_id, organization_id, username, proj_name) VALUES
(1, 1, 'john_doe', 'Project Alpha'),
(2, 1, 'jane_smith', 'Project Beta'),
(3, 2, 'alice_jones', 'Health App'),
(4, 3, 'bob_brown', 'E-Learning Platform');

-- Вставка данных в таблицу задач
INSERT INTO task (tsk_id, tsk_username, tsk_name, description, deadline, status, project_id) VALUES
(1, 'john_doe', 'Design UI', 'Create the user interface for the project.', '2023-11-30', FALSE, 1),
(2, 'jane_smith', 'Develop API', 'Develop the backend API for the application.', '2023-12-15', FALSE, 1),
(3, 'alice_jones', 'Research', 'Conduct research for the health app.', '2023-11-20', TRUE, 3),
(4, 'bob_brown', 'Create Content', 'Develop educational content for the platform.', '2023-12-01', FALSE, 2);

-- Вставка данных в таблицу комментариев пользователей
INSERT INTO comment_usr (com_username, task_id, date, comment_text) VALUES
('john_doe', 1, CURRENT_TIMESTAMP, 'Looking good, let’s make it more user-friendly.'),
('jane_smith', 2, CURRENT_TIMESTAMP, 'API development is on track.'),
('alice_jones', 3, CURRENT_TIMESTAMP, 'Found some interesting data for our app.'),
('bob_brown', 4, CURRENT_TIMESTAMP, 'Content creation is progressing well.');

-- Вставка данных в таблицу вложений
INSERT INTO attachment (attach_username, task_id, mime_type) VALUES
('john_doe', 1, 'image/png'),
('jane_smith', 2, 'application/json'),
('alice_jones', 3, 'text/plain'),
('bob_brown', 4, 'application/pdf');

-- Вставка данных в таблицу статуса пользователя
INSERT INTO user_status (username, organization_id, usr_position) VALUES
('john_doe', 1, 'Owner'),
('jane_smith', 1, 'Developer'),
('alice_jones', 2, 'Researcher'),
('john_doe', 2, 'Owner'),
('bob_brown', 3, 'Content Creator'),
('alice_jones', 3, 'Owner');
