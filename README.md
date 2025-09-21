# Python script for airline data analysis

## Requirements:
- Python
- PostgreSQL
- `pip install psycopg2-binary`

## Setup:
Change in code:
```python
database = 'airport_analytics'  # your database
password = '0000'               # your password
```

## Run:
```bash
python main.py
```

## What it does:
1. Shows list of tables in DB
2. Counts flights by airlines  
3. Analyzes booking prices

## Example queries:

**1. List all tables:**
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

**2. Flights by airlines (GROUP BY + COUNT):**
```sql
SELECT 
    airline_id,
    COUNT(*) as total_flights
FROM flights
GROUP BY airline_id
ORDER BY total_flights DESC;
```

**3. Booking price statistics (AVG, MIN, MAX):**
```sql
SELECT 
    status,
    COUNT(*) as bookings_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM booking
GROUP BY status;
```