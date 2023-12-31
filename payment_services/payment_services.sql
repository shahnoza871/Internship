-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS payment.services_data_validation
(
    phone_num character varying COLLATE pg_catalog."default" NOT NULL,
    device_info json NOT NULL,
    service_id integer NOT NULL,
    transaction_id character varying COLLATE pg_catalog."default" NOT NULL,
    input_data json NOT NULL,
    id integer NOT NULL DEFAULT nextval('payment.services_data_validation_id_seq'::regclass),
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT services_data_validation_pkey PRIMARY KEY (id)
);

COMMENT ON COLUMN payment.services_data_validation.input_data
    IS 'необходимые данные для сервиса';

CREATE TABLE IF NOT EXISTS payment.services_payments
(
    id integer NOT NULL DEFAULT nextval('payment.services_payments_id_seq'::regclass),
    service_id integer NOT NULL,
    amount numeric(15, 2) NOT NULL,
    transaction_id character varying COLLATE pg_catalog."default" NOT NULL,
    input_data json NOT NULL,
    result integer,
    massage character varying COLLATE pg_catalog."default",
    code integer,
    description text COLLATE pg_catalog."default",
    amount_received numeric(15, 2),
    amount_sent numeric(15, 2),
    terminal_commission numeric(15, 2),
    service_fee numeric(15, 2),
    reference_no character varying COLLATE pg_catalog."default",
    state integer,
    phone_num character varying COLLATE pg_catalog."default" NOT NULL,
    device_info json NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT payment_service_pkey PRIMARY KEY (id)
);

COMMENT ON COLUMN payment.services_payments.id
    IS 'Uniquely generated for each customer.';

COMMENT ON COLUMN payment.services_payments.service_id
    IS 'ID сервис';

COMMENT ON COLUMN payment.services_payments.amount
    IS 'Сумма к оплате.';

COMMENT ON COLUMN payment.services_payments.transaction_id
    IS 'ID транзакции';

COMMENT ON COLUMN payment.services_payments.input_data
    IS 'Hеобходимые данные для сервиса (json)';

COMMENT ON COLUMN payment.services_payments.result
    IS 'Kод результата';

COMMENT ON COLUMN payment.services_payments.massage
    IS 'Tекст ответа';

COMMENT ON COLUMN payment.services_payments.code
    IS 'Koд ответа';

COMMENT ON COLUMN payment.services_payments.description
    IS 'Описание ответа';

COMMENT ON COLUMN payment.services_payments.amount_received
    IS 'полученная сумма';

COMMENT ON COLUMN payment.services_payments.amount_sent
    IS 'отправленная сумма';

COMMENT ON COLUMN payment.services_payments.service_fee
    IS 'комиссия за услугу';

COMMENT ON COLUMN payment.services_payments.state
    IS 'Статус транзакции';

CREATE TABLE IF NOT EXISTS payment.sessions
(
    phone_num character varying COLLATE pg_catalog."default" NOT NULL,
    device_info json NOT NULL,
    login_at timestamp with time zone NOT NULL,
    logout_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id integer NOT NULL DEFAULT nextval('payment.sessions_id_seq'::regclass),
    CONSTRAINT sessions_pkey PRIMARY KEY (id)
);

COMMENT ON COLUMN payment.sessions.login_at
    IS 'время входа';

COMMENT ON COLUMN payment.sessions.logout_at
    IS 'время выхода';

COMMENT ON COLUMN payment.sessions.created_at
    IS 'время запроса';

CREATE TABLE IF NOT EXISTS payment.users
(
    phone_num character varying COLLATE pg_catalog."default" NOT NULL,
    device_info json NOT NULL,
    id integer NOT NULL DEFAULT nextval('payment.users_id_seq'::regclass),
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);

COMMENT ON COLUMN payment.users.phone_num
    IS 'номер телефона';

COMMENT ON COLUMN payment.users.device_info
    IS 'модель телефона пользователя';
END;