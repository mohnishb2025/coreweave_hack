def timestamp_ms(snowflake_id):
    return snowflake_id >> 22
