# Offline Deployment Guide

This guide explains how to deploy the Project Manager application in a closed network environment without internet access.

## Prerequisites

- Python 3.7 or higher
- No internet access required after setup

## Included Local Assets

The application now includes all necessary external assets locally:

### CSS/JS Libraries
- **Bootstrap 5.1.3**: Complete CSS and JS bundle
  - Located: `static/lib/bootstrap/`
- **Font Awesome 6.0.0**: Icons and fonts
  - Located: `static/lib/fontawesome/`
  - Includes webfonts: fa-solid-900.woff2, fa-regular-400.woff2, fa-brands-400.woff2
- **Chart.js**: Charts and data visualization
  - Located: `static/lib/chartjs/`

### Python Dependencies
- **Flask 2.3.3**: Web framework
- **Werkzeug 2.3.7**: WSGI utilities
- Standard library modules (no external dependencies):
  - json, os, sys, datetime, enum, typing, uuid, subprocess, time, webbrowser, threading, signal, logging, glob, shutil

## Installation Steps

### 1. Copy Application Files
Copy the entire project directory to your target machine:
```
project_manager/
├── static/lib/          # Local assets (included)
├── templates/           # HTML templates (updated for local assets)
├── *.py                 # Python application files
├── requirements.txt     # Python dependencies
├── projects.json        # Data file
└── OFFLINE_DEPLOYMENT.md # This guide
```

### 2. Install Python Dependencies
If pip is available (for initial setup):
```bash
pip install -r requirements.txt
```

For completely offline installation:
1. Download packages on a machine with internet:
   ```bash
   pip download -r requirements.txt -d offline_packages/
   ```
2. Copy `offline_packages/` to target machine
3. Install offline:
   ```bash
   pip install -r requirements.txt --no-index --find-links offline_packages/
   ```

### 3. Verify Installation
Test that all assets are available:
```bash
# Check if Flask is installed
python -c "import flask; print('Flask version:', flask.__version__)"

# Check if static assets exist
ls -la static/lib/bootstrap/css/bootstrap.min.css
ls -la static/lib/fontawesome/css/all-local.min.css
ls -la static/lib/chartjs/chart.min.js
```

## Running the Application

### Web Interface (Recommended)
```bash
python web_app.py
```
Access at: http://localhost:8083

### Alternative Web Interface
```bash
python start_web.py
```
Access at: http://localhost:8082

### CLI Interface
```bash
python cli.py
```

## Features Available Offline

✅ **Fully Available:**
- Complete web interface with Bootstrap styling
- Font Awesome icons
- Interactive charts and data visualization
- Project management (CRUD operations)
- Category management
- Task tracking
- Progress monitoring
- Data persistence (JSON files)
- Project templates
- Batch operations
- Export/Import functionality

✅ **Limited (Optional Features):**
- Email notifications (requires SMTP server configuration)
- SMS notifications (requires external service configuration)

## File Structure After Deployment

```
project_manager/
├── static/
│   ├── css/
│   │   └── style.css                    # Custom styles
│   ├── js/
│   │   └── app.js                       # Custom JavaScript
│   └── lib/                             # Local libraries
│       ├── bootstrap/
│       │   ├── css/bootstrap.min.css
│       │   └── js/bootstrap.bundle.min.js
│       ├── fontawesome/
│       │   ├── css/all-local.min.css    # Updated with local paths
│       │   └── webfonts/                # Font files
│       │       ├── fa-solid-900.woff2
│       │       ├── fa-regular-400.woff2
│       │       └── fa-brands-400.woff2
│       └── chartjs/
│           └── chart.min.js
├── templates/                           # Updated for local assets
├── projects.json                        # Data storage
├── requirements.txt                     # Python dependencies
└── [application files...]
```

## Security Considerations

- All external CDN dependencies have been replaced with local files
- No external network requests are made during normal operation
- Data is stored locally in JSON files
- Web interface runs on localhost only by default

## Troubleshooting

### Missing Icons or Styles
- Verify `static/lib/` directory contains all files
- Check browser console for 404 errors
- Ensure Flask is serving static files correctly

### Chart.js Not Working
- Confirm `static/lib/chartjs/chart.min.js` exists
- Check browser console for JavaScript errors

### Font Issues
- Verify webfonts are in `static/lib/fontawesome/webfonts/`
- Check that `all-local.min.css` references correct font paths

## Performance Notes

- Application runs entirely locally
- No internet connectivity required after setup
- Data persistence through JSON files
- Suitable for air-gapped environments

## Backup and Migration

To backup your data:
```bash
# Backup all project data
cp projects.json projects-backup.json

# Or use the web interface export functionality
```

To migrate to another system:
1. Copy entire project directory
2. Install Python dependencies
3. Run application

Your project manager is now ready for offline use in a closed network environment!