# run the application in background
function knowledgebase_start() {
  $HOME/.knowledgebase/python/main.py &
  echo "started knowledgebase"
}

# find pid and kill it
function knowledgebase_stop() {
  pid=`ps -ef | grep '.knowledgebase/python/main.py' | awk '{print $2 " " $8'} | grep python3 | awk '{print $1}'`
  kill -9 $pid
  echo "stopped knowledgebase"
}

# TODO
function knowledgebase_add() {
  echo "knowledgebase_add"
}

function knowledgebase() {
  if [[ "$1" == "start" ]]; then
    knowledgebase_start
  elif [[ "$1" == "stop" ]]; then
    knowledgebase_stop
  elif [[ "$1" == "add" ]]; then
    knowledgebase_add
  else
    echo "argument must be one of \"start\", \"stop\" or \"add\""
  fi
}
