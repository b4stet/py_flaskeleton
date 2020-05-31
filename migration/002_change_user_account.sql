ALTER TABLE user_account                                                                                           
    ADD COLUMN salt CHAR(32) NOT NULL DEFAULT '_blank'
;

ALTER TABLE user_account                                                                                           
    ALTER COLUMN salt DROP DEFAULT 
;
