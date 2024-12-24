

-- Вставка данных в таблицу пользователей
-- password123
-- janeSuper
-- Jones12345
-- fantik123
-- passwd
-- 123456
-- qwerty123
INSERT INTO user_tt (username, usr_password, first_name, age) VALUES
('john_doe', 'scrypt:32768:8:1$Bb7TP6VIuk4zKfrL$7fc84e6564e6c7ce431b9430c36174fdba6a59216e041d73d1b12dd2dcd71e0d71fe33b63f6cb21881cf42fc8fd1432955974f535c270f2e5a73f8182e996559', 'John', 30),
('jane_smith', 'scrypt:32768:8:1$yvWjrhRqGIxMN2Qj$db5892012027799539cb2f5076a6a2f5373b664d2d23993b8430cf62f1a1d2f331b22920c0e6534e32e37cde80df473bccf7d80edddbc0f70bbc6a5ffd84869f', 'Jane', 28),
('alice_jones', 'scrypt:32768:8:1$D5lbV6AcyqRqe5y9$45b27da7c0a24edda069a732309b4e4d73439e3006b9a39303c9bc33c5da3ffda3de1798a0ff4559eb0266ba4e844e438a4deec18ebbf40bf30a44786fe9cf27', 'Alice', 35),
('bob_brown', 'scrypt:32768:8:1$5kaAmUbkJGiqBrUu$8f6554e981b3be6ede18d5ec921db1b0942a9ae3a66da815e08618feed0037a842f4b43b560b401431c5a6842e3926362b57549eea819dca6f9d89d29253d922', 'Bob', 40),
('charlie_black', 'scrypt:32768:8:1$gbiL0Csmci0rD4HA$f773c216d99dbd344ce21e65934698d3550f939f7619f70629ea555608917519582153012ea9e95cf8238facd9dec32201e8bcdf98aa27823a0caabfca2fe85d', 'Charlie', 32),
('diana_green', 'scrypt:32768:8:1$7rD30wGCAiPiujjH$0d773e96fdbaebb68eb06546056a5f5c5c5efbeddd7368b8a18113ac66e49305b3deb2af3342aeb771f3ac3abc4752c02704e22a72e78c47c94a7c8a704ef0eb', 'Diana', 29),
('edward_white', 'scrypt:32768:8:1$1ZeeDz6kZcMqZt7q$64c056ef792a81bb5e5186e858ae5156eaf72f54a5ac9d6628f136f442a287bebfb9814556c9509fc269ba3eb8fb62f724361a7c11606fbefd5587210ca0c01a', 'Edward', 41);

-- Вставка данных в таблицу организаций
-- orgpass1
-- orgpass2
-- orgpass3
-- orgpass4
-- orgpass5
INSERT INTO organization (org_name, org_password, description) VALUES
('Tech Corp', 'scrypt:32768:8:1$GAPxKuE2RpgzL2E5$232081d599550925e52ff8f59cc25de417513612101edc7c323cb12b5ea6492536f9cfba64c3bd92fb82b7aa3775622974b165724afa63258036822d7975ae16', 'A leading tech company'),
('Health Inc', 'scrypt:32768:8:1$D9r6z7yYsmfedGMV$9d6a12e96e38adb8dbd2951c76fda25fc9c1a8ecc284abaa72ec85721b3dd2538fb152c37f2d608bf562a875d36b8fda83528cb1186a7cc5de3ccc5e04580059', 'A health care organization'),
('Edu Solutions', 'scrypt:32768:8:1$GEFSzURruGoGhLn1$4b691051a230be5a2746512500aa7bde2b8919eafb8725d37852e2939cedc8d4dba20a27809910aa444aaa3cd3d53472bdef153e32cada57c9f88da20d5c29bc', 'An educational services provider'),
('Finance Group', 'scrypt:32768:8:1$TYfQsDjv0RqgSWQz$baa9e2e80b854a682d13207f1a9f258c6cd3aaf909f8d6f0803fff7b452c8843c283e73ec0a204aca19e740bcf1c9de7063d2e9db960b2991eee078840a3dab9', 'A financial services company'),
('Creative Agency', 'scrypt:32768:8:1$G7bbvjqnHOZl25I9$389c827ac9a261b291eb1a2fefe6da64832dd358ed2737dc2c65e1a8931f12f7ab0772c4f04054015fef62edece4daa66b9e59a3a9a115ffe998326510f7ee48', 'A creative marketing agency');

-- Вставка данных в таблицу проектов
INSERT INTO project (organization_id, username, proj_name) VALUES
(1, 'john_doe', 'Project Alpha'),
(1, 'jane_smith', 'Project Beta'),
(2, 'alice_jones', 'Health App'),
(3, 'bob_brown', 'E-Learning Platform'),
(4, 'charlie_black', 'Finance Tracker'),
(5, 'diana_green', 'Brand Awareness Campaign'),
(4, 'edward_white', 'Investment Portfolio Management');

-- Вставка данных в таблицу задач
INSERT INTO task (tsk_username, tsk_name, description, deadline, status, project_id) VALUES
('john_doe', 'Design UI', 'Create the user interface for the project.', '2023-11-30', FALSE, 1),
('jane_smith', 'Develop API', 'Develop the backend API for the application.', '2023-12-15', FALSE, 1),
('alice_jones', 'Research', 'Conduct research for the health app.', '2023-11-20', TRUE, 3),
('bob_brown', 'Create Content', 'Develop educational content for the platform.', '2023-12-01', FALSE, 2),
('charlie_black', 'Market Analysis', 'Analyze market trends for the finance tracker.', '2023-11-25', FALSE, 5),
('diana_green', 'Design Campaign', 'Create a design for the brand awareness campaign.', '2023-12-10', FALSE, 6),
('edward_white', 'Portfolio Review', 'Review investment portfolios and suggest improvements.', '2023-12-20', FALSE, 7);

-- Вставка данных в таблицу комментариев пользователей
INSERT INTO comment_usr (com_username, task_id, date, comment_text) VALUES
('john_doe', 1, CURRENT_TIMESTAMP, 'Looking good, let’s make it more user-friendly.'),
('jane_smith', 2, CURRENT_TIMESTAMP, 'API development is on track.'),
('alice_jones', 3, CURRENT_TIMESTAMP, 'Found some interesting data for our app.'),
('bob_brown', 4, CURRENT_TIMESTAMP, 'Content creation is progressing well.'),
('charlie_black', 5, CURRENT_TIMESTAMP, 'Starting the market analysis today.'),
('diana_green', 6, CURRENT_TIMESTAMP, 'The design concepts are ready for review.'),
('edward_white', 7, CURRENT_TIMESTAMP, 'I will gather the necessary data for the portfolio review.');

-- Вставка данных в таблицу статуса пользователя
INSERT INTO user_status (username, organization_id, usr_position) VALUES
('john_doe', 1, 'Owner'),
('jane_smith', 1, 'Developer'),
('alice_jones', 2, 'Researcher'),
('john_doe', 2, 'Owner'),
('bob_brown', 1, 'Content Creator'),
('alice_jones', 3, 'Owner'),
('charlie_black', 4, 'Owner'),
('diana_green', 5, 'Owner'),
('edward_white', 4, 'Investment Advisor'),
('charlie_black', 5, 'Analyst'),
('diana_green', 1, 'Developer');
