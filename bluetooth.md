# Pinenote bluetooth connection to Logitech K480 keyboard

	root@pinenote:~# dmesg | grep Bluetooth
	[    3.580865] Bluetooth: Core ver 2.22
	[    3.581852] Bluetooth: HCI device and connection manager initialized
	[    3.582457] Bluetooth: HCI socket layer initialized
	[    3.582915] Bluetooth: L2CAP socket layer initialized
	[    3.583418] Bluetooth: SCO socket layer initialized
	[    3.585098] Bluetooth: HIDP (Human Interface Emulation) ver 1.2
	[    3.585696] Bluetooth: HIDP socket layer initialized
	[    9.733121] Bluetooth: HCI UART driver ver 2.3
	[    9.733136] Bluetooth: HCI UART protocol H4 registered
	[    9.733438] Bluetooth: HCI UART protocol Broadcom registered
	[   10.256383] Bluetooth: hci0: BCM: chip id 107
	[   10.264081] Bluetooth: hci0: BCM: features 0x2f
	[   10.296721] Bluetooth: hci0: BCM4345C0
	[   10.302311] Bluetooth: hci0: BCM4345C0 (003.001.025) build 0000
	[   10.318376] Bluetooth: hci0: BCM4345C0 'brcm/BCM4345C0.hcd' Patch
	[   18.557907] Bluetooth: hci0: BCM43455 37.4MHz Raspberry Pi 3+-0159
	[   18.558619] Bluetooth: hci0: BCM4345C0 (003.001.025) build 0290

* Modules hidp and uhid compiled as modules
* Connect via bluetoothctl::

		root@pinenote:~# bluetoothctl
		Agent registered
		[CHG] Controller 90:C3:68:B9:CA:54 Pairable: yes
		[bluetooth]# power on
		Changing power on succeeded
		[bluetooth]# discoverable on
		Changing discoverable on succeeded
		[CHG] Controller 90:C3:68:B9:CA:54 Discoverable: yes
		[bluetooth]# pairable on
		Changing pairable on succeeded
		[bluetooth]# agent KeyboardOnly
		Agent is already registered
		[bluetooth]# default-agent
		Default agent request successful
		[bluetooth]# scan on
		Discovery started
		[CHG] Controller 90:C3:68:B9:CA:54 Discovering: yes
		[...]
		[NEW] Device F4:73:35:6B:38:D0 Keyboard K480
		[...]
		[bluetooth]# pair F4:73:47:6B:38:D0
		Attempting to pair with F4:73:47:6B:38:D0
		[agent] Passkey: 183308
		[agent] Passkey: 183308
		[agent] Passkey: 183308
		[agent] Passkey: 183308
		[agent] Passkey: 183308
		[agent] Passkey: 183308
		[agent] Passkey: 183308
		[CHG] Device F4:73:47:6B:38:D0 Paired: yes
		Pairing successful
		[Keyboard K480]# trust F4:73:47:6B:38:D0
		Changing F4:73:47:6B:38:D0 trust succeeded
		[bluetooth]# connect F4:73:47:6B:38:D0
		Attempting to connect to F4:73:47:6B:38:D0
		[CHG] Device F4:73:47:6B:38:D0 Connected: yes
		Connection successful
		[Keyboard K480]#
