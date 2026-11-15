#!/usr/bin/env bash

PROJECT="$HOME/recovery"

#export DATA="/run/media/theo/maindrive/fellowship/m4efad/recovery/data"
export DATA="$PROJECT/data"
export WORK="$PROJECT/newresults"
export CONF="$PROJECT/conf"

export PATH="$PROJECT/code:$PATH"
export PATH="$PROJECT/metatoolkit/metatoolkit/:$PATH"
export PATH="$PROJECT/maaslin3/R/:$PATH"

source "$PROJECT/venv/bin/activate"
