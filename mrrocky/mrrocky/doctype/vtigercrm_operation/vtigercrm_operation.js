// Copyright (c) 2022, l and contributors
// For license information, please see license.txt

frappe.ui.form.on('VTigerCRM Operation', {
    refresh: function(frm) {
        frm.set_df_property('ibsn', 'read_only', !frm.is_new());
        frappe.msgprint({
            title: __('Notification'),
            message: __('Are you sure you want to proceed?'),
            primary_action:{
                action(values) {
                    new frappe.ui.form.MultiSelectDialog({
                        doctype: "Contact",
                        target: this.cur_frm,
                        setters: {
                            first_name: 'NORY',
                            last_name: 'ZAMORA'
                        },
                        add_filters_group: 0,
                        date_field: "contact_date",
                        get_query() {
                            return {
                                filters: { docstatus: ['!=', 2] }
                            }
                        },
                        action(selections) {
                            console.log(selections);
                        }
                    });
                }
            }
        });
        frappe.show_progress('Loading..', 70, 100, 'Please wait');
    }
});