var keystone = require('keystone'),
    Types = keystone.Field.Types;

/**
 * User Model
 * ==========
 */
var Raspberry = new keystone.List('Raspberry');

Raspberry.add({
    internal_ip: { type: String, required: true, index: true, label: 'Internal IP', initial: true },
    external_ip: { type: String, required: true, index: true, label: 'External IP', initial: true },
    hash: { type: String, index: true, initial: true },
    username: { type: String, initial: true, required: true, index: true },
    password: { type: Types.Password, required: true, initial: true },
    status: {
        online: { type: Boolean, label: 'Rpi Online', index: true},
        last_online_at: { type: Date, label: 'Last Online At'}
    },
    created_at: { type: Date, default: Date.now }
});

// Provide access to Keystone
// User.schema.virtual('canAccessKeystone').get(function () {
    // return this.isAdmin;
// });


/**
 * Registration
 */
Raspberry.defaultColumns = 'online, username, hash|20%, external_ip, internal_ip, password, created_at|15%';
Raspberry.register();
