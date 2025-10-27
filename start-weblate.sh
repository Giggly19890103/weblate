#!/bin/bash

# Weblate Startup Script
# One-click operation to start Weblate server and Celery workers

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Weblate Startup Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Navigate to Weblate directory (IMPORTANT: Must be here before starting Celery)
cd $HOME/Documents/weblate-weblate-5.13.3

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source $HOME/weblate-env/bin/activate

# Set Django settings module (required for Celery to work properly)
export DJANGO_SETTINGS_MODULE=weblate.settings

# Check if Celery is already running
if pgrep -f "celery.*weblate" > /dev/null; then
    echo -e "${YELLOW}Celery workers are already running!${NC}"
else
    echo -e "${GREEN}Starting Celery workers...${NC}"
    # Start Celery with proper configuration (from Weblate directory)
    nohup celery -A weblate.utils worker \
        --pidfile=$HOME/weblate-celery.pid \
        --logfile=$HOME/weblate-celery%I.log \
        --loglevel=DEBUG \
        --queues=celery,notify,memory,translate,backup \
        --beat \
        -n celery@$(hostname) \
        > /dev/null 2>&1 &
    sleep 3
    echo -e "${GREEN}✓ Celery workers started${NC}"
fi

# Check if server is already running
if pgrep -f "manage.py runserver" > /dev/null; then
    echo -e "${YELLOW}Django server is already running!${NC}"
else
    echo -e "${GREEN}Starting Django development server...${NC}"
    nohup python3 manage.py runserver > server.log 2>&1 &
    sleep 2
    echo -e "${GREEN}✓ Django server started on http://localhost:8000${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Weblate is now running!${NC}"
echo ""
echo -e "  Access Weblate at: ${BLUE}http://localhost:8000${NC}"
echo ""
echo -e "  Logs:"
echo -e "    - Server:  ${YELLOW}tail -f $HOME/Documents/weblate-weblate-5.13.3/server.log${NC}"
echo -e "    - Celery:  ${YELLOW}tail -f $HOME/weblate-celery.log${NC}"
echo ""
echo -e "  To stop Weblate, run: ${YELLOW}./stop-weblate.sh${NC}"
echo -e "${BLUE}========================================${NC}"


