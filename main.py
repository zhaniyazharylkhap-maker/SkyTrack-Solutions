import psycopg2


host = 'localhost'
port = '5432'
database = 'airport_analytics'
user = 'postgres'
password = '0000'

connection = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port=port
    )

cursor = connection.cursor()

cursor.execute("""               
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
               """
)

record = cursor.fetchall()

print("Data from Database:- ", record)



cursor.execute("""               
SELECT 
    airline_id,
    COUNT(*) as total_flights
FROM flights
GROUP BY airline_id
ORDER BY total_flights DESC;
    """
)

record = cursor.fetchall()

print("1 - КОЛИЧЕСТВО РЕЙСОВ ПО АВИАКОМПАНИЯМ", record)


cursor.execute(
"""
SELECT 
    status,
    COUNT(*) as bookings_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM booking
GROUP BY status;
"""
)
record = cursor.fetchall()
print("2 - СРЕДНИЙ ПРАЙС, мин прайс и макс прайс", record)



