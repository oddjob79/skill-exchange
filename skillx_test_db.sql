--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET SQL_USER = 'udacity'

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: SQL_USER
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO SQL_USER;

--
-- Name: mem_skills_held; Type: TABLE; Schema: public; Owner: SQL_USER
--

CREATE TABLE public.mem_skills_held (
    member_id integer NOT NULL,
    skill_id integer NOT NULL
);


ALTER TABLE public.mem_skills_held OWNER TO SQL_USER;

--
-- Name: mem_skills_wanted; Type: TABLE; Schema: public; Owner: SQL_USER
--

CREATE TABLE public.mem_skills_wanted (
    member_id integer NOT NULL,
    skill_id integer NOT NULL
);


ALTER TABLE public.mem_skills_wanted OWNER TO SQL_USER;

--
-- Name: members; Type: TABLE; Schema: public; Owner: SQL_USER
--

CREATE TABLE public.members (
    id integer NOT NULL,
    name character varying NOT NULL,
    location character varying NOT NULL,
    gender character varying(10) NOT NULL,
    match_location boolean NOT NULL,
    user_id character varying NOT NULL
);


ALTER TABLE public.members OWNER TO SQL_USER;

--
-- Name: members_id_seq; Type: SEQUENCE; Schema: public; Owner: SQL_USER
--

CREATE SEQUENCE public.members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.members_id_seq OWNER TO SQL_USER;

--
-- Name: members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: SQL_USER
--

ALTER SEQUENCE public.members_id_seq OWNED BY public.members.id;


--
-- Name: skills; Type: TABLE; Schema: public; Owner: SQL_USER
--

CREATE TABLE public.skills (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    equipment_reqd character varying,
    category character varying(20)
);


ALTER TABLE public.skills OWNER TO SQL_USER;

--
-- Name: skills_id_seq; Type: SEQUENCE; Schema: public; Owner: SQL_USER
--

CREATE SEQUENCE public.skills_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skills_id_seq OWNER TO SQL_USER;

--
-- Name: skills_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: SQL_USER
--

ALTER SEQUENCE public.skills_id_seq OWNED BY public.skills.id;


--
-- Name: members id; Type: DEFAULT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.members ALTER COLUMN id SET DEFAULT nextval('public.members_id_seq'::regclass);


--
-- Name: skills id; Type: DEFAULT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.skills ALTER COLUMN id SET DEFAULT nextval('public.skills_id_seq'::regclass);


--
-- Name: skills _sk_name_uc; Type: CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT _sk_name_uc UNIQUE (name);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: mem_skills_held mem_skills_held_pkey; Type: CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.mem_skills_held
    ADD CONSTRAINT mem_skills_held_pkey PRIMARY KEY (member_id, skill_id);


--
-- Name: mem_skills_wanted mem_skills_wanted_pkey; Type: CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.mem_skills_wanted
    ADD CONSTRAINT mem_skills_wanted_pkey PRIMARY KEY (member_id, skill_id);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);


--
-- Name: members members_user_id_key; Type: CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_user_id_key UNIQUE (user_id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- Name: mem_skills_held mem_skills_held_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.mem_skills_held
    ADD CONSTRAINT mem_skills_held_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id) ON DELETE CASCADE;


--
-- Name: mem_skills_held mem_skills_held_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.mem_skills_held
    ADD CONSTRAINT mem_skills_held_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id) ON DELETE CASCADE;


--
-- Name: mem_skills_wanted mem_skills_wanted_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.mem_skills_wanted
    ADD CONSTRAINT mem_skills_wanted_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id) ON DELETE CASCADE;


--
-- Name: mem_skills_wanted mem_skills_wanted_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: SQL_USER
--

ALTER TABLE ONLY public.mem_skills_wanted
    ADD CONSTRAINT mem_skills_wanted_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


INSERT INTO public.skills (name, description, category, equipment_reqd)
VALUES (
'English',
'Learn to speak the English language',
'languages',
'none'
),
(
'Swimming',
'Learn to swim',
'sports',
'swimsuit, goggles'
),
(
'Piano',
'Learn to play the piano',
'musical instrument',
'keyboard or piano'
),
(
'Chinese cooking',
'Learn 5 Chinese recipes',
'cooking',
'ingredients and kitchen utensils'
);

INSERT INTO public.members
(name, location, gender, match_location, user_id)
VALUES (
'benny',
'Sweden',
'Male',
false,
'5dd3f103a072d20f12a11e3c'
);
