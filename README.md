# Collecting Children's Attractions Data 

Automated system for collecting children's attraction data from OpenStreetMap worldwide.

## What It Does

Collects children's attractions data for any city including:
- Playgrounds, theme parks, water parks
- Zoos, aquariums, museums  
- Toy stores

## Quick Start
```bash
pip install requests
python test.py
```

Change city : `city = "london"` - for example 

## Output File

`attractions.json` - attractions from new york 
`test.json` - test file for any city 

Example:
```json
{
  "city": "London",
  "name": "British Museum",
  "type": "Museum",
  "coordinates": {"lat": 51.519, "lng": -0.127},
  "seo_saturation": 10,
  "search_popularity": 8
}
```

## Features

- free OpenStreetMap API
- Works for any city worldwide
- Auto-retry if server is busy and because before was the server is slow 
- No duplicate entries
- All cities in one file

## How to Use

### Single City
```python
city = "new york"
run_and_save(city)
```

### Multiple Cities
```python
cities = ["new york", "london", "paris"]
for city in cities:
    run_and_save(city)
```

## Data Fields

- **city** - City name
- **name** - Attraction name
- **type** - Museum, Zoo, Playground, etc.
- **coordinates** - Exact latitude and longitude
- **seo_saturation** - Online presence score (0-10)
- **search_popularity** - Popularity score (0-10)

## How It Works

1. You type city name 
2. System finds city in OpenStreetMap
3. Collects all children's attractions
4. Saves to JSON file
5. No duplicates added

## Scoring System

**SEO Saturation:**
- Has website: +4 points
- Has phone: +3 points
- Has Wikipedia: +3 points

**Search Popularity:**
- Based on how much info the attraction has
- More details = higher score

## Speed

Takes 60-90 seconds per city for complete data collection.

## Error Handling

If server is busy:
- Waits 10 seconds
- Tries again
- Up to 3 attempts total


Results append to same file automatically.

## Technical

- **API:** Overpass (OpenStreetMap) - Free
- **Language:** Python 
- **Dependencies:** requests library 
- **Cost:** totally free 

## Author

Built for IntelliVerse AI Growth Agent data collection pipeline.