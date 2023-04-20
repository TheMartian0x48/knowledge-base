# TODO
function knowledgebase_start() {
  python3 $HOME/.knowledgebase/python/main.py
}

# TODO
function knowledgebase_stop() {
  echo "knowledgebase_stop"
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
