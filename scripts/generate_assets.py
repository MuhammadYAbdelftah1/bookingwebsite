import os
import json
from PIL import Image, ImageDraw, ImageFont
import shutil
from pathlib import Path
import logging
from datetime import datetime
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AssetGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.assets_dir = self.base_dir / 'assets'
        self.images_dir = self.assets_dir / 'images'
        self.icons_dir = self.assets_dir / 'icons'
        self.manifest_file = self.assets_dir / 'assets_manifest.json'
        
        # Create directories if they don't exist
        self._create_directories()
        
        # Asset configuration
        self.destinations = [
            'Paris', 'Tokyo', 'Dubai', 'Rome', 'New York', 'Bali', 'Maldives', 'London'
        ]
        
        self.features = [
            {'name': 'Easy Booking', 'icon': 'booking'},
            {'name': '24/7 Support', 'icon': 'support'},
            {'name': 'Trusted Worldwide', 'icon': 'trust'},
            {'name': 'Best Price Guarantee', 'icon': 'price'},
            {'name': 'Secure Payment', 'icon': 'security'},
            {'name': 'Travel Insurance', 'icon': 'insurance'}
        ]

        # Color palette
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#f97316',
            'accent': '#10b981',
            'dark': '#1e293b',
            'light': '#f8fafc'
        }

    def _create_directories(self):
        """Create necessary directories for assets."""
        directories = [
            self.assets_dir,
            self.images_dir,
            self.images_dir / 'hero',
            self.images_dir / 'destinations',
            self.icons_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

    def _generate_gradient_image(self, width, height, colors, filename):
        """Generate a gradient image."""
        try:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # Create gradient
            for y in range(height):
                # Interpolate between colors
                r = int((1 - y/height) * int(colors[0][1:3], 16) + (y/height) * int(colors[1][1:3], 16))
                g = int((1 - y/height) * int(colors[0][3:5], 16) + (y/height) * int(colors[1][3:5], 16))
                b = int((1 - y/height) * int(colors[0][5:7], 16) + (y/height) * int(colors[1][5:7], 16))
                
                # Draw horizontal line
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Save image
            image.save(filename, 'WEBP', quality=85)
            logger.info(f"Generated gradient image: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error generating gradient image: {e}")
            return None

    def _generate_destination_image(self, destination, width=800, height=600):
        """Generate a placeholder image for a destination."""
        try:
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # Add gradient background
            colors = [self.colors['primary'], self.colors['secondary']]
            for y in range(height):
                r = int((1 - y/height) * int(colors[0][1:3], 16) + (y/height) * int(colors[1][1:3], 16))
                g = int((1 - y/height) * int(colors[0][3:5], 16) + (y/height) * int(colors[1][3:5], 16))
                b = int((1 - y/height) * int(colors[0][5:7], 16) + (y/height) * int(colors[1][5:7], 16))
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add destination name
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            text = destination
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Add text shadow
            draw.text((x+2, y+2), text, font=font, fill='black')
            draw.text((x, y), text, font=font, fill='white')
            
            # Save image
            filename = self.images_dir / 'destinations' / f"{destination.lower().replace(' ', '_')}.webp"
            image.save(filename, 'WEBP', quality=85)
            logger.info(f"Generated destination image: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error generating destination image: {e}")
            return None

    def generate_hero_background(self):
        """Generate hero background image."""
        try:
            filename = self.images_dir / 'hero' / 'background.webp'
            colors = [self.colors['primary'], self.colors['accent']]
            
            if self._generate_gradient_image(1920, 1080, colors, filename):
                return {
                    'type': 'image',
                    'path': str(filename.relative_to(self.base_dir)),
                    'source': 'Generated',
                    'alt': 'Travel background image'
                }
        except Exception as e:
            logger.error(f"Error generating hero background: {e}")
        return None

    def generate_destination_images(self):
        """Generate images for destinations."""
        destination_assets = []
        
        for destination in self.destinations:
            try:
                image_path = self._generate_destination_image(destination)
                if image_path:
                    destination_assets.append({
                        'name': destination,
                        'path': str(image_path.relative_to(self.base_dir)),
                        'source': 'Generated',
                        'alt': f'{destination} travel destination'
                    })
            except Exception as e:
                logger.error(f"Error generating image for {destination}: {e}")
        
        return destination_assets

    def generate_feature_icons(self):
        """Generate SVG icons for features."""
        icons = []
        for feature in self.features:
            icon_path = self.icons_dir / f"{feature['icon']}.svg"
            
            # Create simple SVG icon with gradient
            svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:{self.colors['primary']};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:{self.colors['secondary']};stop-opacity:1" />
                    </linearGradient>
                </defs>
                <path fill="url(#grad)" d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99z"/>
            </svg>'''
            
            with open(icon_path, 'w') as f:
                f.write(svg_content)
            
            icons.append({
                'name': feature['name'],
                'path': str(icon_path.relative_to(self.base_dir)),
                'source': 'Generated SVG',
                'alt': f"{feature['name']} icon"
            })
        
        return icons

    def generate_manifest(self, assets):
        """Generate manifest file for all assets."""
        manifest = {
            'generated_at': datetime.now().isoformat(),
            'assets': assets,
            'color_palette': self.colors
        }
        
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Generated manifest file: {self.manifest_file}")

    def run(self):
        """Main execution method."""
        logger.info("Starting asset generation...")
        
        assets = {
            'hero': self.generate_hero_background(),
            'destinations': self.generate_destination_images(),
            'icons': self.generate_feature_icons()
        }
        
        self.generate_manifest(assets)
        logger.info("Asset generation completed!")

if __name__ == '__main__':
    generator = AssetGenerator()
    generator.run() 