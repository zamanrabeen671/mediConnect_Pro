USE medi_connect_pro;

-- ---------------------
-- Table: users
-- ---------------------
CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) UNIQUE,
  `password` VARCHAR(255),
  `role` ENUM('doctor','patient','admin') NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

-- ---------------------
-- Table: blood_groups
-- ---------------------
CREATE TABLE `blood_groups` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `group_name` VARCHAR(10) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
);

-- ---------------------
-- Table: doctors
-- ---------------------
CREATE TABLE `doctors` (
  `id` INT NOT NULL,
  `full_name` VARCHAR(120) NOT NULL,
  `phone` VARCHAR(20) NOT NULL UNIQUE,
  `chamber` VARCHAR(256),
  `bmdc_number` VARCHAR(20) UNIQUE,
  `experience` VARCHAR(20),
  `consultation_fee` VARCHAR(20),
  `status` ENUM('pending','approved','rejected','blocked') DEFAULT 'pending',
  PRIMARY KEY (`id`),
  FOREIGN KEY (`id`) REFERENCES `users` (`id`)
);

-- ---------------------
-- Table: patients
-- ---------------------
CREATE TABLE `patients` (
  `id` INT NOT NULL,
  `full_name` VARCHAR(120),
  `age` INT,
  `gender` VARCHAR(20),
  `phone` VARCHAR(20),
  `blood_group_id` INT,
  `address` VARCHAR(256),
  `serial_number` INT UNIQUE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`blood_group_id`) REFERENCES `blood_groups` (`id`)
);

-- ---------------------
-- Table: specializations
-- ---------------------
CREATE TABLE `specializations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
);

-- ---------------------
-- Table: institutes
-- ---------------------
CREATE TABLE `institutes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL UNIQUE,
  `address` VARCHAR(255),
  PRIMARY KEY (`id`)
);

-- ---------------------
-- Table: qualifications
-- ---------------------
CREATE TABLE `qualifications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
);

-- ---------------------
-- Table: doctor_specializations
-- ---------------------
CREATE TABLE `doctor_specializations` (
  `doctor_id` INT NOT NULL,
  `specialization_id` INT NOT NULL,
  PRIMARY KEY (`doctor_id`, `specialization_id`),
  FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`),
  FOREIGN KEY (`specialization_id`) REFERENCES `specializations` (`id`)
);

-- ---------------------
-- Table: doctor_institutes
-- ---------------------
CREATE TABLE `doctor_institutes` (
  `doctor_id` INT NOT NULL,
  `institute_id` INT NOT NULL,
  PRIMARY KEY (`doctor_id`, `institute_id`),
  FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`),
  FOREIGN KEY (`institute_id`) REFERENCES `institutes` (`id`)
);

-- ---------------------
-- Table: doctor_qualifications
-- ---------------------
CREATE TABLE `doctor_qualifications` (
  `doctor_id` INT NOT NULL,
  `qualification_id` INT NOT NULL,
  PRIMARY KEY (`doctor_id`, `qualification_id`),
  FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`),
  FOREIGN KEY (`qualification_id`) REFERENCES `qualifications` (`id`)
);

-- ---------------------
-- Table: doctor_schedules
-- ---------------------
CREATE TABLE `doctor_schedules` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `doctor_id` INT NOT NULL,
  `day_of_week` VARCHAR(50),
  `start_time` TIME,
  `end_time` TIME,
  `max_patients` INT,
  `duration_per_appointment` INT DEFAULT 30,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`)
);

-- ---------------------
-- Table: appointments
-- ---------------------
CREATE TABLE `appointments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `doctor_id` INT NOT NULL,
  `patient_id` INT NOT NULL,
  `schedule_id` INT,
  `appointment_date` DATE,
  `appointment_time` TIME,
  `status` ENUM('pending','confirmed','completed','cancelled') DEFAULT 'pending',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`),
  FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  FOREIGN KEY (`schedule_id`) REFERENCES `doctor_schedules` (`id`)
);

-- ---------------------
-- Table: prescriptions
-- ---------------------
CREATE TABLE `prescriptions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `appointment_id` INT NOT NULL UNIQUE,
  `patient_id` INT,
  `notes` TEXT,
  `document_path` VARCHAR(255),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`),
  FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`)
);

-- ---------------------
-- Table: medicines
-- ---------------------
CREATE TABLE `medicines` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  `strength` VARCHAR(50),
  `form` VARCHAR(50),
  `manufacturer` VARCHAR(150),
  PRIMARY KEY (`id`)
);

-- ---------------------
-- Table: prescription_medicines
-- ---------------------
CREATE TABLE `prescription_medicines` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `prescription_id` INT NOT NULL,
  `medicine_id` INT NOT NULL,
  `dosage` VARCHAR(50),
  `duration` VARCHAR(50),
  `instruction` VARCHAR(255),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`prescription_id`) REFERENCES `prescriptions` (`id`),
  FOREIGN KEY (`medicine_id`) REFERENCES `medicines` (`id`)
);

INSERT INTO medicines (name, strength, form, manufacturer) VALUES
('Paracetamol', '500mg', 'Tablet', 'Eskayef'),
('Amoxicillin', '250mg', 'Capsule', 'Square Pharmaceuticals'),
('Azithromycin', '500mg', 'Tablet', 'Beximco Pharma'),
('Ibuprofen', '400mg', 'Tablet', 'ACI Limited'),
('Omeprazole', '20mg', 'Capsule', 'Renata Limited'),
('Metformin', '500mg', 'Tablet', 'Incepta Pharma'),
('Cetirizine', '10mg', 'Tablet', 'Eskayef'),
('Diclofenac', '50mg', 'Tablet', 'ACI Limited'),
('Ranitidine', '150mg', 'Tablet', 'Beximco Pharma'),
('Cefixime', '200mg', 'Capsule', 'Renata Limited'),
('Paracetamol Syrup', '120mg/5ml', 'Syrup', 'Eskayef'),
('Amoxicillin Syrup', '125mg/5ml', 'Syrup', 'Incepta Pharma'),
('Salbutamol', '100mcg', 'Inhaler', 'Beximco Pharma'),
('Prednisolone', '5mg', 'Tablet', 'Renata Limited'),
('Losartan', '50mg', 'Tablet', 'ACI Limited'),
('Amlodipine', '5mg', 'Tablet', 'Eskayef'),
('Captopril', '25mg', 'Tablet', 'Incepta Pharma'),
('Hydrochlorothiazide', '25mg', 'Tablet', 'Beximco Pharma'),
('Levocetirizine', '5mg', 'Tablet', 'Renata Limited'),
('Clindamycin', '300mg', 'Capsule', 'ACI Limited'),
('Cefuroxime', '250mg', 'Tablet', 'Eskayef'),
('Azithromycin Syrup', '200mg/5ml', 'Syrup', 'Incepta Pharma'),
('Metronidazole', '400mg', 'Tablet', 'Beximco Pharma'),
('Doxycycline', '100mg', 'Capsule', 'Renata Limited'),
('Vitamin C', '500mg', 'Tablet', 'ACI Limited'),
('Paracetamol 650mg', '650mg', 'Tablet', 'Eskayef'),
('Fexofenadine', '120mg', 'Tablet', 'Beximco Pharma'),
('Levothyroxine', '50mcg', 'Tablet', 'Renata Limited'),
('Omeprazole 40mg', '40mg', 'Capsule', 'ACI Limited'),
('Pantoprazole', '40mg', 'Tablet', 'Eskayef'),
('Tramadol', '50mg', 'Tablet', 'Incepta Pharma'),
('Gabapentin', '300mg', 'Capsule', 'Beximco Pharma'),
('Ceftriaxone', '1g', 'Injection', 'Renata Limited'),
('Diclofenac Injection', '75mg', 'Injection', 'ACI Limited'),
('Salbutamol Syrup', '2mg/5ml', 'Syrup', 'Eskayef'),
('Prednisolone Syrup', '5mg/5ml', 'Syrup', 'Beximco Pharma'),
('Lorazepam', '1mg', 'Tablet', 'Renata Limited'),
('Diazepam', '5mg', 'Tablet', 'Incepta Pharma'),
('Metformin XR', '500mg', 'Tablet', 'ACI Limited'),
('Atorvastatin', '10mg', 'Tablet', 'Eskayef'),
('Simvastatin', '20mg', 'Tablet', 'Beximco Pharma'),
('Alprazolam', '0.5mg', 'Tablet', 'Renata Limited'),
('Montelukast', '10mg', 'Tablet', 'ACI Limited'),
('Clopidogrel', '75mg', 'Tablet', 'Eskayef'),
('Rivaroxaban', '10mg', 'Tablet', 'Beximco Pharma'),
('Warfarin', '5mg', 'Tablet', 'Renata Limited'),
('Enalapril', '10mg', 'Tablet', 'ACI Limited'),
('Metoprolol', '50mg', 'Tablet', 'Eskayef'),
('Bisoprolol', '5mg', 'Tablet', 'Beximco Pharma'),
('Losartan 100mg', '100mg', 'Tablet', 'Renata Limited'),
('Hydrochlorothiazide 50mg', '50mg', 'Tablet', 'ACI Limited'),
('Pantoprazole IV', '40mg', 'Injection', 'Eskayef'),
('Cefixime Suspension', '100mg/5ml', 'Syrup', 'Beximco Pharma'),
('Azithromycin 250mg', '250mg', 'Tablet', 'Renata Limited'),
('Cefuroxime Injection', '500mg', 'Injection', 'ACI Limited'),
('Diclofenac Gel', '1%', 'Gel', 'Eskayef'),
('Hydrocortisone Cream', '1%', 'Cream', 'Beximco Pharma'),
('Betamethasone Cream', '0.05%', 'Cream', 'Renata Limited'),
('Amoxicillin 500mg', '500mg', 'Capsule', 'Incepta Pharma'),
('Levofloxacin', '500mg', 'Tablet', 'ACI Limited'),
('Cefpodoxime', '200mg', 'Tablet', 'Eskayef'),
('Cefixime 200mg', '200mg', 'Tablet', 'Beximco Pharma'),
('Metronidazole Gel', '1%', 'Gel', 'Renata Limited'),
('Omeprazole SR', '20mg', 'Tablet', 'ACI Limited'),
('Pantoprazole SR', '40mg', 'Tablet', 'Eskayef'),
('Salbutamol Tablet', '4mg', 'Tablet', 'Beximco Pharma'),
('Azithromycin 500mg', '500mg', 'Tablet', 'Renata Limited'),
('Ceftriaxone 500mg', '500mg', 'Injection', 'ACI Limited'),
('Diclofenac 50mg', '50mg', 'Tablet', 'Eskayef'),
('Metformin 1000mg', '1000mg', 'Tablet', 'Beximco Pharma'),
('Amoxicillin 250mg', '250mg', 'Capsule', 'Renata Limited'),
('Levocetirizine 10mg', '10mg', 'Tablet', 'ACI Limited'),
('Cefixime 400mg', '400mg', 'Tablet', 'Eskayef'),
('Omeprazole 20mg', '20mg', 'Tablet', 'Beximco Pharma'),
('Pantoprazole 40mg', '40mg', 'Tablet', 'Renata Limited'),
('Amlodipine 10mg', '10mg', 'Tablet', 'ACI Limited'),
('Losartan 50mg', '50mg', 'Tablet', 'Eskayef'),
('Captopril 50mg', '50mg', 'Tablet', 'Beximco Pharma'),
('Hydrochlorothiazide 25mg', '25mg', 'Tablet', 'Renata Limited'),
('Clindamycin 150mg', '150mg', 'Capsule', 'ACI Limited'),
('Doxycycline 100mg', '100mg', 'Capsule', 'Eskayef'),
('Vitamin D', '2000IU', 'Tablet', 'Beximco Pharma'),
('Calcium Carbonate', '500mg', 'Tablet', 'Renata Limited'),
('Iron Tablet', '65mg', 'Tablet', 'ACI Limited'),
('Multivitamin', '1 tablet', 'Tablet', 'Eskayef'),
('Folic Acid', '400mcg', 'Tablet', 'Beximco Pharma'),
('Paracetamol 500mg', '500mg', 'Tablet', 'Renata Limited'),
('Metformin 500mg', '500mg', 'Tablet', 'ACI Limited'),
('Aspirin', '75mg', 'Tablet', 'Eskayef'),
('Omeprazole 20mg', '20mg', 'Tablet', 'Beximco Pharma'),
('Ranitidine 150mg', '150mg', 'Tablet', 'Renata Limited'),
('Cetirizine 10mg', '10mg', 'Tablet', 'ACI Limited'),
('Levothyroxine 50mcg', '50mcg', 'Tablet', 'Eskayef'),
('Atorvastatin 20mg', '20mg', 'Tablet', 'Beximco Pharma'),
('Simvastatin 20mg', '20mg', 'Tablet', 'Renata Limited'),
('Montelukast 10mg', '10mg', 'Tablet', 'ACI Limited'),
('Clopidogrel 75mg', '75mg', 'Tablet', 'Eskayef'),
('Warfarin 5mg', '5mg', 'Tablet', 'Beximco Pharma'),
('Rivaroxaban 20mg', '20mg', 'Tablet', 'Renata Limited'),
('Enalapril 10mg', '10mg', 'Tablet', 'ACI Limited'),
('Metoprolol 50mg', '50mg', 'Tablet', 'Eskayef'),
('Bisoprolol 5mg', '5mg', 'Tablet', 'Beximco Pharma'),
('Losartan 100mg', '100mg', 'Tablet', 'Renata Limited'),
('Hydrochlorothiazide 50mg', '50mg', 'Tablet', 'ACI Limited');

-- ---------------------
-- Insert 10 Institutes
-- ---------------------
INSERT INTO institutes (name, address) VALUES
('Bangabandhu Sheikh Mujib Medical University', 'Dhaka'),
('Dhaka Medical College', 'Dhaka'),
('Sir Salimullah Medical College', 'Dhaka'),
('Rajshahi Medical College', 'Rajshahi'),
('Chittagong Medical College', 'Chattogram'),
('Sylhet MAG Osmani Medical College', 'Sylhet'),
('Mymensingh Medical College', 'Mymensingh'),
('Khulna Medical College', 'Khulna'),
('Barisal Medical College', 'Barisal'),
('Jashore Medical College', 'Jashore');

-- ---------------------
-- Insert 20 Qualifications
-- ---------------------
INSERT INTO qualifications (name) VALUES
('MBBS'),
('BDS'),
('MD (Cardiology)'),
('MD (Neurology)'),
('MD (Medicine)'),
('MS (Surgery)'),
('FCPS (Medicine)'),
('FCPS (Surgery)'),
('Diploma in Diabetes'),
('CCPD'),
('MD (Pediatrics)'),
('MD (Dermatology)'),
('MD (Gynecology)'),
('MD (Orthopedics)'),
('MS (ENT)'),
('MD (Psychiatry)'),
('MPhil (Oncology)'),
('PhD (Pharmacology)'),
('BSc Nursing'),
('Diploma in Radiology');

-- ---------------------
-- Insert 10 Specializations
-- ---------------------
INSERT INTO specializations (name) VALUES
('Cardiology'),
('Neurology'),
('Orthopedics'),
('Dermatology'),
('Gynecology'),
('Pediatrics'),
('ENT'),
('Psychiatry'),
('Oncology'),
('Diabetology');


INSERT INTO blood_groups (group_name) VALUES
('A+'),
('A-'),
('B+'),
('B-'),
('AB+'),
('AB-'),
('O+'),
('O-');