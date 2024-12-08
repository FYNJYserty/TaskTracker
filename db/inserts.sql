

-- Вставка данных в таблицу пользователей
INSERT INTO user_tt (username, usr_password, first_name, age) VALUES
('john_doe', 'password123', 'John', 30),
('jane_smith', 'securepass', 'Jane', 28),
('alice_jones', 'mypassword', 'Alice', 35),
('bob_brown', 'pass456', 'Bob', 40);

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
