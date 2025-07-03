CREATE TABLE user_event_summary (
  user_id TEXT,
  event_hour TIMESTAMP,   -- Rounded to the hour
  event_minute TIMESTAMP, -- Rounded to the minute
  event_type TEXT,
  event_count INT,
  PRIMARY KEY (user_id, event_minute, event_type)
);
