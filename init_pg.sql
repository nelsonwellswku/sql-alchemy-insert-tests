CREATE SCHEMA IF NOT EXISTS dbo;

CREATE TABLE IF NOT EXISTS dbo."AppUser" (
    "AppUserId"  SERIAL        NOT NULL,
    "FirstName"  VARCHAR(100)  NULL,
    "LastName"   VARCHAR(100)  NULL,
    "Birthday"   DATE          NULL,
    "Gender"     VARCHAR(50)   NULL,
    "Ethnicity"  VARCHAR(100)  NULL,
    CONSTRAINT "PK_AppUser" PRIMARY KEY ("AppUserId")
);
