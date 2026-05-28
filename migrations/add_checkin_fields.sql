-- Migration: Add QR Code Check-in fields to guests table
-- Run this SQL script in your MySQL database

USE event_management;

-- Add check-in tracking columns
ALTER TABLE guests 
ADD COLUMN qr_token VARCHAR(100) AFTER dietary_requirements,
ADD COLUMN checked_in BOOLEAN DEFAULT FALSE AFTER qr_token,
ADD COLUMN check_in_time DATETIME AFTER checked_in;

-- Add index for faster QR token lookup
CREATE INDEX idx_qr_token ON guests(qr_token);
CREATE INDEX idx_checked_in ON guests(checked_in);

-- View updated table structure
DESCRIBE guests;

SELECT 'Migration completed successfully!' AS status;
