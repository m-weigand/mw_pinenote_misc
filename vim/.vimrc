" for flake8, create a configuration file: ~/.config/flake8:
"	 [flake8]
"	ignore = F403
"
" install vim-plug
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif


" Specify a directory for plugins (for Neovim: ~/.local/share/nvim/plugged)
call plug#begin('~/.vim/plugged')

Plug 'https://github.com/vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'https://github.com/majutsushi/tagbar'
" Plug 'https://github.com/tpope/vim-fugitive'
" Plug 'https://github.com/scrooloose/nerdtree'
" Plug 'https://github.com/vim-syntastic/syntastic'

" Plug 'Valloric/YouCompleteMe', { 'do': 'python3 ./install.py' }
" Plug 'Valloric/YouCompleteMe', { 'commit':'d98f896', 'do': 'python3 ./install.py' }
Plug 'https://github.com/ervandew/supertab'
Plug 'https://github.com/tpope/vim-commentary'

Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

Plug 'https://github.com/fisadev/vim-isort'

" Plug 'https://github.com/sheerun/vim-polyglot'
" let g:polyglot_disabled = ['latex']

Plug 'https://github.com/ntpeters/vim-better-whitespace'
" Plug 'https://github.com/tell-k/vim-autopep8'
Plug 'https://github.com/nvie/vim-flake8'

Plug 'https://github.com/vimwiki/vimwiki.git', {'branch': 'dev'}

" Plug 'https://github.com/jplaut/vim-arduino-ino'
Plug 'https://github.com/clinstid/eink.vim'

" Plug 'lervag/vimtex'
let g:tex_flavor='latex'
let g:vimtex_view_method='zathura'
let g:vimtex_quickfix_mode=0
set conceallevel=1
let g:tex_conceal='abdmg'

" Initialize plugin system
call plug#end()

"*****************************************************************************
"" Basic Setup
"*****************************************************************************"
"" Encoding
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8

"" Fix backspace indent
set backspace=indent,eol,start

"" Tabs. May be overriten by autocmd rules
set tabstop=4
set softtabstop=0
set shiftwidth=4
set expandtab

"" Map leader to ,
let mapleader=','
let maplocalleader = "."

"" Enable hidden buffers
set hidden

"" Searching
set hlsearch
set incsearch
set ignorecase
set smartcase

"" Encoding
set bomb
set binary
set ttyfast

"" Directories for swp files
set nobackup
set noswapfile

set fileformats=unix,dos,mac
set showcmd
set shell=/bin/bash

"*****************************************************************************
"" Visual Settings
"*****************************************************************************
syntax off
set ruler
set number

let no_buffers_menu=1
" if empty(glob('~/.vim/colors/molokai.vim'))
" 	echo "Downloading molokai color scheme"
" 	silent !curl -fLo ~/.vim/colors/molokai.vim --create-dirs
" 		\ https://github.com/tomasr/molokai/raw/master/colors/molokai.vim
" endif
" "" colorscheme molokai

set background=light
colorscheme eink

set mousemodel=popup
set t_Co=16
set nocursorline
set guioptions=egmrti
set gfn=Monospace\ 10

let g:CSApprox_loaded = 1

if $COLORTERM == 'gnome-terminal'
    set term=gnome-256color
else
    if $TERM == 'xterm'
	set term=xterm-256color
    endif
endif

if &term =~ '256color'
  set t_ut=
endif

"" Disable the blinking cursor.
set gcr=a:blinkon0
set scrolloff=3

"" Status bar
set laststatus=2

"" Use modeline overrides
set modeline
set modelines=10

set title
set titleold="Terminal"
set titlestring=%F

set statusline=%F%m%r%h%w%=(%{&ff}/%Y)\ (line\ %l\/%L,\ col\ %c)\

"" no one is really happy until you have these shortcuts
cnoreabbrev W! w!
cnoreabbrev Q! q!
cnoreabbrev Qall! qall!
cnoreabbrev Wq wq
cnoreabbrev Wa wa
cnoreabbrev wQ wq
cnoreabbrev WQ wq
cnoreabbrev W w
cnoreabbrev Q q
cnoreabbrev Qall qall

"" The PC is fast enough, do syntax highlight syncing from start
augroup vimrc-sync-fromstart
  autocmd!
  autocmd BufEnter * :syntax sync fromstart
augroup END

"" Remember cursor position
augroup vimrc-remember-cursor-position
  autocmd!
  autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g`\"" | endif
augroup END


"*****************************************************************************
"" Mappings
"*****************************************************************************
"" Split
noremap <Leader>h :<C-u>split<CR>
noremap <Leader>v :<C-u>vsplit<CR>

"" Git
noremap <Leader>ga :Gwrite<CR>
noremap <Leader>gc :Gcommit<CR>
noremap <Leader>gsh :Gpush<CR>
noremap <Leader>gll :Gpull<CR>
noremap <Leader>gs :Gstatus<CR>
noremap <Leader>gb :Gblame<CR>
noremap <Leader>gd :Gvdiff<CR>
noremap <Leader>gr :Gremove<CR>

"" Tabs
nnoremap <Tab> gt
nnoremap <S-Tab> gT
nnoremap <silent> <S-t> :tabnew<CR>

"" Buffer nav
noremap <leader>z :bp<CR>
noremap <leader>q :bp<CR>
noremap <leader>x :bn<CR>
noremap <leader>w :bn<CR>

"" Close buffer
noremap <leader>c :bd<CR>

" vim-airline
let g:airline_theme = 'powerlineish'
let g:airline#extensions#branch#enabled = 1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ''
let g:airline#extensions#tabline#left_alt_sep = ''

if !exists('g:airline_symbols')
	let g:airline_symbols = {}
endif

" powerline symbols
let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''
let g:airline_symbols.branch = ''
let g:airline_symbols.readonly = ''
let g:airline_symbols.linenr = ''
let g:airline#extensions#virtualenv#enabled = 1
let g:airline#extensions#tagbar#enabled = 1
let g:airline#extensions#syntastic#enabled = 1

" nmap <buffer> <F5> :w<Esc>mwG:r!python %<CR>`.
nmap <F5> <Esc>:w<CR>:!python %<CR>

" grammar spelling
set spell spelllang=en_us
" next spelling word
noremap <leader>t ]s


" disable concealing in latex
let g:tex_conceal=""
au FileType * setl cole=0

" Tagbar
nmap <silent> <F4> :TagbarToggle<CR>
let g:tagbar_autofocus = 1

"" NERDTree configuration
" let g:NERDTreeChDirMode=2
" let g:NERDTreeIgnore=['\.rbc$', '\~$', '\.pyc$', '\.db$', '\.sqlite$', '__pycache__']
" let g:NERDTreeSortOrder=['^__\.py$', '\/$', '*', '\.swp$', '\.bak$', '\~$']
" let g:NERDTreeShowBookmarks=1
" let g:nerdtree_tabs_focus_on_files=1
" let g:NERDTreeMapOpenInTabSilent = '<RightMouse>'
" let g:NERDTreeWinSize = 20
" set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*.pyc,*.db,*.sqlite
" nnoremap <silent> <F2> :NERDTreeFind<CR>
" noremap <F3> :NERDTreeToggle<CR>

" syntastic
let g:syntastic_always_populate_loc_list=1
let g:syntastic_error_symbol='✗'
let g:syntastic_warning_symbol='⚠'
let g:syntastic_style_error_symbol = '✗'
let g:syntastic_style_warning_symbol = '⚠'
let g:syntastic_auto_loc_list=1
let g:syntastic_aggregate_errors = 1
let g:syntastic_python_checkers=['python', 'flake8']
let g:syntastic_python_flake8_post_args='--ignore W391,E402,F403,F405'
let g:syntastic_aggregate_errors=1
let g:syntastic_check_on_open = 1
let g:syntastic_disabled_filetypes=['tex', 'rst']
let g:syntastic_tex_checkers=['']
let g:syntastic_rst_checkers=['']


"python with virtualenv support
" py3 << EOF
" import os
" import sys
" if 'VIRTUAL_ENV' in os.environ:
"   project_base_dir = os.environ['VIRTUAL_ENV']
"   activate_this = os.path.join(project_base_dir, 'bin/activate_this.py')
"   # execfile(activate_this, dict(__file__=activate_this))

"   with open(activate_this) as f:
"     code = compile(f.read(), activate_this, 'exec')
"     exec(code, dict(__file__=activate_this))
" EOF

" autocompleteme
" let g:ycm_autoclose_preview_window_after_insertion = 1

" let g:UltiSnipsExpandTrigger="<c-j>"
" let g:UltiSnipsJumpForwardTrigger="<c-j>"
" let g:UltiSnipsJumpBackwardTrigger="<c-k>"

" let g:ycm_key_list_select_completion=[]
" let g:ycm_key_list_previous_completion=[]

" make YCM compatible with UltiSnips (using supertab)
let g:ycm_key_list_select_completion = ['<C-n>', '<Down>']
let g:ycm_key_list_previous_completion = ['<C-p>', '<Up>']
let g:SuperTabDefaultCompletionType = '<C-n>'

" better key bindings for UltiSnipsExpandTrigger
let g:UltiSnipsExpandTrigger = "<tab>"
let g:UltiSnipsJumpForwardTrigger = "<tab>"
let g:UltiSnipsJumpBackwardTrigger = "<s-tab>"

"" Clean search (highlight)
nnoremap <silent> <leader><space> :noh<cr>

"" Vmap for maintain Visual Mode after shifting > and <
vmap < <gv
vmap > >gv

" open vertical windows
nnoremap <leader>w <C-w>v<C-w>l

" enable pasting mode
noremap <F1> :set paste<CR>
noremap <F2> :set nopaste<CR>

" let g:vim_arduino_auto_open_serial = 1
noremap <F6> :!ino serial<CR>

noremap <F9> :Isort<CR>

" Set scripts to be executable from the shell
" au BufWritePost * if getline(1) =~ "^#!" | if getline(1) =~ "/bin/" | silent !chmod +x <afile> | endif | endif

" resize current buffer by +/- 10
nnoremap <leader><Left> :vertical resize -10<cr>
nnoremap <leader><Down> :resize +10<cr>
nnoremap <leader><Up> :resize -10<cr>
nnoremap <leader><Right> :vertical resize +10<cr>

" clear whitespaces on save
autocmd BufEnter * EnableStripWhitespaceOnSave
noremap <F8> :StripWhitespace<CR>

set colorcolumn=80
let g:vimwiki_list = [{'path': '~/vimwiki/', 'syntax': 'markdown', 'ext': '.md'}]

" let g:UltiSnipsExpandTrigger="<C-j>"
" let g:UltiSnipsJumpForwardTrigger="<C-j>"
" let g:UltiSnipsJumpBackwardTrigger="<C-k>"

" Function to activate a virtualenv in the embedded interpreter for
" omnicomplete and other things like that.
function LoadVirtualEnv(path)
    let activate_this = a:path . '/bin/activate_this.py'
    if getftype(a:path) == "dir" && filereadable(activate_this)
python << EOF
import vim
activate_this = vim.eval('l:activate_this')
execfile(activate_this, dict(__file__=activate_this))
EOF
    endif
endfunction

autocmd BufWritePost *.py call flake8#Flake8()

:nmap <ScrollWheelUp> <nop>
:nmap <S-ScrollWheelUp> <nop>
:nmap <C-ScrollWheelUp> <nop>
:nmap <ScrollWheelDown> <nop>
:nmap <S-ScrollWheelDown> <nop>
:nmap <C-ScrollWheelDown> <nop>
:nmap <ScrollWheelLeft> <nop>
:nmap <S-ScrollWheelLeft> <nop>
:nmap <C-ScrollWheelLeft> <nop>
:nmap <ScrollWheelRight> <nop>
:nmap <S-ScrollWheelRight> <nop>
:nmap <C-ScrollWheelRight> <nop>

" %! TEX program = xelatex
" %! TEX parameter = -shell-escape
