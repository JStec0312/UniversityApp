INSERT INTO universities (name) VALUES 
('Politechnika Łódzka'),
('Uniwersytet Warszawski'),
('AGH');

INSERT INTO faculties (name, university_id) VALUES
('Wydział Elektrotechniki, Elektroniki, Informatyki i Automatyki', 1),
('Wydział Zarządzania', 1),
('Wydział Matematyki, Informatyki i Mechaniki', 2),
('Wydział Geologii, Geofizyki i Ochrony Środowiska', 3);

INSERT INTO majors (name, faculty_id) VALUES
('Informatyka', 1),
('Automatyka i Robotyka', 1),
('Zarządzanie', 2),
('Matematyka', 3),
('Geoinżynieria', 4);
