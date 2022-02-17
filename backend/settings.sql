CREATE DATABASE my_demo_auth;
CREATE USER auth_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE my_demo_auth TO auth_user;
ALTER USER auth_user CREATEDB; -- to allow tests to run