IF DB_ID(N'PCMonitor') IS NULL
BEGIN
    EXEC(N'CREATE DATABASE [PCMonitor]');
END
GO

USE [PCMonitor];
GO

IF OBJECT_ID(N'dbo.monitor_readings', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.monitor_readings (
        reading_id BIGINT IDENTITY(1, 1) NOT NULL
            CONSTRAINT PK_monitor_readings PRIMARY KEY,
        captured_at DATETIME2(0) NOT NULL,
        hostname NVARCHAR(255) NOT NULL,
        operating_system NVARCHAR(100) NOT NULL,
        os_release NVARCHAR(100) NULL,
        machine NVARCHAR(100) NULL,
        uptime_seconds BIGINT NOT NULL,
        local_ip NVARCHAR(45) NULL,
        cpu_percent DECIMAL(6, 2) NOT NULL,
        memory_percent DECIMAL(6, 2) NOT NULL,
        disk_percent DECIMAL(6, 2) NOT NULL,
        disk_total_gb DECIMAL(12, 2) NOT NULL,
        disk_used_gb DECIMAL(12, 2) NOT NULL,
        disk_free_gb DECIMAL(12, 2) NOT NULL,
        bytes_sent BIGINT NOT NULL,
        bytes_received BIGINT NOT NULL
    );
END
GO

IF OBJECT_ID(N'dbo.process_snapshots', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.process_snapshots (
        process_snapshot_id BIGINT IDENTITY(1, 1) NOT NULL
            CONSTRAINT PK_process_snapshots PRIMARY KEY,
        reading_id BIGINT NOT NULL,
        pid INT NOT NULL,
        process_name NVARCHAR(255) NOT NULL,
        username NVARCHAR(255) NULL,
        memory_percent DECIMAL(6, 2) NOT NULL,
        cpu_percent DECIMAL(6, 2) NOT NULL,
        CONSTRAINT FK_process_snapshots_monitor_readings
            FOREIGN KEY (reading_id)
            REFERENCES dbo.monitor_readings(reading_id)
            ON DELETE CASCADE
    );
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = N'IX_monitor_readings_captured_at'
      AND object_id = OBJECT_ID(N'dbo.monitor_readings')
)
BEGIN
    CREATE INDEX IX_monitor_readings_captured_at
        ON dbo.monitor_readings(captured_at);
END
GO
