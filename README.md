# Travel Booking Website Asset Generator

This script automatically generates and optimizes visual assets for a travel booking website using WordPress + Hello Elementor Theme + Travelpayouts plugin.

## Features

- Generates beautiful gradient background images
- Creates destination placeholder images with text overlays
- Generates SVG icons with gradients
- Optimizes images for web use (WebP format)
- Creates a manifest file for asset tracking
- Organizes assets in a structured directory

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python scripts/generate_assets.py
```

The script will:
1. Create necessary directories
2. Generate and optimize images
3. Create SVG icons
4. Create a manifest file

## Directory Structure

```
assets/
├── images/
│   ├── hero/
│   │   └── background.webp
│   └── destinations/
│       ├── paris.webp
│       ├── tokyo.webp
│       └── ...
├── icons/
│   ├── booking.svg
│   ├── support.svg
│   └── ...
└── assets_manifest.json
```

## Asset Usage in WordPress

1. Upload the generated assets to your WordPress media library
2. Use in Elementor:
   - Hero section: Use the gradient background image
   - Destination cards: Use the destination images
   - Feature icons: Use the SVG icons

## Color Palette

The script uses a travel-friendly color palette:

```css
:root {
    --primary: #2563eb;     /* Ocean Blue */
    --secondary: #f97316;   /* Sunset Orange */
    --accent: #10b981;      /* Nature Green */
    --dark: #1e293b;        /* Deep Blue */
    --light: #f8fafc;       /* Off-White */
}
```

## Font Recommendations

- Headings: 'Poppins' (Google Fonts)
- Body: 'Inter' (Google Fonts)

## Performance Optimization

- Images are automatically saved in WebP format
- SVG icons are optimized for web use
- Manifest file tracks all assets
- Gradient-based design for fast loading

## Customization

You can customize the generated assets by modifying:
1. The color palette in the script
2. The destination list
3. The feature icons and their names
4. The image dimensions and quality settings

## License

All generated assets are from royalty-free sources:
- Unsplash: [License](https://unsplash.com/license)
- Pexels: [License](https://www.pexels.com/license/) 