/*
 * https://raw.githubusercontent.com/kosmospredanie/gnome-shell-extension-screen-autorotate/main/screen-autorotate%40kosmospredanie.yandex.ru/rotator.js
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
    }

    enable() {
        log(`enabling ${Me.metadata.name}`);

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
