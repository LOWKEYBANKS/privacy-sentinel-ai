```sql
-- Privacy Sentinel AI - Database Initialization
-- Phase 0: Core tables for analysis and auditing

-- Extension for UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main analysis audit log
CREATE TABLE IF NOT EXISTS analysis_audit_log (
    id SERIAL PRIMARY KEY,
    content_hash VARCHAR(16) NOT NULL,
    risk_score INTEGER NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
    risk_count INTEGER NOT NULL CHECK (risk_count >= 0),
    client_ip VARCHAR(45),
    source_url TEXT,
    timestamp TIMESTAMP DEFAULT 
                    
                        ƒ
                        CURRENT TIMESTAMP
                    
                ,
    
    -- Indexes for performance
    CONSTRAINT idx_audit_content_hash UNIQUE (content_hash, timestamp)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_audit_content_hash ON analysis_audit_log(content_hash);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON analysis_audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_score ON analysis_audit_log(risk_score);
CREATE INDEX IF NOT EXISTS idx_audit_client_ip ON analysis_audit_log(client_ip);

-- Risk types catalog
CREATE TABLE IF NOT EXISTS risk_types (
    id SERIAL PRIMARY KEY,
    risk_name VARCHAR(50) NOT NULL UNIQUE,
    risk_category VARCHAR(30) NOT NULL,
    weight INTEGER DEFAULT 1 CHECK (weight >= 1 AND weight <= 25),
    description TEXT,
    created_at TIMESTAMP DEFAULT 
                    
                        ƒ
                        CURRENT TIMESTAMP
                    
                
);

-- Insert default risk categories
INSERT INTO risk_types (risk_name, risk_category, weight, description) VALUES
('biometric_data', 'sensitive', 25, 'Fingerprint, face, voice biometrics collection'),
('location_tracking', 'moderate', 20, 'GPS or location data tracking'),
('voice_data', 'sensitive', 15, 'Voice recording or analysis'),
('email_collection', 'basic', 10, 'Email address collection'),
('data_sharing', 'moderate', 20, 'Third-party data sharing practices'),
('marketing_data', 'basic', 10, 'Advertising or marketing data'),
('tracking_data', 'basic', 12, 'Analytics or user tracking'),
('cookie_tracking', 'low', 8, 'Web tracking cookies'),
('camera_access', 'sensitive', 18, 'Camera permission requests'),
('microphone_access', 'sensitive', 18, 'Microphone permission requests')
ON CONFLICT (risk_name) DO NOTHING;

-- API usage metrics
CREATE TABLE IF NOT EXISTS api_metrics (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    processing_time_ms INTEGER,
    client_ip VARCHAR(45),
    timestamp TIMESTAMP DEFAULT 
                    
                        ƒ
                        CURRENT TIMESTAMP
                    
                ,
    request_size_bytes INTEGER DEFAULT 0,
    response_size_bytes INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_api_metrics_endpoint ON api_metrics(endpoint);
CREATE INDEX IF NOT EXISTS idx_api_metrics_timestamp ON api_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_api_metrics_status ON api_metrics(status_code);

-- System configuration
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT 
                    
                        ƒ
                        CURRENT TIMESTAMP
                    
                
);

-- Default configuration
INSERT INTO system_config (key, value, description) VALUES
('max_text_length', '16000', 'Maximum text length for analysis requests'),
('rate_limit', '100', 'Rate limit per minute per IP'),
('llm_mode', 'development', 'LLM processing mode'),
('version', '1.0.0', 'Current API version')
ON CONFLICT (key) DO NOTHING;

-- Create views for reporting
CREATE OR REPLACE VIEW daily_metrics AS
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as total_requests,
    AVG(CASE WHEN endpoint = '/api/summarize' THEN processing_time_ms END) as avg_summary_time,
    AVG(risk_score) as avg_risk_score,
    COUNT(DISTINCT client_ip) as unique_ips
FROM analysis_audit_log 
JOIN api_metrics ON DATE(analysis_audit_log.timestamp) = DATE(api_metrics.timestamp)
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Grant permissions to database user
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO dev;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO dev;
GRANT SELECT ON ALL VIEWS IN SCHEMA public TO dev;

COMMIT;

-- Verification queries
SELECT 'Database initialized successfully' as status;
SELECT COUNT(*) as risk_types_loaded FROM risk_types;
