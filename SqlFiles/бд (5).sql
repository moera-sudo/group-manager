DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS addresses CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS s_family_info CASCADE;
DROP TABLE IF EXISTS stud_group_list CASCADE;
DROP TABLE IF EXISTS student_info CASCADE;
DROP TABLE IF EXISTS vote_answers CASCADE;
DROP TABLE IF EXISTS votes CASCADE;
DROP TABLE IF EXISTS login_logs CASCADE;




-- Создаем функцию для генерации 10-значного кода
CREATE OR REPLACE FUNCTION generate_group_code()
RETURNS TRIGGER AS $$
DECLARE
    generated_code VARCHAR(10);
    is_unique BOOLEAN;
BEGIN
    LOOP
        -- Генерация случайного 10-значного кода
        generated_code := (
            SELECT string_agg(chars, '')
            FROM (
                SELECT substr('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', (random() * 35 + 1)::int, 1) AS chars
                FROM generate_series(1, 10)
            ) AS code_parts
        );

        -- Проверка уникальности
        SELECT NOT EXISTS(SELECT 1 FROM groups WHERE group_code = generated_code) INTO is_unique;

        -- Если код уникален, выходим из цикла
        IF is_unique THEN
            EXIT;
        END IF;
    END LOOP;

    -- Устанавливаем сгенерированный код для нового добавляемого ряда
    NEW.group_code := generated_code;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггер для таблицы groups
drop trigger if exists trg_generate_group_code;
CREATE TRIGGER trg_generate_group_code
BEFORE INSERT ON groups
FOR EACH ROW
WHEN (NEW.group_code IS NULL OR NEW.group_code = '')
EXECUTE FUNCTION generate_group_code();

--logи входа админа
CREATE TABLE login_logs (
    id SERIAL PRIMARY KEY,
    chat_id VARCHAR(255) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE OR REPLACE FUNCTION log_admin_login()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.acc_type = 'admin' THEN
        INSERT INTO login_logs (chat_id, login_time)
        VALUES (NEW.chat_id, CURRENT_TIMESTAMP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

drop trigger if exists trigger_log_admin_login;
CREATE TRIGGER trigger_log_admin_login
AFTER UPDATE OF chat_id
ON accounts
FOR EACH ROW
WHEN (OLD.chat_id IS DISTINCT FROM NEW.chat_id AND NEW.acc_type = 'admin')
EXECUTE FUNCTION log_admin_login();



--view для всех данных о студенте
drop view if exists student_full_info;
CREATE OR REPLACE VIEW student_full_info AS
SELECT
    s.name AS "Имя",
    s.surname AS "Фамилия",
    s.last_name AS "Отчество",
    s.birthday AS "Дата рождения",
    s.iin AS "ИИН",
    s.phone_number AS "Номер телефона",
	ac.email as "Почта",
    s.gender AS "Пол",
    s.education_type AS "Форма обучения",
    s.course AS "Курс",
    g.group_name AS "Группа",
    s.student_status AS "Статус студента",
    s.hobby AS "Хобби",
    s.special_needs AS "Особые потребности",
    s.is_invalid AS "Инвалидность",
    s.is_have_psyphis_qualities AS "Особые психофизические качества",
    s.is_underachiever AS "Неуспевающий",
    s.is_ifm AS "Учет ИДН",
    s.is_orphan AS "Сирота",
    s.nationality AS "Национальность",
    s.citizenship AS "Гражданство",
    s.registration AS "Регистрация",
    s.doc_validity_period AS "Срок действия документа",
    s.social_status AS "Социальный статус",
    s.lost_parent AS "Потеря родителей",
    s.retired_parents AS "Родители пенсионеры",
    s.is_large_family AS "Многодетная семья",
    s.childs_count AS "Количество детей",
    a.city || ' р.' || a.district || ' ' || a.street || ' ' || a.house || ' п.' || a.entrance || ' этаж' || a.floor || ' кв. ' || a.flat AS "Адрес проживания",
    s.live_with_whom AS "С кем проживает",
    s.ownership_form AS "Форма собственности",
    s.ex_school AS "Бывшая школа",
    s.from_where_country AS "Страна прописки",
    e.city || ' р.' || e.district || ' ' || e.street || ' ' || e.house || ' п.' || e.entrance || ' этаж' || e.floor || ' кв.' || e.flat AS "Откуда прибыл",
    s.where_country AS "Куда прибыл",
    r.city || ' р.' || r.district || ' ' || r.street || ' ' || r.house || ' п.' || r.entrance || ' этаж' || r.floor || ' кв.' || r.flat AS "Адрес прописки",
    f.mother_name AS "Имя матери",
    f.mother_surname AS "Фамилия матери",
    f.mother_last_name AS "Отчество матери",
    f.mother_phone_number AS "Телефон матери",
    f.mother_birthday AS "Дата рождения матери",
    f.mother_workplace AS "Место работы матери",
    f.mother_education_info AS "Образование матери",
    f.mother_social_status AS "Социальный статус матери",
    f.father_name AS "Имя отца",
    f.father_surname AS "Фамилия отца",
    f.father_last_name AS "Отчество отца",
    f.father_phone_number AS "Телефон отца",
    f.father_birthday AS "Дата рождения отца",
    f.father_workplace AS "Место работы отца",
    f.father_education_info AS "Образование отца",
    f.father_social_status AS "Социальный статус отца",
    f.guardian_name AS "Имя опекуна",
    f.guardian_surname AS "Фамилия опекуна",
    f.guardian_last_name AS "Отчество опекуна",
    f.guardian_phone_number AS "Телефон опекуна",
    f.guardian_birthday AS "Дата рождения опекуна",
    f.guardian_workplace AS "Место работы опекуна",
    f.guardian_education_info AS "Образование опекуна",
    f.guardian_social_status AS "Социальный статус опекуна"
FROM
    student_info s
JOIN
    s_family_info f
ON
    s.student_id = f.student_id
JOIN
    addresses a
ON
    s.address_id = a.address_id
JOIN
    accounts ac
ON
    s.student_id = ac.student_id
JOIN
    addresses e
ON
    s.ex_address_id = e.address_id
LEFT JOIN
    addresses r
ON
    s.reg_address_id = r.address_id
JOIN
    groups g
ON
    s.group_id = g.group_id;


--view для всех данных аккаунтов
drop view if exists view_account_details;
CREATE OR REPLACE VIEW view_account_details AS
SELECT 
    a.account_id,
    a.email "почта",
    a.chat_id "чат айди из телеграмм",
    s.name || '' || s.surname ||' '|| s.last_name AS "Фио",
    a.acc_type AS "Тип аккаунта"
FROM 
    accounts a
LEFT JOIN student_info s ON a.student_id = s.student_id;



INSERT INTO stud_group_list (sgl_id, group_name, student_fio) 
VALUES 
    (1, 'ПО2306', 'Абильдин Шынгыс'),
    (2, 'ПО2306', 'Адилова Адина'),
    (3, 'ПО2306', 'Аширбек Амир'),
    (4, 'ПО2306', 'Бекен Алиакбар'),
    (5, 'ПО2306', 'Бурик Егор'),
    (6, 'ПО2306', 'Быстрицкий Трофим'),
    (7, 'ПО2306', 'Вяткин Кирилл'),
    (8, 'ПО2306', 'Ермохин Данил'),
    (9, 'ПО2306', 'Жакан Алуа'),
    (10, 'ПО2306', 'Жусупова Альбина'),
    (11, 'ПО2306', 'Заккиев Ерсултан'),
    (12, 'ПО2306', 'Кабдрашев Мансур'),
    (13, 'ПО2306', 'Курмангалиев Ельдар'),
    (14, 'ПО2306', 'Лекерова Амина'),
    (15, 'ПО2306', 'Манасбаев Алинур'),
    (16, 'ПО2306', 'Мукынов Мансур'),
    (17, 'ПО2306', 'Рожков Артём'),
    (18, 'ПО2306', 'Саден Мереке'),
    (19, 'ПО2306', 'Свобода Артём'),
    (20, 'ПО2306', 'Тлеухан Ильяс');
	
Select * from accounts
select * from student_info
Select * from groups