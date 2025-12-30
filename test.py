import requests
import json
import os
import time

def get_kids_attractions(city_name, max_retries=3):
    url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json][timeout:90];
    (
      area["name"~"{city_name}",i][admin_level~"4|5|8"];
      area["name"~"{city_name}",i][place~"city|borough"];
    )->.searchArea;
    (
      nwr["leisure"~"playground|theme_park|water_park"](area.searchArea);
      nwr["tourism"~"zoo|aquarium|museum"](area.searchArea);
      nwr["shop"="toy"](area.searchArea);
    );
    out center;
    """

    # 🆕 RETRY LOGIC
    for attempt in range(max_retries):
        try:
            print(f"Searching {city_name}... (Attempt {attempt + 1}/{max_retries})")
            response = requests.post(url, data={"data": query}, timeout=120)
            
            if response.status_code != 200:
                print(f"API returned status {response.status_code}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # 10, 20, 30 seconds
                    print(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Failed after {max_retries} attempts")
                    return []
            
            data = response.json() # to get JSON response
            elements = data.get("elements", []) # get attractions
            
            if not elements:
                print(f"No data returned for {city_name}")
                return []
            
            print(f"Found {len(elements)} raw results for {city_name}")
            break
            
        except requests.exceptions.Timeout:
            print(f"Request timed out")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 15
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts")
                return []
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)
            else:
                return []
    
    city_results = []
    for item in elements:
        tags = item.get("tags", {})
        name = tags.get("name")
        if not name: continue

        lat = item.get("lat") or item.get("center", {}).get("lat")
        lon = item.get("lon") or item.get("center", {}).get("lon")
        if lat is None or lon is None: continue

        # Calculate SEO saturation score
        seo_score = 0
        if "website" in tags: seo_score += 4
        if "phone" in tags: seo_score += 3
        if "wikipedia" in tags or "wikidata" in tags: seo_score += 3
        
        # Calculate search popularity score
        pop_score = min(10, len(tags))
        
        city_results.append({
            "city": city_name.title(),
            "name": name,
            "type": (tags.get("tourism") or tags.get("leisure") or "Attraction").title(),
            "coordinates": {"lat": lat, "lng": lon},
            "seo_saturation": seo_score,
            "search_popularity": pop_score
        })
    
    return city_results

def run_and_save(city_to_add):
    filename = "test.json" # data file name
    
    if os.path.exists(filename):
        with open(filename, "r") as f:
            master_list = json.load(f) 
    else:
        master_list = [] 

    new_data = get_kids_attractions(city_to_add)
    
    # to not add duplicates
    existing_names = {item["name"] for item in master_list}
    
    added_count = 0
    for attraction in new_data:
        if attraction["name"] not in existing_names:
            master_list.append(attraction)
            added_count += 1

    with open(filename, "w") as f:
        json.dump(master_list, f, indent=4)

    print(f"Added {added_count} attractions from {city_to_add}.")
    print(f"Total attractions: {len(master_list)}")

    # Testing 
    if added_count == 0:
        print("No new attractions were added. Maybe duplicates.")
    return added_count
if __name__ == "__main__":
    city = "berlin"
    run_and_save(city)