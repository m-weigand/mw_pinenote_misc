/*
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 *
 * Based on:
 * https://raw.githubusercontent.com/kosmospredanie/gnome-shell-extension-screen-autorotate/main/screen-autorotate%40kosmospredanie.yandex.ru/extension.js
 */
'use strict';
const St = imports.gi.St;
// const Gio = imports.gi.Gio;
const { GLib, Gio } = imports.gi;

const ExtensionUtils = imports.misc.extensionUtils;
const Me = ExtensionUtils.getCurrentExtension();
// const rotator = Me.imports.rotator;
const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const Slider = imports.ui.slider;

const Orientation = Object.freeze({
    'normal': 0,
    'left-up': 1,
    'bottom-up': 2,
    'right-up': 3
});

// imports.searchPath.unshift('.');
const BusUtils = Me.imports.busUtils;

// function call_dbus_method(method, params = null) {
// 	log("pre get sync");
//     let connection = Gio.bus_get_sync(Gio.BusType.SESSION, null);
// 	log("post get sync");
//     return connection.call_sync(
//         'org.gnome.Mutter.DisplayConfig',
//         '/org/gnome/Mutter/DisplayConfig',
//         'org.gnome.Mutter.DisplayConfig',
//         method,
//         params,
//         null,
//         Gio.DBusCallFlags.NONE,
//         -1,
//         null);
// }

// function get_state() {
//     let result = call_dbus_method('GetCurrentState');
//     return new BusUtils.DisplayConfigState(result);
// }

// function rotate_to(transform) {
//     let state = this.get_state();
//     let builtin_monitor = state.builtin_monitor;
//     let logical_monitor = state.get_logical_monitor_for(builtin_monitor.connector);
//     logical_monitor.transform = transform;
//     let variant = state.pack_to_apply( BusUtils.Methods['temporary'] );
//     call_dbus_method('ApplyMonitorsConfig', variant);
// }


class Extension {
    constructor() {
        this._indicator = null;
        this._indicator2 = null;
    }

	_write_to_sysfs_file(filename, value){
		try {
			// The process starts running immediately after this function is called. Any
			// error thrown here will be a result of the process failing to start, not
			// the success or failure of the process itself.
			let proc = Gio.Subprocess.new(
				// The program and command options are passed as a list of arguments
				['/bin/sh', '-c', `echo ${value} > ` + filename],
					// /sys/module/drm/parameters/debug'],

				// The flags control what I/O pipes are opened and how they are directed
				Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE
			);

			// Once the process has started, you can end it with `force_exit()`
			// proc.force_exit();
		} catch (e) {
			logError(e);
		}
	}

	_add_bw_slider() {
        this.m_bw_slider = new PopupMenu.PopupBaseMenuItem({ activate: true });
		this._indicator.menu.addMenuItem(this.m_bw_slider);

        this._bw_slider = new Slider.Slider(0.5);
        this._sliderChangedId = this._bw_slider.connect('notify::value',
            this._bw_slider_changed.bind(this));
        this._bw_slider.accessible_name = _("BW Threshold");

        const icon = new St.Icon({
            icon_name: 'display-brightness-symbolic',
            style_class: 'popup-menu-icon',
        });
        this.m_bw_slider.add(icon);
        this.m_bw_slider.add_child(this._bw_slider);
        this.m_bw_slider.connect('button-press-event', (actor, event) => {
            return this._bw_slider.startDragging(event);
        });
        this.m_bw_slider.connect('key-press-event', (actor, event) => {
            return this._bw_slider.emit('key-press-event', event);
        });
        this.m_bw_slider.connect('scroll-event', (actor, event) => {
            return this._bw_slider.emit('scroll-event', event);
        });
	}

	_bw_slider_changed(){
		let bw_threshold;
		// transform to thresholds 1 to 7 in roughly similar-sized bins
		bw_threshold = 4 + Math.floor(this._bw_slider.value * 9);
		log(`new bw threshold: ${bw_threshold}`);
		this._write_to_sysfs_file(
			'/sys/module/rockchip_ebc/parameters/bw_threshold',
			bw_threshold
		);
	}

    enable() {
        log(`enabling ${Me.metadata.name}`);

		// ////////////////////////////////////////////////////////////////////
		// Button 1
        let indicatorName = `${Me.metadata.name} Indicator`;

        // Create a panel button
        this._indicator = new PanelMenu.Button(0.0, indicatorName, false);

        // Add an icon
        let icon = new St.Icon({
            gicon: new Gio.ThemedIcon({name: 'face-laugh-symbolic'}),
            style_class: 'system-status-icon'
        });
        this._indicator.add_child(icon);

        // `Main.panel` is the actual panel you see at the top of the screen,
        // not a class constructor.
        Main.panel.addToStatusArea(indicatorName, this._indicator);

		let item;
		item = new PopupMenu.PopupMenuItem(_('Rotate'));
		item.connect('activate', () => {
			this.rotate_screen();
		});
		this._indicator.menu.addMenuItem(item);

		this.mitem_bw_mode = new PopupMenu.PopupMenuItem(_('Black & White'));
		this.mitem_bw_mode.connect('activate', () => {
			this.toggle_bw();
		});

		this._indicator.menu.addMenuItem(this.mitem_bw_mode);

		this._add_bw_slider();

		// ////////////////////////////////////////////////////////////////////
        // let indicatorName2 = `${Me.metadata.name} Indicator2`;
		// this._indicator2 = new PanelMenu.Button(0.0, indicatorName2, false);
        // let icon2 = new St.Icon({
        //     gicon: new Gio.ThemedIcon({name: 'face-laugh-symbolic'}),
        //     style_class: 'system-status-icon'
        // });
        // this._indicator2.add_child(icon2);
		// this._indicator2.connect('open-state-changed', () => {
		// 	log('The button was clicked!');
		// });

        // Main.panel.addToStatusArea(indicatorName2, this._indicator2);

    }

	toggle_bw(){
		log("BW BW BW\n");
		// this._write_to_sysfs_file(
		// 	'/sys/module/drm/parameters/debug',
		// 	1
		// )

		let filename = '/sys/module/rockchip_ebc/parameters/bw_mode'
		// read current value
		const file = Gio.File.new_for_path(filename);
		const [, contents, etag] = file.load_contents(null);
		const ByteArray = imports.byteArray;
		const contentsString = ByteArray.toString(contents);
		log(`Result: ${contents}`);
		log(`orig: ${contents}`);
		let new_value;
		let new_wf;
		if(contentsString[0] == 'N'){
			log('toggling black and white mode');
			// fast mode
			new_value = 1;
			new_wf = 1;
			this.mitem_bw_mode.label.set_text('Grayscale Mode');
		}
		else{
			log('toggling back to standard mode');
			// standard mode
			new_value = 0;
			new_wf = 4;
			this.mitem_bw_mode.label.set_text('Black & White');
		}

		let wf_file;
		wf_file = '/sys/module/rockchip_ebc/parameters/default_waveform';

		// todo: use async functions
		try {
			// The process starts running immediately after this function is called. Any
			// error thrown here will be a result of the process failing to start, not
			// the success or failure of the process itself.
			let proc = Gio.Subprocess.new(
				// The program and command options are passed as a list of arguments
				['/bin/sh', '-c', `echo ${new_value} > ` + filename],
					// /sys/module/drm/parameters/debug'],

				// The flags control what I/O pipes are opened and how they are directed
				Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE
			);

			// Once the process has started, you can end it with `force_exit()`
			// proc.force_exit();
		} catch (e) {
			logError(e);
		}
		try {
			// The process starts running immediately after this function is called. Any
			// error thrown here will be a result of the process failing to start, not
			// the success or failure of the process itself.
			let proc = Gio.Subprocess.new(
				// The program and command options are passed as a list of arguments
				['/bin/sh', '-c', `echo ${new_wf} > ` + wf_file],
					// /sys/module/drm/parameters/debug'],

				// The flags control what I/O pipes are opened and how they are directed
				Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE
			);

			// Once the process has started, you can end it with `force_exit()`
			// proc.force_exit();
		} catch (e) {
			logError(e);
		}
	}

    // REMINDER: It's required for extensions to clean up after themselves when
    // they are disabled. This is required for approval during review!
    disable() {
        log(`disabling ${Me.metadata.name}`);

        this._indicator.destroy();
        this._indicator = null;
    }

	rotate_screen(){
		log('rotate_screen start');
    	// let state = get_state();
    	// let logical_monitor = state.get_logical_monitor_for(builtin_monitor.connector);
		// log(logical_monitor.transform);
		this.rotate_to("left-up");

	}

	rotate_to(orientation) {
        log('Rotate screen to ' + orientation);
        let target = Orientation[orientation];
        try {
            GLib.spawn_async(
                Me.path,
                ['gjs', `${Me.path}/rotator.js`, `${target}`],
                null,
                GLib.SpawnFlags.SEARCH_PATH,
                null);
        } catch (err) {
            logError(err);
        }
    }
}


function init() {
    log(`initializing ${Me.metadata.name}`);

    return new Extension();
}
