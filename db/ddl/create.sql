DROP DATABASE IF EXISTS PROJECT;

CREATE DATABASE PROJECT;

\c project;

CREATE TABLE GENERAL_PUBLIC (
  general_public_name VARCHAR(20) NOT NULL,
  general_public_phone VARCHAR(10) NOT NULL,
  general_public_email VARCHAR(50) NOT NULL,
  general_public_address VARCHAR(500) NOT NULL,
  general_public_age INT NOT NULL,
  general_public_aadhar_no VARCHAR(12) NOT NULL,
  PRIMARY KEY (general_public_aadhar_no)
);

CREATE TABLE ANIMAL_SHELTER (
  animal_shelter_certificate_no VARCHAR(50) NOT NULL,
  animal_shelter_no_of_pets INT NOT NULL,
  animal_shelter_address VARCHAR(5000) NOT NULL,
  animal_shelter_phone CHAR(10) NOT NULL,
  animal_shelter_name VARCHAR(50) NOT NULL,
  animal_shelter_city VARCHAR(20) NOT NULL,
  PRIMARY KEY(animal_shelter_certificate_no)
);

CREATE TABLE ANIMAL_TYPE (
  animal_type_id VARCHAR(50) NOT NULL,
  animal_type_breed VARCHAR(40) NOT NULL,
  animal_type_type VARCHAR(20) NOT NULL,
  PRIMARY KEY (animal_type_id),
  UNIQUE(animal_type_breed)
);

CREATE TABLE DOCTORS (
  doctor_domain VARCHAR(50) NOT NULL,
  doctor_name VARCHAR(20) NOT NULL,
  doctor_phone VARCHAR(10) NOT NULL,
  doctor_email VARCHAR(40) NOT NULL,
  doctor_hospital_address VARCHAR(5000) NOT NULL,
  doctor_certificate_no VARCHAR(50) NOT NULL,
  PRIMARY KEY (doctor_certificate_no)
);

CREATE TABLE PET_CARE_PRODUCTS (
  pet_care_products_id VARCHAR(20) NOT NULL,
  pet_care_products_product_type VARCHAR(25) NOT NULL,
  pet_care_products_link VARCHAR(1000) NOT NULL,
  pet_care_products_link_website VARCHAR(30) NOT NULL,
  pet_care_products_animal_type_id VARCHAR(50) NOT NULL,
  PRIMARY KEY (pet_care_products_id),
  FOREIGN KEY(pet_care_products_animal_type_id) REFERENCES ANIMAL_TYPE(animal_type_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE PET_SHOP (
  pet_shop_no_of_pets INT NOT NULL,
  pet_shop_certificate_no VARCHAR(50) NOT NULL,
  pet_shop_phone CHAR(10) NOT NULL,
  pet_shop_name VARCHAR(40) NOT NULL,
  pet_shop_address VARCHAR(5000) NOT NULL,
  pet_shop_city VARCHAR(20) NOT NULL,
  PRIMARY KEY (pet_shop_certificate_no)
);

CREATE TABLE ZOOS (
  zoos_id VARCHAR(20) NOT NULL,
  zoos_name VARCHAR(50) NOT NULL,
  zoos_address VARCHAR(5000) NOT NULL,
  zoos_phone CHAR(11) NOT NULL,
  zoos_no_of_animals INT NOT NULL,
  zoos_visiting_hours VARCHAR(20) NOT NULL,
  PRIMARY KEY (zoos_id)
);

CREATE TABLE ANIMAL (
  animal_id VARCHAR(50) NOT NULL,
  animal_zoos_id VARCHAR(4) ,
  animal_pet_shop_certificate_no VARCHAR(4) ,
  animal_animal_shelter_certificate_no VARCHAR(4) ,
  animal_adopted BOOL NOT NULL,
  animal_type_id VARCHAR(50) NOT NULL,
  animal_from_pet_shop BOOL NOT NULL,
  animal_from_shelter BOOL NOT NULL,
  animal_from_zoos BOOL NOT NULL,
  animal_disease_history_exist BOOL NOT NULL,
  animal_gender CHAR(1) NOT NULL,
  animal_weight FLOAT NOT NULL,
  animal_age INT NOT NULL,
  animal_price INT,
  animal_image_link varchar(5000) NOT NULL,
  PRIMARY KEY(animal_id),
  FOREIGN KEY(animal_type_id) REFERENCES ANIMAL_TYPE(animal_type_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_zoos_id) REFERENCES ZOOS(zoos_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_animal_shelter_certificate_no) REFERENCES ANIMAL_SHELTER(animal_shelter_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_pet_shop_certificate_no) REFERENCES PET_SHOP(pet_shop_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ANIMAL_ADOPTED (
  animal_adopted_animal_id VARCHAR(50) NOT NULL,
  animal_adopted_animal VARCHAR(50) NOT NULL,
  animal_adopted_zoos_id VARCHAR(4) ,
  animal_adopted_adoption_date DATE DEFAULT('01-01-2000'),
  animal_adopted_sponsor_amount FLOAT  DEFAULT(0.0),
  animal_adopted_price_from_shop FLOAT DEFAULT(0.0),
  animal_adopted_general_public_aadhar VARCHAR(12) DEFAULT('NOT ADOPTED'),
  animal_adopted_pet_shop_certificate_no VARCHAR(4) ,
  animal_adopted_animal_shelter_certificate_no VARCHAR(4) ,
  PRIMARY KEY (animal_adopted_animal_id),
  FOREIGN KEY (animal_adopted_general_public_aadhar) REFERENCES GENERAL_PUBLIC(general_public_aadhar_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_adopted_pet_shop_certificate_no) REFERENCES PET_SHOP(pet_shop_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_adopted_animal_shelter_certificate_no) REFERENCES ANIMAL_SHELTER(animal_shelter_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_adopted_zoos_id) REFERENCES ZOOS(zoos_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_adopted_animal_id) REFERENCES ANIMAL(animal_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SPONSOR (
  sponsor_id VARCHAR(50) NOT NULL,
  sponsor_zoos_id VARCHAR(50) NOT NULL,
  sponsor_animal_id VARCHAR(50) NOT NULL,
  PRIMARY KEY (sponsor_id),
  FOREIGN KEY (sponsor_zoos_id) REFERENCES ZOOS(zoos_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (sponsor_animal_id) REFERENCES ANIMAL(animal_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ADOPT (
  adopt_id VARCHAR(50) NOT NULL,
  adopt_animal_id VARCHAR(20) NOT NULL,
  adopt_animal_shelter_certificate_no VARCHAR(50) NOT NULL,
  FOREIGN KEY (adopt_animal_shelter_certificate_no) REFERENCES    ANIMAL_SHELTER(animal_shelter_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (adopt_animal_id) REFERENCES ANIMAL(animal_id) ON UPDATE CASCADE ON DELETE CASCADE,
  PRIMARY KEY (adopt_id)
);

CREATE TABLE HOST (
  host_id VARCHAR(20) NOT NULL,
  host_animal_id VARCHAR(20) NOT NULL,
  host_pet_shop_certificate_no VARCHAR(50) NOT NULL,
  PRIMARY KEY (host_id),
  FOREIGN KEY (host_pet_shop_certificate_no) REFERENCES PET_SHOP(pet_shop_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (host_animal_id) REFERENCES ANIMAL(animal_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ANIMAL_ANIMAL_DISEASE_HISTORY (
  animal_animal_disease_history_animal_disease_name VARCHAR(100) NOT NULL,
  animal_animal_disease_history_animal_id VARCHAR(20) NOT NULL,
  animal_animal_disease_history_animal_disease_no_of_months INT NOT NULL,
  animal_animal_disease_history_general_public_aadhar_no CHAR(12) DEFAULT('Not Adopted'),
  animal_animal_disease_history_pet_shop_certificate_no VARCHAR(50)  DEFAULT(NULL),
  animal_animal_disease_history_animal_shelter_certificate_no VARCHAR(50)  DEFAULT(NULL),
  animal_animal_disease_history_zoos_id VARCHAR(20)  DEFAULT(NULL),
  PRIMARY KEY (
    animal_animal_disease_history_animal_disease_name,
    animal_animal_disease_history_animal_id
  ),
  FOREIGN KEY (animal_animal_disease_history_animal_id) REFERENCES ANIMAL(animal_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (
    animal_animal_disease_history_general_public_aadhar_no
  ) REFERENCES GENERAL_PUBLIC(general_public_aadhar_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (
    animal_animal_disease_history_pet_shop_certificate_no
  ) REFERENCES PET_SHOP(pet_shop_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (
    animal_animal_disease_history_animal_shelter_certificate_no
  ) REFERENCES ANIMAL_SHELTER(animal_shelter_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (animal_animal_disease_history_zoos_id) REFERENCES ZOOS(zoos_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ANIMAL_TYPE_ANIMAL_TYPE_CARE (
  animal_type_animal_type_care_id VARCHAR(50) NOT NULL,
 animal_type_animal_type_care_animal_type_care TEXT NOT NULL,
  animal_type_animal_type_care_animal_type_breed VARCHAR(20) NOT NULL,
  PRIMARY KEY (animal_type_animal_type_care_id),
  FOREIGN KEY (animal_type_animal_type_care_animal_type_breed) REFERENCES ANIMAL_TYPE(animal_type_breed) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE QUERIES (
  queries_query_id VARCHAR(20) NOT NULL,
  queries_query_question VARCHAR(5000) NOT NULL,
  queries_raised_by_aadhar_no VARCHAR(12) NOT NULL DEFAULT('Anonymus'),
  PRIMARY KEY (queries_query_id),
  FOREIGN KEY (queries_raised_by_aadhar_no) REFERENCES GENERAL_PUBLIC(general_public_aadhar_no) ON UPDATE CASCADE ON DELETE
  SET
    DEFAULT
);

CREATE TABLE QUERIES_QUERY_ANSWER (
  queries_query_answer_id VARCHAR(20) NOT NULL,
  queries_query_answer_query_answer TEXT NOT NULL,
  queries_query_answer_query_id VARCHAR(20) NOT NULL,
  queries_query_answer_query_answered_by VARCHAR(50) NOT NULL,
  PRIMARY KEY (queries_query_answer_id),
  FOREIGN KEY (queries_query_answer_query_id) REFERENCES QUERIES(queries_query_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (queries_query_answer_query_answered_by) REFERENCES DOCTORS(doctor_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE LOGIN_PUBLIC (
  login_public_adhar_no_id VARCHAR(12) NOT NULL,
  login_public_username VARCHAR(20) NOT NULL,
  login_public_password VARCHAR(20) NOT NULL,
  FOREIGN KEY (login_public_adhar_no_id) REFERENCES GENERAL_PUBLIC(general_public_aadhar_no) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE LOGIN_ZOO (
  login_zoo_zoos_id VARCHAR(3) NOT NULL,
  login_zoo_username VARCHAR(40) NOT NULL,
  login_zoo_password VARCHAR(20) NOT NULL,
  FOREIGN KEY (login_zoo_zoos_id) REFERENCES ZOOS(zoos_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE LOGIN_PET_SHOP (
  login_pet_shop_certificate_no_id VARCHAR(3) NOT NULL,
  login_pet_shop_username VARCHAR(40) NOT NULL,
  login_pet_shop_password VARCHAR(20) NOT NULL,
  FOREIGN KEY (login_pet_shop_certificate_no_id) REFERENCES PET_SHOP(pet_shop_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE LOGIN_ANIMAL_SHELTER (
  login_animal_shelter_certificate_no_id VARCHAR(2) NOT NULL,
  login_animal_shelter_username VARCHAR(40) NOT NULL,
  login_animal_shelter_password VARCHAR(20) NOT NULL,
  FOREIGN KEY (login_animal_shelter_certificate_no_id) REFERENCES ANIMAL_SHELTER(animal_shelter_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE LOGIN_DOCTORS (
  login_doctor_certificate_no_id VARCHAR(50) NOT NULL,
  login_doctor_username VARCHAR(40) NOT NULL,
  login_doctor_password VARCHAR(20) NOT NULL,
  FOREIGN KEY (login_doctor_certificate_no_id) REFERENCES DOCTORS(doctor_certificate_no) ON UPDATE CASCADE ON DELETE CASCADE
);
