##### SETTINGS #####
set -g theme_color_scheme nord


##### ALIAS ######
alias config '/usr/bin/git --git-dir=$HOME/.myconfig/ --work-tree=$HOME'
alias ranger 'ranger --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"'
