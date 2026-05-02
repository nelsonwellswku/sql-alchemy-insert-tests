IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'TestDb')
BEGIN
    CREATE DATABASE TestDb;
END
GO

USE TestDb;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'dbo' AND t.name = 'AppUser'
)
BEGIN
    CREATE TABLE dbo.AppUser (
        AppUserId  INT           IDENTITY(1,1) NOT NULL CONSTRAINT PK_AppUser PRIMARY KEY,
        FirstName  NVARCHAR(100) NULL,
        LastName   NVARCHAR(100) NULL,
        Birthday   DATE          NULL,
        Gender     NVARCHAR(50)  NULL,
        Ethnicity  NVARCHAR(100) NULL
    );
END
GO
