
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'
SCREEN_NAME="regioheldentest"
CWD="cd RegioHeldenTest;"
START_COMMAND="screen -dmS ${SCREEN_NAME} /usr/bin/python3 manage.py runserver 0.0.0.0:8000;"
STOP_COMMAND="screen -X -S ${SCREEN_NAME} quit; screen -wipe;"
SCREEN_LIST="screen -ls;"
TEST_COMMAND="/usr/bin/python3 manage.py test --settings=RegioHeldenTest.test_settings;"

while getopts "sdrlt" opt; do
  case $opt in
    s)
      echo "${GREEN}Starting screen regioheldentest${NC}"
      COMMAND="${CWD} ${START_COMMAND}"
      ;;
    d)
      echo "${RED}Stopping screen regioheldentest${NC}"
      COMMAND="${CWD} ${STOP_COMMAND}"
      ;;
    r)
      echo "${ORANGE}Reloading screen regioheldentest${NC}"
      COMMAND="${CWD} ${STOP_COMMAND} ${START_COMMAND}"
      ;;
    l)
      echo "${BLUE}Showing screen status${NC}"
      COMMAND="${SCREEN_LIST}"
      ;;
    t)
      echo "${PURPLE}Executing test suite.${NC}"
      COMMAND="${CWD} ${TEST_COMMAND}"
      ;;
    \?)
      echo "\nHelp: sh run.sh -[s|d|r|l|t]"
      echo "Options for the RegioHeldenTest program:"
      echo "  ${GREEN}s${NC}: Start a new screen process with django runserver on port 8000."
      echo "  ${RED}d${NC}: Stop the django runserver screen process and remove dead processes."
      echo "  ${ORANGE}r${NC}: Reload the django runserver screen process (same as start/stop)."
      echo "  ${BLUE}l${NC}: Check the status of the screen processes."
      echo "  ${PURPLE}t${NC}: Execute the django test suite.\n"
      exit
      ;;
  esac
done

echo "(executing: ${COMMAND})"
vagrant ssh -- "${COMMAND} "