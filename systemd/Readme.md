The panfrost gpu should be triggered once on boot to prevent it from shutting down.

This systemd unit runs eglinfo once to do exactly that.

## Installation

* Copy to

	/etc/systemd/system/

* Reload systemd unit files

 	sudo systemctl daemon-reload

* Activate the unit

	sudo systemctl enable mweigand_eglinfo.service

