-- Create Database
CREATE DATABASE IF NOT EXISTS event_management;
USE event_management;

-- Events Table
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME,
    location VARCHAR(255),
    budget DECIMAL(10, 2) DEFAULT 0.00,
    status ENUM('Planning', 'Confirmed', 'Completed', 'Cancelled') DEFAULT 'Planning',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Guests Table
CREATE TABLE IF NOT EXISTS guests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    rsvp_status ENUM('Pending', 'Accepted', 'Declined') DEFAULT 'Pending',
    guest_count INT DEFAULT 1,
    dietary_requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    booking_type ENUM('Venue', 'Catering', 'Photography', 'Music', 'Decoration', 'Other') NOT NULL,
    vendor_name VARCHAR(200) NOT NULL,
    description TEXT,
    cost DECIMAL(10, 2) DEFAULT 0.00,
    booking_date DATE,
    status ENUM('Pending', 'Confirmed', 'Paid', 'Cancelled') DEFAULT 'Pending',
    contact_info VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_event_date ON events(event_date);
CREATE INDEX idx_event_status ON events(status);
CREATE INDEX idx_guest_event ON guests(event_id);
CREATE INDEX idx_guest_rsvp ON guests(rsvp_status);
CREATE INDEX idx_booking_event ON bookings(event_id);
CREATE INDEX idx_booking_status ON bookings(status);

-- Insert sample data
INSERT INTO events (name, description, event_date, event_time, location, budget, status) VALUES
('Annual Tech Conference 2025', 'A comprehensive technology conference featuring industry leaders', '2025-11-15', '09:00:00', 'Convention Center, Delhi', 500000.00, 'Planning'),
('Corporate Gala Dinner', 'Year-end celebration and awards ceremony', '2025-12-20', '19:00:00', 'Grand Hotel, Mumbai', 300000.00, 'Planning');

INSERT INTO guests (event_id, name, email, phone, rsvp_status, guest_count) VALUES
(1, 'Rahul Sharma', 'rahul.sharma@example.com', '+91-9876543210', 'Accepted', 1),
(1, 'Priya Patel', 'priya.patel@example.com', '+91-9876543211', 'Pending', 2),
(2, 'Amit Kumar', 'amit.kumar@example.com', '+91-9876543212', 'Accepted', 1);

INSERT INTO bookings (event_id, booking_type, vendor_name, description, cost, booking_date, status, contact_info) VALUES
(1, 'Venue', 'Convention Center Delhi', 'Main hall booking for 500 attendees', 150000.00, '2025-11-15', 'Confirmed', 'venue@convention.com'),
(1, 'Catering', 'Royal Caterers', 'Full day catering with lunch and snacks', 200000.00, '2025-11-15', 'Pending', 'contact@royalcaterers.com'),
(2, 'Venue', 'Grand Hotel Mumbai', 'Banquet hall for 150 guests', 100000.00, '2025-12-20', 'Confirmed', 'bookings@grandhotel.com');
