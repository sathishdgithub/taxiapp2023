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
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
1	Test
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	contenttypes	contenttype
5	sessions	session
6	sites	site
7	taxiapp	complaint_statement
8	taxiapp	otp_codes
9	taxiapp	taxi_detail
10	taxiapp	myuser
11	taxiapp	reasons
12	taxiapp	city_code
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add permission	3	add_permission
8	Can change permission	3	change_permission
9	Can delete permission	3	delete_permission
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add site	6	add_site
17	Can change site	6	change_site
18	Can delete site	6	delete_site
19	Can add Customer Complaint	7	add_complaint_statement
20	Can change Customer Complaint	7	change_complaint_statement
21	Can delete Customer Complaint	7	delete_complaint_statement
22	Can add OTP Code	8	add_otp_codes
23	Can change OTP Code	8	change_otp_codes
24	Can delete OTP Code	8	delete_otp_codes
25	Can add Driver/Owner	9	add_taxi_detail
26	Can change Driver/Owner	9	change_taxi_detail
27	Can delete Driver/Owner	9	delete_taxi_detail
28	Can add Administrator	10	add_myuser
29	Can change Administrator	10	change_myuser
30	Can delete Administrator	10	delete_myuser
31	Can add Complaint Reason	11	add_reasons
32	Can change Complaint Reason	11	change_reasons
33	Can delete Complaint Reason	11	delete_reasons
34	Can add City Code	12	add_city_code
35	Can change City Code	12	change_city_code
36	Can delete City Code	12	delete_city_code
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	1	1
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 36, true);


--
-- Data for Name: taxiapp_city_code; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taxiapp_city_code (id, city, city_code, whatsapp, sms, distress, distress_contact, taxi_no, police_no, complaint_no) FROM stdin;
5	Chennai	MAS	t	t	f	\N	0	0	0
3	Hyderabad	HYD	t	t	f	\N	4	0	0
4	Bangalore	SBC	t	t	f	\N	1	0	0
\.


--
-- Data for Name: taxiapp_myuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taxiapp_myuser (id, password, last_login, user_number, email, sms_number, whatsapp_number, area, location, is_active, is_admin, is_staff, city_id) FROM stdin;
2	pbkdf2_sha256$36000$6DGTLxCoJTak$aLn99ZOvyssXh2bvT1tG4XpmO7TYzVXzEYSxpl8K2Uk=	2019-05-25 12:41:11.309+05:30	\N	sana@gmail.com	\N	\N		\N	t	t	t	\N
3	pbkdf2_sha256$36000$oi0vtj9EOMSz$ef14f4sIZGYpovytlwjfXKDvTHPMjoOznP51HIU1h8o=	2019-05-01 18:44:32.144+05:30	SBC-ID-0001	sana1@gmail.com	9856520000	\N	Bangalore		t	t	t	4
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2019-04-26 09:20:41.525+05:30	3	HYD Hyderabad	1	[{"added": {}}]	12	2
2	2019-04-26 09:22:31.18+05:30	4	SBC Bangalore	1	[{"added": {}}]	12	2
3	2019-04-26 09:22:57.881+05:30	5	MAS Chennai	1	[{"added": {}}]	12	2
4	2019-04-26 15:36:08.522+05:30	7	Sanjeeva(TS03CM5263)	1	[{"added": {}}]	9	2
5	2019-04-26 15:42:46.346+05:30	1	drunk and drive	1	[{"added": {}}]	11	2
6	2019-04-26 15:43:06.831+05:30	1	HYD-CN-0001 Sanjeeva drunk and drive	1	[{"added": {}}]	7	2
7	2019-04-26 16:15:03.172+05:30	9	Sanjeeva Reddy(TS03CM5264)	1	[{"added": {}}]	9	2
8	2019-04-27 22:28:34.43+05:30	2	HYD-CN-0002 Sanjeeva drunk and drive	1	[{"added": {}}]	7	2
9	2019-04-27 22:29:02.223+05:30	2	signal jumping	1	[{"added": {}}]	11	2
10	2019-04-27 22:29:56.833+05:30	3	sana1@gmail.com	1	[{"added": {}}]	10	2
11	2019-04-27 22:29:59.857+05:30	3	HYD-CN-0003 Sanjeeva Reddy signal jumping	1	[{"added": {}}]	7	2
12	2019-05-24 17:14:25.388+05:30	7	Sanjeeva(TS03CM5263)	2	[]	9	2
13	2019-05-24 17:18:57.383+05:30	1	Vishnu(TS1234)	2	[{"changed": {"fields": ["traffic_number", "engine_number", "owner_driver"]}}]	9	2
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 13, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 12, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	taxiapp	0001_initial	2019-03-19 18:13:12.558+05:30
2	contenttypes	0001_initial	2019-03-19 18:13:12.674+05:30
3	admin	0001_initial	2019-03-19 18:13:12.861+05:30
4	admin	0002_logentry_remove_auto_add	2019-03-19 18:13:12.893+05:30
5	contenttypes	0002_remove_content_type_name	2019-03-19 18:13:12.986+05:30
6	auth	0001_initial	2019-03-19 18:13:13.519+05:30
7	auth	0002_alter_permission_name_max_length	2019-03-19 18:13:13.542+05:30
8	auth	0003_alter_user_email_max_length	2019-03-19 18:13:13.557+05:30
9	auth	0004_alter_user_username_opts	2019-03-19 18:13:13.573+05:30
10	auth	0005_alter_user_last_login_null	2019-03-19 18:13:13.604+05:30
11	auth	0006_require_contenttypes_0002	2019-03-19 18:13:13.604+05:30
12	auth	0007_alter_validators_add_error_messages	2019-03-19 18:13:13.62+05:30
13	auth	0008_alter_user_username_max_length	2019-03-19 18:13:13.635+05:30
14	sessions	0001_initial	2019-03-19 18:13:13.776+05:30
15	sites	0001_initial	2019-03-19 18:13:13.823+05:30
16	sites	0002_alter_domain_unique	2019-03-19 18:13:13.932+05:30
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 16, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
d7sgnqxtoip75zqbp7n97fjhwemb0b16	MDcwNmVlNTgyM2FjZmNhMDgzYmY2ZWNkZjdhMTFhYjVlNWVkOTA0Yjp7Il9hdXRoX3VzZXJfaGFzaCI6IjllOTAwMzYwNTU5MGEzMjc2MTg2M2YxOWRmMTcyZjU4MTQyMDRjZmQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2019-05-09 09:22:40.794+05:30
njwwcwqa12710rkgqwc3chh970vl8kmc	ODZhYmI4NDA1NzJjMDI1NDU3OGQzMGIwNWYxOTMwZjc3YTgxMzYyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjBlNDQwYzRmYzRmNTVlY2NiOWJkNWIyY2Y4YjQyZTZmYmYxZDQ3MzkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2019-05-10 16:18:11.981+05:30
shhr92kdtz28gcmv1egldqa7eq59q7dc	ZDY2MDQ2YThiYmE3YWFlM2ExN2MyNGFmODhhMzlhN2NhYjc5NWMwYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImM2MmQzNjg5ZGNjZDVkYzg0ZGFjYjE4YTRkM2UzMzFjMTZmZWY1OTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=	2019-05-15 18:44:32.184+05:30
k9o4p8ds7sd0530f0tvtapsb08txavyy	ODZhYmI4NDA1NzJjMDI1NDU3OGQzMGIwNWYxOTMwZjc3YTgxMzYyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjBlNDQwYzRmYzRmNTVlY2NiOWJkNWIyY2Y4YjQyZTZmYmYxZDQ3MzkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2019-05-20 17:37:53.76+05:30
ayvfjanfacn9kqjhqgenohhcod1byu29	ODZhYmI4NDA1NzJjMDI1NDU3OGQzMGIwNWYxOTMwZjc3YTgxMzYyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjBlNDQwYzRmYzRmNTVlY2NiOWJkNWIyY2Y4YjQyZTZmYmYxZDQ3MzkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2019-06-07 17:13:47.44+05:30
ntg4sx0x106jdvc4utjworck89hjsmdi	ODZhYmI4NDA1NzJjMDI1NDU3OGQzMGIwNWYxOTMwZjc3YTgxMzYyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjBlNDQwYzRmYzRmNTVlY2NiOWJkNWIyY2Y4YjQyZTZmYmYxZDQ3MzkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2019-06-08 12:11:09.948+05:30
ahmsz7dkp03loc5ogsb4ezb5l8vjzxdk	ODZhYmI4NDA1NzJjMDI1NDU3OGQzMGIwNWYxOTMwZjc3YTgxMzYyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjBlNDQwYzRmYzRmNTVlY2NiOWJkNWIyY2Y4YjQyZTZmYmYxZDQ3MzkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2019-06-08 12:41:11.324+05:30
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: taxiapp_city_code_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taxiapp_city_code_id_seq', 5, true);


--
-- Data for Name: taxiapp_reasons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taxiapp_reasons (id, reason) FROM stdin;
1	drunk and drive
2	signal jumping
\.


--
-- Data for Name: taxiapp_taxi_detail; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taxiapp_taxi_detail (id, number_plate, traffic_number, driver_name, son_of, date_of_birth, phone_number, address, aadhar_number, driving_license_number, date_of_validity, autostand, "union", insurance, capacity_of_passengers, pollution, engine_number, chasis_number, owner_driver, num_of_complaints, driver_image, qr_code, driver_image_name, city_id) FROM stdin;
9	TS03CM5264	HYD-TR-00003	Sanjeeva Reddy	Sanjeeva	2019-04-26	9642153000	Kukatpally	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	OWNER	0	drivers/Screenshot_2.png	qr/HYD-TR-00003.png	\N	3
7	TS03CM5263	HYD-TR-00001	Sanjeeva	Sanjeeva	2019-04-26	9642153083	Kukatpally	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	OWNER	0	drivers/test_images/test1.jpg	qr/HYD-TR-00001.png	\N	3
1	TS1234	HYD-TR-00002	Vishnu	Sana	1989-10-08	7989893499	Hyd	782664114286	HG2015	2020-12-05	Hyd	Hyd	2019-12-04	Five	\N	\N	2012	\N	2	drivers/test_images/test2.jpg	qr/HYD-TR-00002.png	Vishnu	3
\.


--
-- Data for Name: taxiapp_complaint_statement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taxiapp_complaint_statement (id, complaint_number, area, origin_area, destination_area, phone_number, complaint, resolved, assigned_to_id, city_id, reason_id, taxi_id) FROM stdin;
1	HYD-CN-0001	Hyderabad			9642153083		f	\N	3	1	7
2	HYD-CN-0002	Hyderabad	\N	\N	9642153000	\N	f	2	4	1	7
3	HYD-CN-0003	Hyderabad	\N	\N	9642153000	\N	f	3	4	2	9
\.


--
-- Name: taxiapp_complaint_statement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taxiapp_complaint_statement_id_seq', 3, true);


--
-- Name: taxiapp_myuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taxiapp_myuser_id_seq', 3, true);


--
-- Data for Name: taxiapp_otp_codes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taxiapp_otp_codes (id, otp, updated_at, user_id) FROM stdin;
\.


--
-- Name: taxiapp_otp_codes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taxiapp_otp_codes_id_seq', 5, true);


--
-- Name: taxiapp_reasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taxiapp_reasons_id_seq', 2, true);


--
-- Name: taxiapp_taxi_detail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taxiapp_taxi_detail_id_seq', 9, true);


--
-- PostgreSQL database dump complete
--

