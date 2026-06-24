
-- ==============================================
-- POWER-GRID-KIN 
-- ==============================================

-- -------- SUPPRESSION ET CREATION DE LA BASE --------
DROP DATABASE IF EXISTS `power_grid_kin`;
CREATE DATABASE `power_grid_kin` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `power_grid_kin`;
DROP USER IF EXISTS 'powergrid'@'localhost';
CREATE USER 'powergrid'@'localhost' IDENTIFIED BY '1234567890';
GRANT ALL PRIVILEGES ON power_grid_kin.* TO 'powergrid'@'localhost';
FLUSH PRIVILEGES;
-- ==============================================
-- CREATION DES TABLES
-- ==============================================

CREATE TABLE `COMMUNE` (
    `id_commune` INT AUTO_INCREMENT PRIMARY KEY,
    `nom` VARCHAR(100) NOT NULL UNIQUE,
    `population` INT DEFAULT NULL,
    `description` TEXT
) ENGINE=InnoDB;

CREATE TABLE `CAUSE` (
    `id_cause` INT AUTO_INCREMENT PRIMARY KEY,
    `code` VARCHAR(20) NOT NULL UNIQUE,
    `libelle` VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE `TECHNICIEN` (
    `id_technicien` INT AUTO_INCREMENT PRIMARY KEY,
    `nom` VARCHAR(100) NOT NULL,
    `prenom` VARCHAR(100),
    `telephone` VARCHAR(30),
    `email` VARCHAR(150),
    `competence` VARCHAR(200)
) ENGINE=InnoDB;
ALTER TABLE TECHNICIEN ADD COLUMN id_commune INT DEFAULT NULL;
ALTER TABLE TECHNICIEN 
ADD FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune)
ON UPDATE CASCADE ON DELETE SET NULL;

CREATE TABLE `CENTRALE` (
    `id_centrale` INT AUTO_INCREMENT PRIMARY KEY,
    `nom` VARCHAR(150) NOT NULL,
    `id_commune` INT DEFAULT NULL,
    `adresse` VARCHAR(255),
    `puissance_mw` DECIMAL(8,2),
    FOREIGN KEY (`id_commune`) REFERENCES `COMMUNE`(`id_commune`)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE `POSTE` (
    `id_poste` INT AUTO_INCREMENT PRIMARY KEY,
    `nom` VARCHAR(150) NOT NULL,
    `id_commune` INT DEFAULT NULL,
    `id_centrale` INT DEFAULT NULL,
    `tension_kv` DECIMAL(6,2),
    `adresse` VARCHAR(255),
    FOREIGN KEY (`id_commune`) REFERENCES `COMMUNE`(`id_commune`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_centrale`) REFERENCES `CENTRALE`(`id_centrale`)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE `CIRCUIT` (
    `id_circuit` INT AUTO_INCREMENT PRIMARY KEY,
    `code` VARCHAR(50) NOT NULL,
    `intitule` VARCHAR(200),
    `id_poste` INT DEFAULT NULL,
    `tension_kv` DECIMAL(6,2),
    `zone_description` VARCHAR(255),
    FOREIGN KEY (`id_poste`) REFERENCES `POSTE`(`id_poste`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    UNIQUE (`code`, `id_poste`)
) ENGINE=InnoDB;

CREATE TABLE `EQUIPEMENT` (
    `id_equipement` INT AUTO_INCREMENT PRIMARY KEY,
    `type_equipement` VARCHAR(50) NOT NULL,
    `reference` VARCHAR(100),
    `id_circuit` INT DEFAULT NULL,
    `id_poste` INT DEFAULT NULL,
    `statut` VARCHAR(30) DEFAULT 'ok',
    `details` TEXT,
    FOREIGN KEY (`id_circuit`) REFERENCES `CIRCUIT`(`id_circuit`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_poste`) REFERENCES `POSTE`(`id_poste`)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE `SENSOR` (
    `id_sensor` INT AUTO_INCREMENT PRIMARY KEY,
    `code_sensor` VARCHAR(100) NOT NULL UNIQUE,
    `type_sensor` VARCHAR(50),
    `id_equipement` INT DEFAULT NULL,
    `id_circuit` INT DEFAULT NULL,
    `last_update` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `last_value` VARCHAR(100),
    
    FOREIGN KEY (`id_equipement`) REFERENCES `EQUIPEMENT`(`id_equipement`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_circuit`) REFERENCES `CIRCUIT`(`id_circuit`)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE `INCIDENT` (
    `id_incident` INT AUTO_INCREMENT PRIMARY KEY,
    `reference` VARCHAR(60) UNIQUE,
    `titre` VARCHAR(200) NOT NULL,
    `description` TEXT,
    `id_commune` INT DEFAULT NULL,
    `id_poste` INT DEFAULT NULL,
    `id_circuit` INT DEFAULT NULL,
    `id_equipement` INT DEFAULT NULL,
    `id_cause` INT DEFAULT NULL,
    `severity` ENUM('low','medium','high','critical') DEFAULT 'medium',
    `status` ENUM('open','in_progress','resolved','closed') DEFAULT 'open',
    `start_time` DATETIME NOT NULL,
    `end_time` DATETIME DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (`id_commune`) REFERENCES `COMMUNE`(`id_commune`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_poste`) REFERENCES `POSTE`(`id_poste`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_circuit`) REFERENCES `CIRCUIT`(`id_circuit`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_equipement`) REFERENCES `EQUIPEMENT`(`id_equipement`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_cause`) REFERENCES `CAUSE`(`id_cause`)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE `INTERVENTION` (
    `id_intervention` INT AUTO_INCREMENT PRIMARY KEY,
    `id_incident` INT NOT NULL,
    `id_technicien` INT DEFAULT NULL,
    `date_debut` DATETIME NOT NULL,
    `date_fin` DATETIME DEFAULT NULL,
    `action` VARCHAR(255),
    `remarque` TEXT,
    `statut` ENUM('scheduled','ongoing','done','failed') DEFAULT 'scheduled',

    FOREIGN KEY (`id_incident`) REFERENCES `INCIDENT`(`id_incident`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`id_technicien`) REFERENCES `TECHNICIEN`(`id_technicien`)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE `ALERTE` (
    `id_alerte` INT AUTO_INCREMENT PRIMARY KEY,
    `id_incident` INT DEFAULT NULL,
    `id_sensor` INT DEFAULT NULL,
    `type_alerte` VARCHAR(50),
    `niveau` ENUM('info','warning','critical') DEFAULT 'warning',
    `message` TEXT,
    `date_alerte` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `resolved` BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (`id_incident`) REFERENCES `INCIDENT`(`id_incident`)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (`id_sensor`) REFERENCES `SENSOR`(`id_sensor`)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- ==============================================
-- INSERTIONS DE TEST
-- ==============================================

INSERT INTO COMMUNE (nom, population, description) VALUES
('Gombe', 150000, 'Centre administratif'),
('Kinshasa', 300000, 'Commune historique'),
('Kintambo', 250000, 'Zone résidentielle'),
('Ngaliema', 800000, 'Grande zone résidentielle et collines'),
('Bandalungwa', 600000, 'Quartier animé'),
('Selembao', 700000, 'Commune populaire'),
('Mont-Ngafula', 650000, 'Zone vallonnée'),
('Matete', 500000, 'Commune résidentielle Est'),
('Lemba', 600000, 'Zone universitaire'),
('Ngaba', 400000, 'Petite commune dense'),
('Makala', 450000, 'Zone populaire'),
('Limete', 550000, 'Zone industrielle'),
('Kisenso', 500000, 'Commune périphérique'),
('Masina', 900000, 'Zone très peuplée'),
('N’djili', 600000, 'Commune Est'),
('Kimbanseke', 1200000, 'Grande commune Est'),
('Nsele', 200000, 'Zone rurale'),
('Maluku', 180000, 'Commune très étendue'),
('Barumbu', 300000, 'Centre ville'),
('Kalamu', 450000, 'Zone culturelle'),
('Bumbu', 350000, 'Commune dense'),
('Matadi Kibala', 100000, 'Périphérie Ouest'),
('Kingabwa', 150000, 'Zone industrielle et portuaire'),
('Masina Petro-Congo', 250000, 'Zone industrielle et énergies');


INSERT INTO CAUSE (code, libelle) VALUES
('C004', 'Court-circuit'),
('C005', 'Incendie'),
('C006', 'Foudre'),
('C007', 'Acte de vandalisme'),
('C008', 'Câble coupé'),
('C009', 'Inondation'),
('C010', 'Erreur humaine'),
('C011', 'Surcharge transformateur'),
('C012', 'Problème de disjoncteur');


INSERT INTO TECHNICIEN (nom, prenom, telephone, email, competence, id_commune) VALUES
('AKONKWA','BAGANIZI','0990000001','akonkwa.baganizi@example.com','HT/MT', 4),
('CHYROMOD','MUGOLI','0990000002','chyromod.mugoli@example.com','HT/BT', 1),
('OLINDA','EMILI','0990000003','olinda.emili@example.com','Instrumentation', 12),
('KANSAK','A. KANSAK','0990000004','kansak@example.com','Sûreté électrique', 14),
('IDY','KANGELA','0990000005','idy.kangela@example.com','Maintenance générale', 2),
('IKOKO','LORIKI','0990000006','ikoko.loriki@example.com','Instrumentation', 9),
('KABISA','KABISA','0990000007','kabisa@example.com','HT/MT', 7),
('KANYEBE','NYAVINGI','0990000008','kanyebe@example.com','Réseaux', 5),
('KAYEMBE','KAYEMBA','0990000009','kayembe@example.com','BT', 6),
('KUYA','MWAYA','0990000010','kuya.mwaya@example.com','Transformateurs', 12),
('LUKOKI','MINU','0990000011','lukoki@example.com','Tableaux MT', 8),
('MAKMADOU','SONIA','0990000012','makmadou.sonia@example.com','Sécurité incendie', 14),
('MASSANKA','J. BALALA','0990000013','massanka@example.com','Disjoncteurs', 1),
('MASIALA','MUANDA','0990000014','masiala@example.com','Transformateurs', 7),
('MAWANAKA','NEWANZA','0990000015','mawanaka@example.com','Analyse réseau', 16),
('MBALA','MBUYAMBA','0990000016','mbala@example.com','Câblage', 15),
('MINANGA','DAMBOLU','0990000017','minanga@example.com','Sûreté électrique', 3),
('MINGU','MOSEKO','0990000018','mingu@example.com','Mesures', 12),
('MUMBAMBI','MBAMBI','0990000019','mumbambi@example.com','Réseaux BT', 19),
('MUNKOU','KATUMBA','0990000020','munkou@example.com','HT/MT', 21),
('MUSANSA','MUSANSA','0990000021','musansa@example.com','Contrôle', 11),
('TABU','LUMBA-LUMBA','0990000022','tabu@example.com','Maintenance', 13),
('TOLOINGO','VINYO','0990000023','toloingo@example.com','Incendie', 14),
('TSHIYINGISA','NKATUMA','0990000024','tshiyingisa@example.com','Analyse réseau', 24),
('ZULU','SONA','0990000025','zulu@example.com','Coupures', 18);

INSERT INTO CENTRALE (nom, id_commune, adresse, puissance_mw) VALUES
('Centrale Matadi', 1, 'Avenue Centrale 123', 250.00),
('Centrale Ngaliema', 2, 'Rue Ngaliema 45', 150.00);


INSERT INTO POSTE (nom, id_commune, id_centrale, tension_kv, adresse) VALUES
('Poste HT Gombe Centre', 1, 1, 220, 'Boulevard du 30 juin'),
('Poste HT Ngaliema', 4, 1, 220, 'Avenue de la Justice'),
('Poste HT Mont-Ngafula', 7, 1, 220, 'Route de Matadi'),
('Poste MT Limete Industriel', 12, 2, 110, 'Zone Industrielle Limete'),
('Poste MT Masina', 14, 2, 110, 'Boulevard Lumumba'),
('Poste BT Lemba Université', 9, 2, 20, 'UNIKIN'),
('Poste BT Matete Centre', 8, 2, 20, 'Avenue Butembo'),
('Poste BT Kisenso Clinique', 13, 2, 20, 'Route Sanga');


INSERT INTO CIRCUIT (code, intitule, id_poste, tension_kv, zone_description) VALUES
('CIR001', 'Circuit Industriel', 1, 220.00, 'Zone industrielle Sud'),
('CIR002', 'Circuit Résidentiel', 2, 110.00, 'Quartier résidentiel Gombe');


INSERT INTO EQUIPEMENT (type_equipement, reference, id_circuit, id_poste, statut, details) VALUES
('Transformateur', 'TR-220-1', 1, 1, 'ok', 'Transformateur principal'),
('Disjoncteur', 'DJ-110-1', 2, 2, 'ok', 'Disjoncteur secondaire');


INSERT INTO `SENSOR` (`code_sensor`, `type_sensor`, `id_equipement`, `id_circuit`, `last_value`) VALUES
('SEN-001', 'Température', 1, 1, '75°C'),
('SEN-002', 'Courant', 2, 2, '120A');

INSERT INTO INCIDENT 
(reference, titre, description, id_commune, id_poste, id_circuit, id_equipement, id_cause, severity, status, start_time) VALUES
('INC001', 'Panne Transformateur', 'Le transformateur principal est hors service', 1, 1, 1, 1, 1, 'high', 'open', NOW()),
('INC002', 'Surcharge Circuit', 'Le circuit résidentiel est surchargé', 2, 2, 2, 2, 2, 'medium', 'in_progress', NOW());

INSERT INTO INTERVENTION (id_incident, id_technicien, date_debut, action, statut) VALUES
(1, 5, NOW(), 'Analyse du transformateur', 'ongoing'),
(1, 10, NOW(), 'Remplacement du disjoncteur', 'scheduled'),
(2, 14, NOW(), 'Inspection du câble MT', 'done'),
(2, 17, NOW(), 'Mise sous tension progressive', 'scheduled'),
(1, 9, NOW(), 'Test des protections BT', 'ongoing'),
(1, 2, NOW(), 'Réarmement des relais', 'scheduled'),
(2, 21, NOW(), 'Diagnostic du système incendie', 'done'),
(2, 12, NOW(), 'Vérification capteur fumée', 'ongoing');


INSERT INTO `ALERTE` (`id_incident`, `id_sensor`, `type_alerte`, `niveau`, `message`) VALUES
(1, 1, 'Température', 'critical', 'Température élevée du transformateur'),
(2, 2, 'Courant', 'warning', 'Courant proche de la limite');

-- ==============================================
-- VUES ET RAPPORT FINAL
-- ==============================================

-- Incidents détaillés
CREATE OR REPLACE VIEW `vw_incidents_details` AS
SELECT 
    i.id_incident,
    i.reference AS incident_ref,
    i.titre AS incident_titre,
    i.severity,
    i.status AS incident_status,
    co.nom AS commune,
    p.nom AS poste,
    c.intitule AS circuit,
    e.type_equipement AS equipement,
    ca.libelle AS cause
FROM `INCIDENT` i
LEFT JOIN `COMMUNE` co ON i.id_commune = co.id_commune
LEFT JOIN `POSTE` p ON i.id_poste = p.id_poste
LEFT JOIN `CIRCUIT` c ON i.id_circuit = c.id_circuit
LEFT JOIN `EQUIPEMENT` e ON i.id_equipement = e.id_equipement
LEFT JOIN `CAUSE` ca ON i.id_cause = ca.id_cause;

-- Interventions détaillées
CREATE OR REPLACE VIEW `vw_interventions_details` AS
SELECT 
    it.id_intervention,
    i.reference AS incident_ref,
    t.nom AS technicien_nom,
    t.prenom AS technicien_prenom,
    it.date_debut,
    it.date_fin,
    it.action,
    it.statut AS intervention_status
FROM `INTERVENTION` it
LEFT JOIN `INCIDENT` i ON it.id_incident = i.id_incident
LEFT JOIN `TECHNICIEN` t ON it.id_technicien = t.id_technicien;

-- Alertes détaillées
CREATE OR REPLACE VIEW `vw_alertes_details` AS
SELECT 
    a.id_alerte,
    i.reference AS incident_ref,
    s.code_sensor AS sensor_code,
    s.last_value AS sensor_value,
    a.type_alerte,
    a.niveau,
    a.message,
    a.date_alerte,
    a.resolved
FROM `ALERTE` a
LEFT JOIN `INCIDENT` i ON a.id_incident = i.id_incident
LEFT JOIN `SENSOR` s ON a.id_sensor = s.id_sensor;

-- Résumé : incidents par commune et gravité
CREATE OR REPLACE VIEW `vw_incidents_commune_gravite` AS
SELECT 
    co.nom AS commune,
    i.severity,
    COUNT(*) AS nb_incidents
FROM `INCIDENT` i
LEFT JOIN `COMMUNE` co ON i.id_commune = co.id_commune
GROUP BY co.nom, i.severity
ORDER BY co.nom, FIELD(i.severity,'critical','high','medium','low');

-- Résumé : incidents par poste
CREATE OR REPLACE VIEW `vw_incidents_par_poste` AS
SELECT 
    p.nom AS poste,
    COUNT(*) AS nb_incidents
FROM `INCIDENT` i
LEFT JOIN `POSTE` p ON i.id_poste = p.id_poste
GROUP BY p.nom
ORDER BY nb_incidents DESC;

-- Résumé : interventions par technicien
CREATE OR REPLACE VIEW `vw_interventions_par_technicien` AS
SELECT 
    t.nom AS technicien_nom,
    t.prenom AS technicien_prenom,
    COUNT(*) AS nb_interventions
FROM `INTERVENTION` it
LEFT JOIN `TECHNICIEN` t ON it.id_technicien = t.id_technicien
GROUP BY t.nom, t.prenom
ORDER BY nb_interventions DESC;

-- Résumé : alertes par niveau
CREATE OR REPLACE VIEW `vw_alertes_par_niveau` AS
SELECT 
    niveau,
    COUNT(*) AS nb_alertes
FROM `ALERTE`
GROUP BY niveau
ORDER BY FIELD(niveau,'critical','warning','info');

-- Rapport final combiné
CREATE OR REPLACE VIEW `vw_rapport_complet` AS
SELECT
    i.reference AS incident_ref,
    i.titre AS incident_titre,
    i.severity,
    i.status AS incident_status,
    p.nom AS poste,
    c.intitule AS circuit,
    e.type_equipement AS equipement,
    it.action AS intervention_action,
    it.statut AS intervention_status,
    t.nom AS technicien_nom,
    t.prenom AS technicien_prenom,
    a.type_alerte,
    a.niveau AS alert_niveau,
    a.message AS alert_message,
    s.code_sensor AS sensor_code,
    s.last_value AS sensor_value,
    s.last_update AS sensor_last_update
FROM `INCIDENT` i
LEFT JOIN `POSTE` p ON i.id_poste = p.id_poste
LEFT JOIN `CIRCUIT` c ON i.id_circuit = c.id_circuit
LEFT JOIN `EQUIPEMENT` e ON i.id_equipement = e.id_equipement
LEFT JOIN `INTERVENTION` it ON i.id_incident = it.id_incident
LEFT JOIN `TECHNICIEN` t ON it.id_technicien = t.id_technicien
LEFT JOIN `ALERTE` a ON i.id_incident = a.id_incident
LEFT JOIN `SENSOR` s ON a.id_sensor = s.id_sensor
ORDER BY i.id_incident, it.id_intervention, a.id_alerte;



-- Afficher tous les incidents
SELECT * FROM vw_incidents_details;

-- Afficher interventions
SELECT * FROM vw_interventions_details;

-- Afficher alertes
SELECT * FROM vw_alertes_details;

-- Résumé incidents par commune et gravité
SELECT * FROM vw_incidents_commune_gravite;

-- Résumé incidents par poste
SELECT * FROM vw_incidents_par_poste;

-- Résumé interventions par technicien
SELECT * FROM vw_interventions_par_technicien;

-- Résumé alertes par niveau
SELECT * FROM vw_alertes_par_niveau;

-- Rapport final combiné
SELECT * FROM vw_rapport_complet;



-- ============================
-- TABLE SENSOR_LOG (historique des mesures)
-- ============================
CREATE TABLE SENSOR_LOG (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT NOT NULL,
    valeur VARCHAR(100),
    date_mesure DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sensor) REFERENCES SENSOR(id_sensor)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================
-- TABLE MAINTENANCE (interventions planifiées)
-- ============================
CREATE TABLE MAINTENANCE (
    id_maintenance INT AUTO_INCREMENT PRIMARY KEY,
    id_equipement INT NOT NULL,
    id_technicien INT,
    date_planifie DATETIME NOT NULL,
    duree_estimee INT COMMENT 'Durée en minutes',
    type_maintenance ENUM('préventive','curative') DEFAULT 'préventive',
    statut ENUM('scheduled','ongoing','done','canceled') DEFAULT 'scheduled',
    description TEXT,
    FOREIGN KEY (id_equipement) REFERENCES EQUIPEMENT(id_equipement)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_technicien) REFERENCES TECHNICIEN(id_technicien)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================
-- TABLE ROLE (pour gestion des utilisateurs)
-- ============================
CREATE TABLE ROLE (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    nom_role VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
) ENGINE=InnoDB;

-- ============================
-- TABLE USER (utilisateurs du système)
-- ============================
CREATE TABLE USER (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(150),
    actif BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

-- ============================
-- TABLE USER_ROLE (relation utilisateur-role)
-- ============================
CREATE TABLE USER_ROLE (
    id_user INT NOT NULL,
    id_role INT NOT NULL,
    PRIMARY KEY (id_user, id_role),
    FOREIGN KEY (id_user) REFERENCES USER(id_user)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_role) REFERENCES ROLE(id_role)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;



DELIMITER $$

CREATE TRIGGER trg_sensor_alert
AFTER INSERT ON SENSOR_LOG
FOR EACH ROW
BEGIN
    DECLARE seuil DECIMAL(10,2);
    
    -- Récupérer le seuil critique correspondant au type du capteur
    SELECT valeur_critique INTO seuil
    FROM SENSOR_THRESHOLD s
    JOIN SENSOR se ON s.type_sensor = se.type_sensor
    WHERE se.id_sensor = NEW.id_sensor
    LIMIT 1;

    -- Si la valeur dépasse le seuil, créer une alerte
    IF seuil IS NOT NULL AND CAST(NEW.valeur AS DECIMAL(10,2)) > seuil THEN
        INSERT INTO ALERTE (id_sensor, type_alerte, niveau, message)
        VALUES (
            NEW.id_sensor,
            (SELECT type_sensor FROM SENSOR WHERE id_sensor = NEW.id_sensor),
            'critical',
            CONCAT('Valeur critique détectée : ', NEW.valeur)
        );
    END IF;
END$$

DELIMITER ;





DELIMITER $$

CREATE TRIGGER trg_incident_update_status
AFTER UPDATE ON INTERVENTION
FOR EACH ROW
BEGIN
    DECLARE nb_non_done INT;

    -- Compter les interventions pas encore terminées pour l’incident
    SELECT COUNT(*) INTO nb_non_done
    FROM INTERVENTION
    WHERE id_incident = NEW.id_incident AND statut != 'done';

    -- Si toutes les interventions sont terminées, mettre l’incident en 'resolved'
    IF nb_non_done = 0 THEN
        UPDATE INCIDENT
        SET status = 'resolved', updated_at = NOW()
        WHERE id_incident = NEW.id_incident;
    END IF;
END$$

DELIMITER ;



DELIMITER $$

CREATE PROCEDURE AddPlannedIntervention(
    IN p_id_incident INT,
    IN p_id_technicien INT,
    IN p_date_debut DATETIME,
    IN p_action VARCHAR(255)
)
BEGIN
    INSERT INTO INTERVENTION (id_incident, id_technicien, date_debut, action, statut)
    VALUES (p_id_incident, p_id_technicien, p_date_debut, p_action, 'scheduled');
END$$

DELIMITER ;


CALL AddPlannedIntervention(1, 2, '2025-12-25 08:00:00', 'Vérification du transformateur');



CREATE OR REPLACE VIEW vw_incidents_details AS
SELECT 
    i.id_incident,
    i.reference AS incident_ref,
    i.titre AS incident_titre,
    i.severity,
    i.status AS incident_status,
    co.nom AS commune,
    p.nom AS poste,
    c.intitule AS circuit,
    e.type_equipement AS equipement,
    ca.libelle AS cause
FROM INCIDENT i
LEFT JOIN COMMUNE co ON i.id_commune = co.id_commune
LEFT JOIN POSTE p ON i.id_poste = p.id_poste
LEFT JOIN CIRCUIT c ON i.id_circuit = c.id_circuit
LEFT JOIN EQUIPEMENT e ON i.id_equipement = e.id_equipement
LEFT JOIN CAUSE ca ON i.id_cause = ca.id_cause;


CREATE OR REPLACE VIEW vw_incidents_commune_gravite AS
SELECT 
    co.nom AS commune,
    i.severity,
    COUNT(*) AS nb_incidents
FROM INCIDENT i
LEFT JOIN COMMUNE co ON i.id_commune = co.id_commune
GROUP BY co.nom, i.severity
ORDER BY co.nom, FIELD(i.severity,'critical','high','medium','low');


CREATE OR REPLACE VIEW vw_interventions_par_technicien AS
SELECT 
    t.nom AS technicien_nom,
    t.prenom AS technicien_prenom,
    COUNT(*) AS nb_interventions,
    SUM(CASE WHEN i.statut='done' THEN 1 ELSE 0 END) AS interventions_terminees
FROM INTERVENTION i
LEFT JOIN TECHNICIEN t ON i.id_technicien = t.id_technicien
GROUP BY t.nom, t.prenom
ORDER BY nb_interventions DESC;

CREATE OR REPLACE VIEW vw_maintenance_plan AS
SELECT 
    m.id_maintenance,
    e.type_equipement AS equipement,
    t.nom AS technicien_nom,
    t.prenom AS technicien_prenom,
    m.date_planifie,
    m.duree_estimee,
    m.type_maintenance,
    m.statut
FROM MAINTENANCE m
LEFT JOIN EQUIPEMENT e ON m.id_equipement = e.id_equipement
LEFT JOIN TECHNICIEN t ON m.id_technicien = t.id_technicien
ORDER BY m.date_planifie;


CREATE OR REPLACE VIEW vw_alertes_critique AS
SELECT 
    a.id_alerte,
    s.code_sensor AS sensor_code,
    s.type_sensor,
    a.message,
    a.date_alerte,
    i.reference AS incident_ref
FROM ALERTE a
LEFT JOIN SENSOR s ON a.id_sensor = s.id_sensor
LEFT JOIN INCIDENT i ON a.id_incident = i.id_incident
WHERE a.niveau='critical' AND a.resolved=FALSE
ORDER BY a.date_alerte DESC;


CREATE OR REPLACE VIEW vw_sensor_history AS
SELECT 
    sl.id_log,
    s.code_sensor,
    s.type_sensor,
    sl.valeur AS sensor_value,
    sl.date_mesure
FROM SENSOR_LOG sl
LEFT JOIN SENSOR s ON sl.id_sensor = s.id_sensor
ORDER BY sl.date_mesure DESC;

CREATE OR REPLACE VIEW vw_dashboard_global AS
SELECT
    i.reference AS incident_ref,
    i.titre AS incident_titre,
    i.severity,
    i.status AS incident_status,
    co.nom AS commune,
    p.nom AS poste,
    e.type_equipement AS equipement,
    it.action AS intervention_action,
    it.statut AS intervention_status,
    t.nom AS technicien_nom,
    t.prenom AS technicien_prenom,
    a.type_alerte,
    a.niveau AS alert_niveau,
    a.message AS alert_message,
    s.code_sensor AS sensor_code,
    s.last_value AS sensor_value,
    s.last_update AS sensor_last_update
FROM INCIDENT i
LEFT JOIN COMMUNE co ON i.id_commune = co.id_commune
LEFT JOIN POSTE p ON i.id_poste = p.id_poste
LEFT JOIN EQUIPEMENT e ON i.id_equipement = e.id_equipement
LEFT JOIN INTERVENTION it ON i.id_incident = it.id_incident
LEFT JOIN TECHNICIEN t ON it.id_technicien = t.id_technicien
LEFT JOIN ALERTE a ON i.id_incident = a.id_incident
LEFT JOIN SENSOR s ON a.id_sensor = s.id_sensor
ORDER BY i.id_incident, it.id_intervention, a.id_alerte;

