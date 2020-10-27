":se backup? backupdir? backupext? Plugins will be downloaded under the specified directory.
call plug#begin('~/.vim/plugged')

" Declare the list of plugins.
Plug 'tpope/vim-sensible'
Plug 'arcticicestudio/nord-vim'
Plug 'frazrepo/vim-rainbow'

" List ends here. Plugins become visible to Vim after this call.
call plug#end()

set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc
let g:rainbow_active = 1
