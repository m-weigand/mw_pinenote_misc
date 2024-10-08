
* Create file::

		root@pinenote:~# cat /etc/dconf/profile/user
		user-db:user
		system-db:local

* Default gnome settings::

		root@pinenote:~# cat /etc/dconf/db/local.d/01-pinenote-settings
		[org/gnome/desktop/a11y/applications]
		screen-keyboard-enabled=true

		[org/gnome/desktop/a11y/interface]
		high-contrast=true

		[org/gnome/desktop/a11y/keyboard]
		mousekeys-enable=false
		stickykeys-enable=true

		[org/gnome/desktop/interface]
		clock-show-weekday=false
		cursor-blink=false
		cursor-size=24
		cursor-theme='breeze_cursors'
		enable-animations=false
		font-antialiasing='grayscale'
		font-hinting='slight'
		font-name='Noto Sans 11'
		gtk-theme='Breeze'
		icon-theme='breeze'
		show-battery-percentage=true
		toolbar-style='text'
		toolkit-accessibility=true

		[org/gnome/desktop/search-providers]
		disable-external=false
		disabled=['org.gnome.Contacts.desktop', 'org.gnome.Documents.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.Calendar.desktop', 'org.gnome.Software.desktop', 'org.gnome.seahorse.Application.desktop', 'org.gnome.clocks.desktop', 'org.gnome.Terminal.desktop', 'org.gnome.Calculator.desktop', 'org.gnome.Characters.desktop']
		sort-order=['org.gnome.Contacts.desktop', 'org.gnome.Documents.desktop', 'org.gnome.Nautilus.desktop']

		[org/gnome/desktop/wm/preferences]
		action-double-click-titlebar='menu'
		button-layout='icon:minimize,maximize,close'
		theme='HighContrast'
		visual-bell=false

		[org/gnome/shell]
		enabled-extensions=['pnhelper@m-weigand.github.com']

		favorite-apps=['org.gnome.Terminal.desktop', 'org.gnome.Nautilus.desktop', 'firefox.desktop', 'com.github.johnfactotum.Foliate.desktop', 'org.gnome.Geary.desktop', 'com.github.xournalpp.xournalpp.desktop', 'libreoffice-writer.desktop', 'org.kde.okular.desktop']


		[org/gnome/mutter]
		auto-maximize=true
		center-new-windows=true

		[org/gnome/nautilus/preferences]
		click-policy='single'
		default-folder-viewer='icon-view'
		search-filter-time-type='last_modified'
		search-view='list-view'

		[org/gnome/settings-daemon/peripherals/touchscreen]
		orientation-lock=true

* dconf update

* Copy pnhelper extension to

 		/usr/share/gnome-shell/extensions/pnhelper@m-weigand.github.com/

* /etc/lightdm/lightdm.conf::

		[Seat:*]
		autologin-guest = false
		autologin-user = test3
		autologin-user-timeout=0
		autologin-session=gnome-wayland

