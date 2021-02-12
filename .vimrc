" For color scheme see: https://github.com/arcticicestudio/nord-vim
colo nord

set number
set relativenumber
syntax on
set showmode
set autoindent
set mouse=a
filetype indent on
set tabstop=4
set shiftwidth=4
set expandtab
set linebreak
set showmatch
set ignorecase
set smartcase
set backup
set undofile
set backupdir=~/.vim/.backup//  
set directory=~/.vim/.swp//
set undodir=~/.vim/.undo//
set history=1000
set undolevels=1000
set backspace=indent,eol,start
set termguicolors
set noshowmode
set cursorline
set clipboard=unnamedplus
" Disable quote concealing in JSON files
let g:vim_json_conceal=0
" Map :Q to :q in case you type too quick
command! Q :q
