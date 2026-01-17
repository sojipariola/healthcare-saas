#!/bin/bash

# Healthcare SaaS Platform - Setup Script
# This script helps set up the development environment

set -e

echo "🏥 Healthcare SaaS Platform - Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.12 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1,2)
echo "Python version: $PYTHON_VERSION"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠${NC}  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} .env file created"
    echo -e "${YELLOW}⚠${NC}  Please edit .env file with your configuration before continuing"
    echo ""
    read -p "Press enter to continue after editing .env file..."
else
    echo -e "${GREEN}✓${NC} .env file exists"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p logs
mkdir -p media
mkdir -p staticfiles
mkdir -p static
echo -e "${GREEN}✓${NC} Directories created"

# Check if PostgreSQL is available
echo ""
echo "Checking database configuration..."
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✓${NC} PostgreSQL client found"
    echo -e "${YELLOW}⚠${NC}  Make sure PostgreSQL server is running"
else
    echo -e "${YELLOW}⚠${NC}  PostgreSQL client not found. Using Docker is recommended."
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start PostgreSQL (or use docker-compose up -d db)"
echo "3. Run migrations: python manage.py migrate"
echo "4. Create superuser: python manage.py createsuperuser"
echo "5. Run development server: python manage.py runserver"
echo ""
echo "Or use Docker:"
echo "  docker-compose up -d"
echo ""
echo "For more information, see README.md"
echo "=========================================="
