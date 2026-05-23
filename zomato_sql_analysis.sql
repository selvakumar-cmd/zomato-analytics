-- ============================================================
-- ZOMATO INDIA RESTAURANT ANALYTICS — SQL ANALYSIS
-- Author: SELVAKUMAR-ANALYST
-- Dataset: 1,280+ restaurants across 15 Indian cities
-- ============================================================

-- ============================================================
-- 1. BASIC EXPLORATION
-- ============================================================

-- Total restaurant count
SELECT COUNT(*) AS total_restaurants
FROM zomato_cleaned;

-- Distinct cities in dataset
SELECT COUNT(DISTINCT City) AS total_cities
FROM zomato_cleaned;

-- Preview first 10 records
SELECT Restaurant_Name, City, Rating, Cost_For_Two, Online_Order
FROM zomato_cleaned
LIMIT 10;

-- ============================================================
-- 2. CITY-WISE ANALYSIS — KPI Reporting
-- ============================================================

-- Restaurant count and average rating per city
SELECT
    City,
    COUNT(*) AS total_restaurants,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Cost_For_Two), 0) AS avg_cost_for_two,
    COUNT(CASE WHEN Online_Order = 'Yes' THEN 1 END) AS online_delivery_count
FROM zomato_cleaned
GROUP BY City
ORDER BY total_restaurants DESC;

-- Top 5 cities by average rating
SELECT City, ROUND(AVG(Rating), 2) AS avg_rating
FROM zomato_cleaned
GROUP BY City
ORDER BY avg_rating DESC
LIMIT 5;

-- ============================================================
-- 3. ONLINE ORDER IMPACT ANALYSIS — Trend Analysis
-- ============================================================

-- Online vs Offline order comparison
SELECT
    Online_Order,
    COUNT(*) AS restaurant_count,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Cost_For_Two), 0) AS avg_cost,
    SUM(Votes) AS total_votes,
    ROUND(AVG(Votes), 0) AS avg_votes_per_restaurant
FROM zomato_cleaned
GROUP BY Online_Order;

-- Percentage of restaurants with online ordering
SELECT
    Online_Order,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM zomato_cleaned), 1) AS percentage
FROM zomato_cleaned
GROUP BY Online_Order;

-- ============================================================
-- 4. PRICE CATEGORY ANALYSIS — Statistical Analysis
-- ============================================================

-- Restaurant distribution by price category
SELECT
    Price_Category,
    COUNT(*) AS restaurant_count,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Votes), 0) AS avg_votes,
    ROUND(MIN(Cost_For_Two), 0) AS min_cost,
    ROUND(MAX(Cost_For_Two), 0) AS max_cost
FROM zomato_cleaned
GROUP BY Price_Category
ORDER BY avg_cost;

-- ============================================================
-- 5. TOP PERFORMING RESTAURANTS — Data Wrangling
-- ============================================================

-- Top 10 highest rated restaurants (min 100 votes)
SELECT
    Restaurant_Name,
    City,
    Area,
    Rating,
    Cost_For_Two,
    Votes,
    Online_Order
FROM zomato_cleaned
WHERE Votes >= 100
ORDER BY Rating DESC, Votes DESC
LIMIT 10;

-- Top 10 best value-for-money (Value Score = Rating / Cost * 1000)
SELECT
    Restaurant_Name,
    City,
    Rating,
    Cost_For_Two,
    Votes,
    ROUND(Rating / Cost_For_Two * 1000, 2) AS Value_Score
FROM zomato_cleaned
WHERE Votes > 50 AND Cost_For_Two > 0
ORDER BY Value_Score DESC
LIMIT 10;

-- ============================================================
-- 6. RATING DISTRIBUTION — Statistical Analysis
-- ============================================================

-- Rating band segmentation
SELECT
    CASE
        WHEN Rating >= 4.5 THEN 'Excellent (4.5+)'
        WHEN Rating >= 4.0 THEN 'Very Good (4.0-4.4)'
        WHEN Rating >= 3.5 THEN 'Good (3.5-3.9)'
        WHEN Rating >= 3.0 THEN 'Average (3.0-3.4)'
        ELSE 'Below Average (<3.0)'
    END AS rating_band,
    COUNT(*) AS restaurant_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM zomato_cleaned), 1) AS percentage
FROM zomato_cleaned
GROUP BY rating_band
ORDER BY MIN(Rating) DESC;

-- ============================================================
-- 7. CORRELATION & BUSINESS INSIGHTS — ETL / KPI Tracking
-- ============================================================

-- Average votes by price category (engagement analysis)
SELECT
    Price_Category,
    ROUND(AVG(Votes), 0) AS avg_votes,
    ROUND(AVG(Rating), 2) AS avg_rating
FROM zomato_cleaned
GROUP BY Price_Category
ORDER BY avg_votes DESC;

-- City-wise online order adoption rate
SELECT
    City,
    COUNT(*) AS total,
    SUM(CASE WHEN Online_Order = 'Yes' THEN 1 ELSE 0 END) AS online_count,
    ROUND(SUM(CASE WHEN Online_Order = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS online_pct
FROM zomato_cleaned
GROUP BY City
ORDER BY online_pct DESC;

-- ============================================================
-- 8. BUSINESS RECOMMENDATIONS QUERIES
-- ============================================================

-- Underserved cities (low competition, decent rating)
SELECT
    City,
    COUNT(*) AS restaurant_count,
    ROUND(AVG(Rating), 2) AS avg_rating
FROM zomato_cleaned
GROUP BY City
HAVING COUNT(*) < 80 AND AVG(Rating) >= 3.5
ORDER BY avg_rating DESC;

-- Best city + price combo for new restaurant entry
SELECT
    City,
    Price_Category,
    COUNT(*) AS count,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Votes), 0) AS avg_engagement
FROM zomato_cleaned
GROUP BY City, Price_Category
ORDER BY avg_rating DESC, avg_engagement DESC
LIMIT 15;
