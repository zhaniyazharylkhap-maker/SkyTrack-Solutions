import psycopg2

# Database connection parameters
host = 'localhost'
port = '5432'
database = 'airport_analytics'
user = 'postgres'
password = '0000'

# Establish connection
connection = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port=port
)

cursor = connection.cursor()

# Get all tables in the database
cursor.execute("""               
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
               """
)
record = cursor.fetchall()
print("Data from Database:- ", record)
print("\n" + "="*60 + "\n")

# 1. КОЛИЧЕСТВО РЕЙСОВ ПО АВИАКОМПАНИЯМ
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
print("1 - КОЛИЧЕСТВО РЕЙСОВ ПО АВИАКОМПАНИЯМ:")
for row in record:
    print(f"   Авиакомпания {row[0]}: {row[1]} рейсов")
print()

# 2. СРЕДНЯЯ ЦЕНА БИЛЕТОВ ПО СТАТУСАМ БРОНИРОВАНИЯ
cursor.execute("""
SELECT 
    status,
    COUNT(*) as bookings_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM booking
GROUP BY status;
""")
record = cursor.fetchall()
print("2 - СРЕДНЯЯ/МИН/МАКС ЦЕНА ПО СТАТУСАМ БРОНИРОВАНИЯ:")
for row in record:
    print(f"   Статус '{row[0]}': {row[1]} бронирований, средняя цена: {float(row[2]):.2f}, мин: {float(row[3]):.2f}, макс: {float(row[4]):.2f}")
print()

# 3. КОЛИЧЕСТВО ПАССАЖИРОВ ПО СТРАНАМ
cursor.execute("""
SELECT 
    country_of_citizenship,
    COUNT(*) as passengers_count
FROM passengers
GROUP BY country_of_citizenship
ORDER BY passengers_count DESC;
""")
record = cursor.fetchall()
print("3 - КОЛИЧЕСТВО ПАССАЖИРОВ ПО СТРАНАМ:")
for row in record:
    print(f"   {row[0]}: {row[1]} пассажиров")
print()

# 4. СТАТИСТИКА ПО БАГАЖУ
cursor.execute("""
SELECT 
    COUNT(*) as total_baggage,
    AVG(weight_in_kg) as avg_weight,
    MIN(weight_in_kg) as min_weight,
    MAX(weight_in_kg) as max_weight
FROM baggage;
""")
record = cursor.fetchall()
print("4 - СТАТИСТИКА ПО БАГАЖУ:")
for row in record:
    print(f"   Всего багажа: {row[0]}, средний вес: {row[1]:.2f} кг, мин: {row[2]} кг, макс: {row[3]} кг")
print()

# 5. РЕЙСЫ ПО СТАТУСАМ
cursor.execute("""
SELECT 
    status,
    COUNT(*) as flights_count
FROM flights
GROUP BY status
ORDER BY flights_count DESC;
""")
record = cursor.fetchall()
print("5 - РЕЙСЫ ПО СТАТУСАМ:")
for row in record:
    print(f"   Статус '{row[0]}': {row[1]} рейсов")
print()

# 6. РЕЗУЛЬТАТЫ ПРОВЕРКИ БЕЗОПАСНОСТИ
cursor.execute("""
SELECT 
    check_result,
    COUNT(*) as checks_count
FROM security_check
GROUP BY check_result;
""")
record = cursor.fetchall()
print("6 - РЕЗУЛЬТАТЫ ПРОВЕРКИ БЕЗОПАСНОСТИ:")
for row in record:
    print(f"   Результат '{row[0]}': {row[1]} проверок")
print()

# 7. ПАССАЖИРЫ ПО ПОЛУ И ВОЗРАСТУ
cursor.execute("""
SELECT 
    gender,
    COUNT(*) as passengers_count,
    AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM date_of_birth)) as avg_age
FROM passengers
WHERE date_of_birth IS NOT NULL
GROUP BY gender;
""")
record = cursor.fetchall()
print("7 - ПАССАЖИРЫ ПО ПОЛУ И ВОЗРАСТУ:")
for row in record:
    print(f"   Пол '{row[0]}': {row[1]} пассажиров, средний возраст: {row[2]:.1f} лет")
print()

# 8. ПОПУЛЯРНЫЕ ПЛАТФОРМЫ БРОНИРОВАНИЯ
cursor.execute("""
SELECT 
    booking_platform,
    COUNT(*) as bookings_count,
    AVG(price) as avg_price
FROM booking
GROUP BY booking_platform
ORDER BY bookings_count DESC;
""")
record = cursor.fetchall()
print("8 - ПОПУЛЯРНЫЕ ПЛАТФОРМЫ БРОНИРОВАНИЯ:")
for row in record:
    print(f"   Платформа '{row[0]}': {row[1]} бронирований, средняя цена: {row[2]:.2f}")
print()

# 9. АЭРОПОРТЫ ПО СТРАНАМ
cursor.execute("""
SELECT 
    country,
    COUNT(*) as airports_count
FROM airport
GROUP BY country
ORDER BY airports_count DESC;
""")
record = cursor.fetchall()
print("9 - АЭРОПОРТЫ ПО СТРАНАМ:")
for row in record:
    print(f"   {row[0]}: {row[1]} аэропортов")
print()

# 10. ОБЩАЯ СТАТИСТИКА ПО РЕЙСАМ
cursor.execute("""
SELECT 
    COUNT(*) as total_flights,
    COUNT(DISTINCT airline_id) as unique_airlines,
    COUNT(DISTINCT departure_airport_id) as departure_airports,
    COUNT(DISTINCT arrival_airport_id) as arrival_airports
FROM flights;
""")
record = cursor.fetchall()
print("10 - ОБЩАЯ СТАТИСТИКА ПО РЕЙСАМ:")
for row in record:
    print(f"   Всего рейсов: {row[0]}")
    print(f"   Уникальных авиакомпаний: {row[1]}")
    print(f"   Аэропортов отправления: {row[2]}")
    print(f"   Аэропортов прибытия: {row[3]}")

# Close connection
cursor.close()
connection.close()
print("\n" + "="*60)
print("Анализ завершен. Соединение закрыто.")