-- already ran this file so data is in tables!!

use cwise_db;

INSERT INTO user(name, email, password)
VALUES 
("Vaishu Chintam", "jc103@wellesley.edu", "password"),
("Mukhlisa Nematova", "mn109@wellesley.edu", "password"),
("Kathy Yang", "ky107@wellesley.edu", "password"),
("Ashley You", "ay106@wellesley.edu", "password");


INSERT INTO department(name)
VALUES 
("Africana Studies"), ("American Studies"), ("Anthropology"), ("Arabic"), ("Art Department"), ("Art History"), ("Art-Studio"), ("Astronomy"),("Biochemistry"),("Biological Sciences"),("Chemistry"),("Chinese Language and Culture"),("Cinema and Media Studies"),("Classical Civilization"),("Classical Studies Department"),("Cognitive and Linguistic Sci"),("Comparative Literature"),("Computer Science"),("East Asian Languages and Cultures"),("Economics"),("Education"),("Engineering"),("English"),("Environmental Studies"),("French"),("Geosciences"),("German"),("Greek"),("Hindi/Urdu"),("History"),("Italian Studies"),("Japanese Language and Culture"),("Jewish Studies"),("Korean Language and Culture"),("Latin"),("Latin American Studies"), ("Linguistics"), ("Mathematics"), ("Media Arts & Sciences"), ("Medieval/Ren Studies"), ("Middle Eastern Studies"), ("Music"), ("Neuroscience"), ("Peace and Justice Studies"), ("Philosophy"), ("Physical Education"), ("Physics"), ("Political Science"),("Portuguese"), ("Psychology"), ("Quantitative Reasoning"), ("Religion"), ("Russian"), ("Russian Area Studies"), ("Sociology"), ("South Asia Studies Program"), ("Spanish"), ("Statistics"), ("Theatre Studies"), ("Women's and Gender Studies"), ("Writing");

INSERT INTO course(did, course_code, name)
VALUES
(18, "CS 111","Computer Programming and Problem Solving"),
(18, "CS 230","Data Structures"),
(18, "CS 231","Fundamental Algorithms"),
(18, "CS 235","Theory of Computation"),
(18, "CS 240","Foundations of Computer Systems with Laboratory"),
(18, "CS 304","Databases with Web Interfaces");

INSERT INTO professor(name, department_id)
VALUES 
("Scott Anderson", 18),
("Peter Mawhorter", 18),
("Brian Brubach", 18),
("Alexa VanHattum", 18),
("Smaranda Sandu", 18),
("Catherine Delcourt", 18),
("Christine Bassem", 18),
("Franklyn Turbak", 18),
("Yaniv Yacoby", 18),
("Eni Mustafaraj", 18),
("Vinitha Gadiraju", 18),
("Orit Shaer", 18),
("Brian Tjaden", 18),
("Stella Kakavouli", 18),
("Carolyn Anderson", 18),
("Sohie Lee", 18),
("Sara Melnick", 18),
("Panagiotis Metaxas", 18),
("Jordan Tynes", 18);

INSERT INTO review(course_id, user_id, difficulty, credit, prof_name, prof_id, prof_rating, sem, year, take_again, load_heavy, office_hours, helped_learn, stim_interest, description)
VALUES 
(6, 1, "Medium", "Credit", "Scott Anderson", 1, "5", "Fall", "2020", "Yes", "Medium", "Need to Schedule", "Yes", "Yes", "So much fun!"),
(4, 1, "Medium", "Credit", "Smaranda Sandu", 5, "5", "Spring", "2021", "Yes", "Medium", "Sometimes Available", "Yes", "Yes", "Kinda confusing but interesting! Get ready to go to office hours.");
