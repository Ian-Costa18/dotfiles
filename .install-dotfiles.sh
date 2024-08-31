alias config='/usr/bin/git --git-dir=$HOME/.myconfig/ --work-tree=$HOME'
echo ".myconfig" >> $HOME/.gitignore
git clone --bare https://github.com/Ian-Costa18/dotfiles.git $HOME/.myconfig
alias config='/usr/bin/git --git-dir=$HOME/.myconfig/ --work-tree=$HOME'
config config --local status.showUntrackedFiles no
config checkout
echo "If there were errors, delete those files then rerun: config checkout"
sudo pacman -Syu alacritty fish neovim qtile rofi exa unimatrix ranger
echo "powerline-shell and vim-plug needs to be installed using the AUR"
