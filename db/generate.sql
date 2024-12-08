
-- Удаление таблиц
DROP TABLE IF EXISTS comment_usr;
DROP TABLE IF EXISTS attachment;
DROP TABLE IF EXISTS user_status;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS organization;
DROP TABLE IF EXISTS user_tt;

-- Создание таблиц БД
-- Создание таблицы пользователя
CREATE TABLE user_tt (
    username VARCHAR(100) PRIMARY KEY,
    usr_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    age INT
);
-- Создание таблицы организации
CREATE TABLE organization (
    org_id SERIAL PRIMARY KEY,
    org_name VARCHAR(100) NOT NULL,
    org_password VARCHAR(255) NOT NULL,
    description TEXT
);
-- Создание таблицы проекта организации
CREATE TABLE project (
    proj_id SERIAL PRIMARY KEY,
    organization_id INT REFERENCES organization(org_id) ON UPDATE CASCADE,
    username VARCHAR(100) REFERENCES user_tt(username) ON UPDATE CASCADE,
    proj_name VARCHAR(100) NOT NULL
);
-- Создание таблицы задачи
CREATE TABLE task (
    tsk_id SERIAL PRIMARY KEY,
    tsk_username VARCHAR(100) REFERENCES user_tt(username) ON UPDATE CASCADE,
    tsk_name VARCHAR(100) NOT NULL,
    description TEXT,
    deadline DATE,
    status BOOLEAN,
	project_id SERIAL REFERENCES project(proj_id) ON UPDATE CASCADE
);
-- Создание таблицы комментария пользователя
CREATE TABLE comment_usr (
    com_id SERIAL PRIMARY KEY,
    com_username VARCHAR(100) REFERENCES user_tt(username) ON UPDATE CASCADE,
    task_id INT REFERENCES task(tsk_id) ON UPDATE CASCADE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment_text TEXT
);
-- Создание таблицы вложения
CREATE TABLE attachment (
    attach_id SERIAL PRIMARY KEY,
    attach_username VARCHAR(100) REFERENCES user_tt(username) ON UPDATE CASCADE,
    task_id INT REFERENCES task(tsk_id) ON UPDATE CASCADE,
    mime_type VARCHAR(50),
    file_data BYTEA
);
-- Создание таблицы статуса пользователя
CREATE TABLE user_status (
    username VARCHAR(100) REFERENCES user_tt(username) ON UPDATE CASCADE,
    organization_id INT REFERENCES organization(org_id) ON UPDATE CASCADE,
    usr_position VARCHAR(100),
    PRIMARY KEY (username, organization_id)
);