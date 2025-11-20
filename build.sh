#!/bin/bash

# Build script for different platforms

echo "Building AI Meeting Summarizer..."

# Clean previous builds
rm -rf dist/

# Build for current platform
npm run build

echo "Build complete! Check the dist/ folder for the installer."

