CREATE USER decision@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON decision.* TO decision;

CREATE USER grafana@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON decision.* TO grafana;

USE decision;


CREATE TABLE `decision`.`vacancies` (
  `id` bigint auto_increment primary key,
  `requested_date` date DEFAULT NULL,
  `expected_hiring_date` date DEFAULT NULL,
  `title` longtext,
  `normalized_title` longtext,
  `sap_job` bit(1) DEFAULT NULL,
  `client` longtext,
  `client_requester` longtext,
  `department` longtext,
  `requester` longtext,
  `responsible_analyst` longtext,
  `hiring_type` longtext,
  `hiring_deadline` longtext,
  `objective` longtext,
  `priority` longtext,
  `reason` longtext,
  `manager` longtext,
  `name` longtext,
  `phone_number` longtext,
  `country` longtext,
  `state` longtext,
  `city` longtext,
  `neighborhood` longtext,
  `region` longtext,
  `workplace` longtext,
  `only_pwd` bit(1) DEFAULT NULL,
  `age_range` longtext,
  `work_schedule` longtext,
  `professional_level` longtext,
  `academic_level` longtext,
  `english_level` longtext,
  `spanish_level` longtext,
  `other_language` longtext,
  `areas_of_expertise` longtext,
  `main_activities` longtext,
  `technical_and_behavioral_skills` longtext,
  `other_observations` longtext,
  `required_travels` bit(1) DEFAULT NULL,
  `required_equipment` longtext,
  `selling_value` longtext,
  `purchase_value_1` longtext,
  `purchase_value_2` longtext,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `behavioral_skills` longtext,
  `substitute_name` longtext
);

CREATE TABLE `decision`.`applicants` (
  `id` bigint auto_increment primary key,
  `professional_objective` longtext,
  `created_at` timestamp NULL DEFAULT NULL,
  `inserted_by` longtext,
  `updated_at` timestamp NULL DEFAULT NULL,
  `professional_code` longtext,
  `acceptance_date` timestamp NULL DEFAULT NULL,
  `name` longtext,
  `cpf` blob,
  `source` longtext,
  `email` longtext,
  `secondary_email` blob,
  `birth_date` date DEFAULT NULL,
  `secondary_phone_number` blob,
  `phone_number` longtext,
  `cellphone` longtext,
  `gender` longtext,
  `marital_status` longtext,
  `is_pwd` bit(1) DEFAULT NULL,
  `location` longtext,
  `skype` blob,
  `linkedin_url` blob,
  `facebook_url` blob,
  `professional_title` longtext,
  `area_of_expertise` longtext,
  `technical_knowledge` longtext,
  `certifications` longtext,
  `other_certifications` longtext,
  `salary` longtext,
  `professional_level` longtext,
  `academic_level` longtext,
  `english_level` longtext,
  `spanish_level` longtext,
  `other_language` longtext,
  `cv_pt` longtext,
  `cv_en` blob,
  `higher_education_institution` longtext,
  `language_courses` longtext,
  `language_courses_year` longtext,
  `cv_filename` longtext,
  `qualifications` longtext,
  `experiences` longtext,
  `other_courses` longtext,
  `current_job_id` longtext,
  `corporate_email` double DEFAULT NULL,
  `current_job` longtext,
  `current_job_project` longtext,
  `current_job_client` longtext,
  `current_job_unit` longtext,
  `current_job_admission_date` longtext,
  `current_job_last_promotion_date` longtext,
  `current_job_immediate_superior_name` longtext,
  `current_job_immediate_superior_email` longtext
);

CREATE TABLE `decision`.`vacancies_applicants` (
  `id` bigint auto_increment primary key,
  `vacancy_id` bigint NOT NULL,
  `applicant_id` bigint NOT NULL,
  `status` longtext,
  `application_date` date DEFAULT NULL,
  `last_update` date DEFAULT NULL,
  `recruiter` longtext,
  CONSTRAINT `unk_vacancy_applicant` UNIQUE (`vacancy_id`, `applicant_id`),
  FOREIGN KEY (`vacancy_id`) REFERENCES `decision`.`vacancies` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`applicant_id`) REFERENCES `decision`.`applicants` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `decision`.`vacancies_tokens` (
  `id` bigint auto_increment primary key,
  `vacancy_id` bigint NOT NULL,
  `token` varchar(255),
  CONSTRAINT `unk_vacancy_token` UNIQUE (`vacancy_id`, `token`),
  FOREIGN KEY (`vacancy_id`) REFERENCES `decision`.`vacancies` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `decision`.`applicants_tokens` (
  `id` bigint auto_increment primary key,
  `applicant_id` bigint NOT NULL,
  `token` varchar(255),
  CONSTRAINT `unk_applicant_token` UNIQUE (`applicant_id`, `token`),
  FOREIGN KEY (`applicant_id`) REFERENCES `decision`.`applicants` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- CREATE TABLE `decision`.`price_history` (
--     `id` bigint auto_increment primary key,
--     `ticker` varchar(10) not null,
--     `reference_date` date not null default (current_date),
--     `close_price` double not null,
--     CONSTRAINT `unk_ticker_date` UNIQUE (`ticker`, `reference_date`),
--     INDEX `idx_price_dt` (`reference_date`)
-- );

-- CREATE TABLE `decision`.`prediction_price_history` (
--     `id` bigint auto_increment primary key,
--     `ticker` varchar(10) not null,
--     `reference_date` date not null default (current_date),
--     `predicted_price` double not null,
--     `model_version` varchar(255) not null,
--     CONSTRAINT `unk_ticker_date+prediction` UNIQUE (`ticker`, `reference_date`),
--     INDEX `idx_prediction_price_dt` (`reference_date`),
--     INDEX `idx_prediction_ticker` (`ticker`),
--     INDEX `idx_prediction_model_version` (`model_version`)
-- );