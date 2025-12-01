-- Create the database
CREATE DATABASE IF NOT EXISTS mydb;
-- Select the database
USE
    mydb;
    -- Create the user table with timestamp
CREATE TABLE tbl_user(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    PASSWORD VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);