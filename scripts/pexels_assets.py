import os
import json
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

PEXELS_API_KEY = "ildgOxIfTcK5a519pzCWrKx2oBsvQsSrl51YVyymyTkHu4CTC5TuUUoO"
HEADERS = {"Authorization": PEXELS_API_KEY}

# Define destinations with their queries and metadata
DESTINATIONS = {
    "maldives": {
        "query": "maldives aerial beach resort",
        "title": "Maldives",
        "description": "Paradise islands with crystal clear waters",
        "price": "From $999",
        "rating": 4.9,
        "min_duration": 15
    },
    "bali": {
        "query": "bali beach resort aerial",
        "title": "Bali",
        "description": "Tropical paradise with rich culture",
        "price": "From $799",
        "rating": 4.8,
        "min_duration": 15
    },
    "santorini": {
        "query": "santorini beach aerial view",
        "title": "Santorini",
        "description": "Stunning white buildings and blue domes",
        "price": "From $899",
        "rating": 4.7,
        "min_duration": 15
    },
    "caribbean": {
        "query": "caribbean beach resort aerial",
        "title": "Caribbean",
        "description": "Crystal clear waters and white sand beaches",
        "price": "From $849",
        "rating": 4.8,
        "min_duration": 15
    },
    "phuket": {
        "query": "phuket beach resort aerial",
        "title": "Phuket",
        "description": "Exotic beaches and vibrant nightlife",
        "price": "From $699",
        "rating": 4.6,
        "min_duration": 15
    },
    "seychelles": {
        "query": "seychelles beach aerial view",
        "title": "Seychelles",
        "description": "Pristine beaches and unique wildlife",
        "price": "From $1099",
        "rating": 4.9,
        "min_duration": 15
    },
    "mexico": {
        "query": "mexico beach resort aerial",
        "title": "Mexico",
        "description": "Vibrant culture and stunning coastlines",
        "price": "From $699",
        "rating": 4.7,
        "min_duration": 15
    },
    "thailand": {
        "query": "thailand beach resort aerial",
        "title": "Thailand",
        "description": "Golden temples and tropical islands",
        "price": "From $549",
        "rating": 4.6,
        "min_duration": 15
    },
    "australia": {
        "query": "australia beach aerial view",
        "title": "Australia",
        "description": "Great Barrier Reef and white sand beaches",
        "price": "From $899",
        "rating": 4.8,
        "min_duration": 15
    },
    "new zealand": {
        "query": "new zealand beach aerial view",
        "title": "New Zealand",
        "description": "Dramatic landscapes and pristine beaches",
        "price": "From $999",
        "rating": 4.9,
        "min_duration": 15
    },
    "portugal": {
        "query": "portugal beach aerial view",
        "title": "Portugal",
        "description": "Historic charm and Atlantic coast",
        "price": "From $649",
        "rating": 4.7,
        "min_duration": 15
    },
    "greece": {
        "query": "greece beach aerial view",
        "title": "Greece",
        "description": "Ancient history meets stunning beaches",
        "price": "From $799",
        "rating": 4.8,
        "min_duration": 15
    },
    "fiji": {
        "query": "fiji beach resort aerial",
        "title": "Fiji",
        "description": "Overwater bungalows and coral reefs",
        "price": "From $899",
        "rating": 4.8,
        "min_duration": 15
    },
    "hawaii": {
        "query": "hawaii beach aerial view",
        "title": "Hawaii",
        "description": "Volcanic landscapes and tropical beaches",
        "price": "From $799",
        "rating": 4.7,
        "min_duration": 15
    },
    "bora bora": {
        "query": "bora bora beach resort aerial",
        "title": "Bora Bora",
        "description": "Luxury overwater villas and turquoise lagoons",
        "price": "From $1299",
        "rating": 4.9,
        "min_duration": 15
    },
    "mauritius": {
        "query": "mauritius beach resort aerial",
        "title": "Mauritius",
        "description": "Tropical paradise with luxury resorts",
        "price": "From $899",
        "rating": 4.8,
        "min_duration": 15
    }
}

# Define featured experience videos
FEATURED_VIDEOS = [
    {
        "query": "luxury yacht sailing sunset",
        "title": "Luxury Sailing Adventures",
        "description": "Experience the freedom of sailing through crystal-clear waters at sunset",
        "keywords": ["sailing", "yacht", "luxury", "sunset"],
        "min_duration": 30
    },
    {
        "query": "scuba diving coral reef fish",
        "title": "Underwater Discovery",
        "description": "Explore vibrant coral reefs and marine life in pristine waters",
        "keywords": ["diving", "marine life", "adventure", "ocean"],
        "min_duration": 30
    },
    {
        "query": "beach resort infinity pool sunset",
        "title": "Luxury Beach Resorts",
        "description": "Indulge in world-class amenities with breathtaking ocean views",
        "keywords": ["resort", "luxury", "pool", "sunset"],
        "min_duration": 30
    }
]

def create_directories():
    """Create necessary directories if they don't exist"""
    dirs = [
        "assets/videos/destinations",
        "assets/videos/featured",
        "assets/videos/hero",
        "assets/thumbnails"
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

def generate_thumbnail(video_url, save_path):
    """Generate thumbnail from video first frame"""
    # In a real implementation, you would extract the first frame
    # For now, we'll create a placeholder
    response = requests.get(video_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((1280, 720), Image.Resampling.LANCZOS)
    img.save(save_path, 'WEBP', quality=85)
    return save_path

def fetch_destination_videos():
    """Fetch destination videos from Pexels"""
    manifest = {"destinations": {}}
    
    for dest_key, dest_data in DESTINATIONS.items():
        print(f"Fetching video for {dest_key}...")
        response = requests.get(
            f"https://api.pexels.com/videos/search?query={dest_data['query']}&per_page=5&orientation=landscape",
            headers=HEADERS
        )
        data = response.json()
        
        if "videos" in data and data["videos"]:
            # Find video that meets minimum duration requirement
            suitable_video = next(
                (v for v in data["videos"] if v["duration"] >= dest_data["min_duration"]),
                data["videos"][0]
            )
            
            video_files = suitable_video["video_files"]
            
            # Get HD quality video
            hd_video = next(
                (v for v in video_files if v["quality"] == "hd" and v["width"] >= 1920),
                video_files[0]
            )
            
            # Save video
            video_filename = f"{dest_key}.mp4"
            video_path = f"assets/videos/destinations/{video_filename}"
            thumbnail_path = f"assets/thumbnails/{dest_key}.webp"
            
            # Download video
            video_response = requests.get(hd_video["link"])
            with open(video_path, "wb") as f:
                f.write(video_response.content)
            
            # Generate thumbnail
            generate_thumbnail(suitable_video["image"], thumbnail_path)
            
            # Add to manifest
            manifest["destinations"][dest_key] = {
                "title": dest_data["title"],
                "description": dest_data["description"],
                "price": dest_data["price"],
                "rating": dest_data["rating"],
                "video_path": video_path,
                "thumbnail_path": thumbnail_path,
                "duration": suitable_video["duration"],
                "width": hd_video["width"],
                "height": hd_video["height"],
                "photographer": suitable_video["user"]["name"],
                "original_url": suitable_video["url"]
            }
    
    return manifest

def fetch_featured_videos():
    """Fetch featured experience videos"""
    videos = []
    
    for video_data in FEATURED_VIDEOS:
        print(f"Fetching featured video: {video_data['title']}...")
        response = requests.get(
            f"https://api.pexels.com/videos/search?query={video_data['query']}&per_page=5&orientation=landscape",
            headers=HEADERS
        )
        data = response.json()
        
        if "videos" in data and data["videos"]:
            # Find video that meets minimum duration requirement
            suitable_video = next(
                (v for v in data["videos"] if v["duration"] >= video_data["min_duration"]),
                data["videos"][0]
            )
            
            video_files = suitable_video["video_files"]
            
            # Get HD quality video
            hd_video = next(
                (v for v in video_files if v["quality"] == "hd" and v["width"] >= 1920),
                video_files[0]
            )
            
            # Create filename from title
            filename = video_data['title'].lower().replace(' ', '_') + '.mp4'
            video_path = f"assets/videos/featured/{filename}"
            thumbnail_path = f"assets/thumbnails/featured_{filename.replace('.mp4', '.webp')}"
            
            # Download video
            video_response = requests.get(hd_video["link"])
            with open(video_path, "wb") as f:
                f.write(video_response.content)
            
            # Generate thumbnail
            generate_thumbnail(suitable_video["image"], thumbnail_path)
            
            videos.append({
                "title": video_data["title"],
                "description": video_data["description"],
                "keywords": video_data["keywords"],
                "video_path": video_path,
                "thumbnail_path": thumbnail_path,
                "duration": suitable_video["duration"],
                "width": hd_video["width"],
                "height": hd_video["height"],
                "photographer": suitable_video["user"]["name"],
                "original_url": suitable_video["url"]
            })
    
    return videos

def fetch_hero_video():
    """Fetch hero background video"""
    print("Fetching hero video...")
    response = requests.get(
        "https://api.pexels.com/videos/search?query=aerial ocean waves beach sunset&per_page=5&orientation=landscape",
        headers=HEADERS
    )
    data = response.json()
    
    if "videos" in data and data["videos"]:
        # Find longest video
        video = max(data["videos"], key=lambda x: x["duration"])
        video_files = video["video_files"]
        
        # Get highest quality video
        hd_video = next(
            (v for v in video_files if v["quality"] == "hd" and v["width"] >= 1920),
            video_files[0]
        )
        
        # Save video
        video_path = "assets/videos/hero/ocean_sunset.mp4"
        video_response = requests.get(hd_video["link"])
        with open(video_path, "wb") as f:
            f.write(video_response.content)
        
        return {
            "path": video_path,
            "duration": video["duration"],
            "width": hd_video["width"],
            "height": hd_video["height"],
            "photographer": video["user"]["name"],
            "original_url": video["url"]
        }

def main():
    """Main function to fetch and process all assets"""
    create_directories()
    
    # Initialize manifest
    manifest = {
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
        "destinations": {},
        "featured_videos": [],
        "hero_video": None
    }
    
    # Fetch destination videos
    print("Fetching destination videos...")
    dest_manifest = fetch_destination_videos()
    manifest.update(dest_manifest)
    
    # Fetch featured videos
    print("Fetching featured videos...")
    featured_videos = fetch_featured_videos()
    manifest["featured_videos"] = featured_videos
    
    # Fetch hero video
    print("Fetching hero video...")
    hero_video = fetch_hero_video()
    manifest["hero_video"] = hero_video
    
    # Save manifest
    with open("assets/assets_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print("Asset generation completed!")

if __name__ == "__main__":
    main() 