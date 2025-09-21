-- ПРОСТЫЕ АНАЛИТИЧЕСКИЕ ЗАПРОСЫ ДЛЯ АВИАКОМПАНИИ
-- =================================================

-- 1. КОЛИЧЕСТВО РЕЙСОВ ПО АВИАКОМПАНИЯМ
-- Считает сколько рейсов у каждой авиакомпании
SELECT 
    airline_id,
    COUNT(*) as total_flights
FROM flights
GROUP BY airline_id
ORDER BY total_flights DESC;

-- 2. СРЕДНЯЯ ЦЕНА БИЛЕТОВ ПО СТАТУСАМ БРОНИРОВАНИЯ
-- Показывает среднюю цену для разных статусов бронирований
SELECT 
    status,
    COUNT(*) as bookings_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM booking
GROUP BY status;

-- 3. КОЛИЧЕСТВО ПАССАЖИРОВ ПО СТРАНАМ
-- Считает пассажиров по странам гражданства
SELECT 
    country_of_citizenship,
    COUNT(*) as passengers_count
FROM passengers
GROUP BY country_of_citizenship
ORDER BY passengers_count DESC;

-- 4. СТАТИСТИКА ПО БАГАЖУ
-- Анализ веса багажа
SELECT 
    COUNT(*) as total_baggage,
    AVG(weight_in_kg) as avg_weight,
    MIN(weight_in_kg) as min_weight,
    MAX(weight_in_kg) as max_weight
FROM baggage;

-- 5. РЕЙСЫ ПО СТАТУСАМ
-- Показывает количество рейсов в каждом статусе
SELECT 
    status,
    COUNT(*) as flights_count
FROM flights
GROUP BY status
ORDER BY flights_count DESC;

-- 6. РЕЗУЛЬТАТЫ ПРОВЕРКИ БЕЗОПАСНОСТИ
-- Статистика прохождения контроля безопасности
SELECT 
    check_result,
    COUNT(*) as checks_count
FROM security_check
GROUP BY check_result;

-- 7. ПАССАЖИРЫ ПО ПОЛУ И ВОЗРАСТУ
-- Считает пассажиров по полу
SELECT 
    gender,
    COUNT(*) as passengers_count,
    AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM date_of_birth)) as avg_age
FROM passengers
WHERE date_of_birth IS NOT NULL
GROUP BY gender;

-- 8. ПОПУЛЯРНЫЕ ПЛАТФОРМЫ БРОНИРОВАНИЯ
-- Показывает какие платформы используют чаще
SELECT 
    booking_platform,
    COUNT(*) as bookings_count,
    AVG(price) as avg_price
FROM booking
GROUP BY booking_platform
ORDER BY bookings_count DESC;

-- 9. АЭРОПОРТЫ ПО СТРАНАМ
-- Количество аэропортов в каждой стране
SELECT 
    country,
    COUNT(*) as airports_count
FROM airport
GROUP BY country
ORDER BY airports_count DESC;

-- 10. РЕЙСЫ ПО МЕСЯЦАМ (за текущий год)
-- Показывает в какие месяцы больше рейсов
SELECT 
    COUNT(*) as total_flights,
    COUNT(DISTINCT airline_id) as unique_airlines,
    COUNT(DISTINCT departure_airport_id) as departure_airports,
    COUNT(DISTINCT arrival_airport_id) as arrival_airports
FROM flights;