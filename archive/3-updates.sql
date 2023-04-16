ALTER TABLE taxiapp_complaint_statement ADD COLUMN number_plate varchar(200) DEFAULT '';
ALTER TABLE taxiapp_complaint_statement ADD COLUMN latitute VARCHAR(200) DEFAULT '';
ALTER TABLE taxiapp_complaint_statement ADD COLUMN longitude VARCHAR(200) DEFAULT '';
ALTER TABLE taxiapp_complaint_statement ADD COLUMN updated_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;