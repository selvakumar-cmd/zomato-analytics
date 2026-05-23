# 📊 Power BI Dashboard Setup Guide
# Zomato Restaurant Analytics Project

## Step 1: Open Power BI Desktop
- Download from: https://powerbi.microsoft.com/desktop (Free)

## Step 2: Import Data
1. Click "Get Data" → "Text/CSV"
2. Select: dataset/zomato_cleaned.csv
3. Click "Load"

## Step 3: Create These Visuals

### PAGE 1 — OVERVIEW DASHBOARD
┌─────────────────────────────────────────┐
│  Visual 1: Card — Total Restaurants     │
│  Field: Count of Restaurant_Name        │
├─────────────────────────────────────────┤
│  Visual 2: Card — Avg Rating            │
│  Field: Average of Rating               │
├─────────────────────────────────────────┤
│  Visual 3: Card — Avg Cost for Two      │
│  Field: Average of Cost_For_Two         │
├─────────────────────────────────────────┤
│  Visual 4: Bar Chart — City Count       │
│  X-axis: City                           │
│  Y-axis: Count of Restaurant_Name       │
│  Sort: Descending                       │
├─────────────────────────────────────────┤
│  Visual 5: Donut Chart — Online Order   │
│  Legend: Online_Order                   │
│  Values: Count of Restaurant_Name       │
├─────────────────────────────────────────┤
│  Visual 6: Bar Chart — Restaurant Type  │
│  X-axis: Restaurant_Type               │
│  Y-axis: Count of Restaurant_Name       │
└─────────────────────────────────────────┘

### PAGE 2 — RATING & PRICING ANALYSIS
┌─────────────────────────────────────────┐
│  Visual 1: Column Chart — City Rating   │
│  X-axis: City                           │
│  Y-axis: Average of Rating              │
├─────────────────────────────────────────┤
│  Visual 2: Scatter Chart                │
│  X-axis: Cost_For_Two                   │
│  Y-axis: Rating                         │
│  Size: Votes                            │
│  Legend: Restaurant_Type               │
├─────────────────────────────────────────┤
│  Visual 3: Donut — Price Category       │
│  Legend: Price_Category                 │
│  Values: Count of Restaurant_Name       │
├─────────────────────────────────────────┤
│  Visual 4: Bar — Rating by Price Cat    │
│  X-axis: Price_Category                 │
│  Y-axis: Average of Rating              │
└─────────────────────────────────────────┘

### PAGE 3 — CUISINE & INSIGHTS
┌─────────────────────────────────────────┐
│  Visual 1: Word Cloud — Cuisines        │
│  Category: Cuisines                     │
├─────────────────────────────────────────┤
│  Visual 2: Table — Top Restaurants      │
│  Columns: Name, City, Rating, Cost,     │
│           Votes, Value_Score            │
│  Sort by: Value_Score DESC              │
├─────────────────────────────────────────┤
│  Visual 3: Slicer — City               │
│  Field: City                            │
├─────────────────────────────────────────┤
│  Visual 4: Slicer — Online Order        │
│  Field: Online_Order                    │
└─────────────────────────────────────────┘

## Step 4: Theme & Colors
- Go to View → Themes → Browse themes
- Use Red (#E23744) as primary color (Zomato brand)
- Use Dark background for premium look

## Step 5: Add Title
- Insert → Text Box → "🍽️ Zomato India Restaurant Analytics"
- Font: Segoe UI Bold, Size 24, Color: #E23744

## Step 6: Publish (Optional)
- Click "Publish" → Sign in with Microsoft account (Free)
- Share link on Resume / LinkedIn

## DAX Measures to Add:

### Measure 1: High Rated Restaurants
```
High_Rated = CALCULATE(
    COUNTROWS(zomato_cleaned),
    zomato_cleaned[Rating] >= 4.0
)
```

### Measure 2: Online Order %
```
Online_Pct = 
DIVIDE(
    CALCULATE(COUNTROWS(zomato_cleaned), zomato_cleaned[Online_Order] = "Yes"),
    COUNTROWS(zomato_cleaned)
) * 100
```

### Measure 3: Avg Value Score
```
Avg_Value = AVERAGE(zomato_cleaned[Value_Score])
```
