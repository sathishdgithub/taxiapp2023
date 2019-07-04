--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.12
-- Dumped by pg_dump version 9.6.12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: taxiapp_city_code; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxiapp_city_code (
    id integer NOT NULL,
    city character varying(40) NOT NULL,
    city_code character varying(10) NOT NULL,
    whatsapp boolean NOT NULL,
    sms boolean NOT NULL,
    distress boolean NOT NULL,
    distress_contact character varying(13),
    taxi_no bigint NOT NULL,
    police_no bigint NOT NULL,
    complaint_no bigint NOT NULL
);


ALTER TABLE public.taxiapp_city_code OWNER TO postgres;

--
-- Name: taxiapp_city_code_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxiapp_city_code_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taxiapp_city_code_id_seq OWNER TO postgres;

--
-- Name: taxiapp_city_code_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxiapp_city_code_id_seq OWNED BY public.taxiapp_city_code.id;


--
-- Name: taxiapp_complaint_statement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxiapp_complaint_statement (
    id integer NOT NULL,
    complaint_number character varying(20) NOT NULL,
    area character varying(200) NOT NULL,
    origin_area character varying(200),
    destination_area character varying(200),
    phone_number character varying(13) NOT NULL,
    complaint character varying(100),
    resolved boolean NOT NULL,
    assigned_to_id integer,
    city_id integer NOT NULL,
    reason_id integer NOT NULL,
    taxi_id integer
);


ALTER TABLE public.taxiapp_complaint_statement OWNER TO postgres;

--
-- Name: taxiapp_complaint_statement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxiapp_complaint_statement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taxiapp_complaint_statement_id_seq OWNER TO postgres;

--
-- Name: taxiapp_complaint_statement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxiapp_complaint_statement_id_seq OWNED BY public.taxiapp_complaint_statement.id;


--
-- Name: taxiapp_myuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxiapp_myuser (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    user_number character varying(20),
    email character varying(255) NOT NULL,
    sms_number bigint,
    whatsapp_number bigint,
    area character varying(200) NOT NULL,
    location character varying(63),
    is_active boolean NOT NULL,
    is_admin boolean NOT NULL,
    is_staff boolean NOT NULL,
    city_id integer
);


ALTER TABLE public.taxiapp_myuser OWNER TO postgres;

--
-- Name: taxiapp_myuser_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxiapp_myuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taxiapp_myuser_id_seq OWNER TO postgres;

--
-- Name: taxiapp_myuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxiapp_myuser_id_seq OWNED BY public.taxiapp_myuser.id;


--
-- Name: taxiapp_otp_codes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxiapp_otp_codes (
    id integer NOT NULL,
    otp character varying(6) NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id integer
);


ALTER TABLE public.taxiapp_otp_codes OWNER TO postgres;

--
-- Name: taxiapp_otp_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxiapp_otp_codes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taxiapp_otp_codes_id_seq OWNER TO postgres;

--
-- Name: taxiapp_otp_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxiapp_otp_codes_id_seq OWNED BY public.taxiapp_otp_codes.id;


--
-- Name: taxiapp_reasons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxiapp_reasons (
    id integer NOT NULL,
    reason character varying(100) NOT NULL
);


ALTER TABLE public.taxiapp_reasons OWNER TO postgres;

--
-- Name: taxiapp_reasons_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxiapp_reasons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taxiapp_reasons_id_seq OWNER TO postgres;

--
-- Name: taxiapp_reasons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxiapp_reasons_id_seq OWNED BY public.taxiapp_reasons.id;


--
-- Name: taxiapp_taxi_detail; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxiapp_taxi_detail (
    id integer NOT NULL,
    number_plate character varying(24) NOT NULL,
    traffic_number character varying(28) NOT NULL,
    driver_name character varying(40) NOT NULL,
    son_of character varying(40) NOT NULL,
    date_of_birth date,
    phone_number character varying(16) NOT NULL,
    address character varying(200) NOT NULL,
    aadhar_number character varying(22),
    driving_license_number character varying(30),
    date_of_validity date,
    autostand character varying(80),
    "union" character varying(100),
    insurance date,
    capacity_of_passengers character varying(14),
    pollution date,
    engine_number character varying(40),
    chasis_number character varying(30),
    owner_driver character varying(6),
    num_of_complaints bigint NOT NULL,
    driver_image character varying(100) NOT NULL,
    qr_code character varying(100),
    driver_image_name character varying(100),
    city_id integer NOT NULL
);


ALTER TABLE public.taxiapp_taxi_detail OWNER TO postgres;

--
-- Name: taxiapp_taxi_detail_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxiapp_taxi_detail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taxiapp_taxi_detail_id_seq OWNER TO postgres;

--
-- Name: taxiapp_taxi_detail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxiapp_taxi_detail_id_seq OWNED BY public.taxiapp_taxi_detail.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: taxiapp_city_code id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_city_code ALTER COLUMN id SET DEFAULT nextval('public.taxiapp_city_code_id_seq'::regclass);


--
-- Name: taxiapp_complaint_statement id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_complaint_statement ALTER COLUMN id SET DEFAULT nextval('public.taxiapp_complaint_statement_id_seq'::regclass);


--
-- Name: taxiapp_myuser id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_myuser ALTER COLUMN id SET DEFAULT nextval('public.taxiapp_myuser_id_seq'::regclass);


--
-- Name: taxiapp_otp_codes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_otp_codes ALTER COLUMN id SET DEFAULT nextval('public.taxiapp_otp_codes_id_seq'::regclass);


--
-- Name: taxiapp_reasons id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_reasons ALTER COLUMN id SET DEFAULT nextval('public.taxiapp_reasons_id_seq'::regclass);


--
-- Name: taxiapp_taxi_detail id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_taxi_detail ALTER COLUMN id SET DEFAULT nextval('public.taxiapp_taxi_detail_id_seq'::regclass);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: taxiapp_city_code taxiapp_city_code_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_city_code
    ADD CONSTRAINT taxiapp_city_code_pkey PRIMARY KEY (id);


--
-- Name: taxiapp_complaint_statement taxiapp_complaint_statement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_complaint_statement
    ADD CONSTRAINT taxiapp_complaint_statement_pkey PRIMARY KEY (id);


--
-- Name: taxiapp_myuser taxiapp_myuser_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_myuser
    ADD CONSTRAINT taxiapp_myuser_email_key UNIQUE (email);


--
-- Name: taxiapp_myuser taxiapp_myuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_myuser
    ADD CONSTRAINT taxiapp_myuser_pkey PRIMARY KEY (id);


--
-- Name: taxiapp_otp_codes taxiapp_otp_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_otp_codes
    ADD CONSTRAINT taxiapp_otp_codes_pkey PRIMARY KEY (id);


--
-- Name: taxiapp_reasons taxiapp_reasons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_reasons
    ADD CONSTRAINT taxiapp_reasons_pkey PRIMARY KEY (id);


--
-- Name: taxiapp_taxi_detail taxiapp_taxi_detail_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_taxi_detail
    ADD CONSTRAINT taxiapp_taxi_detail_pkey PRIMARY KEY (id);


--
-- Name: taxiapp_taxi_detail taxiapp_taxi_detail_traffic_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_taxi_detail
    ADD CONSTRAINT taxiapp_taxi_detail_traffic_number_key UNIQUE (traffic_number);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_0e939a4f ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_8373b171 ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_417f1b1c ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_de54fa62 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: taxiapp_complaint_statement_02c1725c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_complaint_statement_02c1725c ON public.taxiapp_complaint_statement USING btree (assigned_to_id);


--
-- Name: taxiapp_complaint_statement_5ad5b844; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_complaint_statement_5ad5b844 ON public.taxiapp_complaint_statement USING btree (reason_id);


--
-- Name: taxiapp_complaint_statement_606854bb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_complaint_statement_606854bb ON public.taxiapp_complaint_statement USING btree (taxi_id);


--
-- Name: taxiapp_complaint_statement_c7141997; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_complaint_statement_c7141997 ON public.taxiapp_complaint_statement USING btree (city_id);


--
-- Name: taxiapp_myuser_c7141997; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_myuser_c7141997 ON public.taxiapp_myuser USING btree (city_id);


--
-- Name: taxiapp_myuser_email_18b21411_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_myuser_email_18b21411_like ON public.taxiapp_myuser USING btree (email varchar_pattern_ops);


--
-- Name: taxiapp_otp_codes_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_otp_codes_e8701ad4 ON public.taxiapp_otp_codes USING btree (user_id);


--
-- Name: taxiapp_taxi_detail_c7141997; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_taxi_detail_c7141997 ON public.taxiapp_taxi_detail USING btree (city_id);


--
-- Name: taxiapp_taxi_detail_traffic_number_5d70e859_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taxiapp_taxi_detail_traffic_number_5d70e859_like ON public.taxiapp_taxi_detail USING btree (traffic_number varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_taxiapp_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_taxiapp_myuser_id FOREIGN KEY (user_id) REFERENCES public.taxiapp_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taxiapp_complaint_statement taxiapp_complaint__assigned_to_id_d9a47266_fk_taxiapp_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_complaint_statement
    ADD CONSTRAINT taxiapp_complaint__assigned_to_id_d9a47266_fk_taxiapp_myuser_id FOREIGN KEY (assigned_to_id) REFERENCES public.taxiapp_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taxiapp_complaint_statement taxiapp_complaint_st_taxi_id_642f20e1_fk_taxiapp_taxi_detail_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_complaint_statement
    ADD CONSTRAINT taxiapp_complaint_st_taxi_id_642f20e1_fk_taxiapp_taxi_detail_id FOREIGN KEY (taxi_id) REFERENCES public.taxiapp_taxi_detail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taxiapp_complaint_statement taxiapp_complaint_stat_city_id_0d2af32d_fk_taxiapp_city_code_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_complaint_statement
    ADD CONSTRAINT taxiapp_complaint_stat_city_id_0d2af32d_fk_taxiapp_city_code_id FOREIGN KEY (city_id) REFERENCES public.taxiapp_city_code(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taxiapp_complaint_statement taxiapp_complaint_stat_reason_id_6535f8b0_fk_taxiapp_reasons_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_complaint_statement
    ADD CONSTRAINT taxiapp_complaint_stat_reason_id_6535f8b0_fk_taxiapp_reasons_id FOREIGN KEY (reason_id) REFERENCES public.taxiapp_reasons(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taxiapp_myuser taxiapp_myuser_city_id_d39f9e69_fk_taxiapp_city_code_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_myuser
    ADD CONSTRAINT taxiapp_myuser_city_id_d39f9e69_fk_taxiapp_city_code_id FOREIGN KEY (city_id) REFERENCES public.taxiapp_city_code(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taxiapp_otp_codes taxiapp_otp_codes_user_id_fe7deef2_fk_taxiapp_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_otp_codes
    ADD CONSTRAINT taxiapp_otp_codes_user_id_fe7deef2_fk_taxiapp_myuser_id FOREIGN KEY (user_id) REFERENCES public.taxiapp_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taxiapp_taxi_detail taxiapp_taxi_detail_city_id_12aad47a_fk_taxiapp_city_code_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxiapp_taxi_detail
    ADD CONSTRAINT taxiapp_taxi_detail_city_id_12aad47a_fk_taxiapp_city_code_id FOREIGN KEY (city_id) REFERENCES public.taxiapp_city_code(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

