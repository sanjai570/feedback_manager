#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Feedback Collection System - Setup${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check Python version
echo -e "${YELLOW}[1/7]${NC} Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}\n"

# Create virtual environment
echo -e "${YELLOW}[2/7]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}[3/7]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "\n${YELLOW}[4/7]${NC} Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check for .env file
echo -e "\n${YELLOW}[5/7]${NC} Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ .env file created from template${NC}"
    echo -e "${YELLOW}⚠ Please edit .env with your Supabase credentials:${NC}"
    echo -e "${BLUE}   nano .env${NC}"
    echo ""
    read -p "Press Enter once you've configured the .env file..."
fi
echo -e "${GREEN}✓ Environment configured${NC}"

# Run migrations
echo -e "\n${YELLOW}[6/7]${NC} Running database migrations..."
python manage.py migrate
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migrations completed${NC}"
else
    echo -e "${RED}✗ Migration failed. Check your database connection.${NC}"
    exit 1
fi

# Create superuser
echo -e "\n${YELLOW}[7/7]${NC} Creating admin account..."
echo -e "${BLUE}You will be prompted to create a superuser account${NC}"
python manage.py createsuperuser

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${BLUE}Next steps:${NC}"
echo -e "${GREEN}1.${NC} Start the development server:"
echo -e "   ${BLUE}python manage.py runserver${NC}"
echo ""
echo -e "${GREEN}2.${NC} Access the application:"
echo -e "   Student Portal: ${BLUE}http://localhost:8000/${NC}"
echo -e "   Admin Login:    ${BLUE}http://localhost:8000/admin/login/${NC}"
echo ""
echo -e "${GREEN}3.${NC} For detailed setup guide:"
echo -e "   ${BLUE}cat SETUP_GUIDE.md${NC}"
echo ""
echo -e "${YELLOW}Happy coding!${NC}\n"
