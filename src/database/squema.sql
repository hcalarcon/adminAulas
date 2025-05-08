-- Tabla de usuarios: profesores y alumnos
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT CHECK (role IN ('student', 'teacher')) NOT NULL
);

-- Tabla de aulas o materias
CREATE TABLE classrooms (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- Tabla intermedia para asignar alumnos a aulas
CREATE TABLE student_classroom (
    student_id INTEGER NOT NULL,
    classroom_id INTEGER NOT NULL,
    PRIMARY KEY (student_id, classroom_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
);

-- Tabla de sesiones o clases
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    classroom_id INTEGER NOT NULL,
    topic TEXT NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
);

-- Tabla de asistencia de alumnos a clases
CREATE TABLE attendance (
    student_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    present BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (student_id, session_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
