// Copyright (c) 2022, Jorge Devia and contributors
// For license information, please see license.txt

frappe.ui.form.on('VTigerCRM Field', {
	helpdesk: function(frm) {
		frappe.model.with_doctype('ToDo', function() {
			var options = $.map(frappe.get_meta('ToDo').fields,
				function(d) {
					console.log(d);
					if(d.fieldname && frappe.model.no_value_type.indexOf(d.fieldtype)===-1) {
						return d.label;
					}
					return null;
				}
			)
			frappe.meta.get_docfield("VTigerCRM HelpDesk", "erpnext_issue", frm.docname).options = options.join("\n");
		});
		return frappe.call({
			method: "getFields",
			args: {module:'HelpDesk'},
			doc: cur_frm.doc,
			callback: function(data) {
				if(data.message) {
					let options = data.message;
					frappe.meta.get_docfield("VTigerCRM HelpDesk", "vtigercrm_helpdesk", frm.docname).options = options.join("\n");
				}
			}
		});
	},
	contacts: function(frm) {
		frappe.model.with_doctype('Contact', function() {
			var options = $.map(frappe.get_meta('Issue').fields,
				function(d) {
					console.log(d);
					if(d.fieldname && frappe.model.no_value_type.indexOf(d.fieldtype)===-1) {
						return d.label;
					}
					return null;
				}
			)
			frappe.meta.get_docfield("VTigerCRM HelpDesk", "erpnext_issue", frm.docname).options = options.join("\n");
		});
		return frappe.call({
			method: "getFields",
			doc: cur_frm.doc,
			callback: function(data) {
				if(data.message) {
					let options = data.message;
					frappe.meta.get_docfield("VTigerCRM HelpDesk", "vtigercrm_helpdesk", frm.docname).options = options.join("\n");
				}
			}
		});
	},
	salesorder: function(frm) {
		frappe.model.with_doctype('SalesOrder', function() {
			var options = $.map(frappe.get_meta('SalesOrder').fields,
				function(d) {
					console.log(d);
					if(d.fieldname && frappe.model.no_value_type.indexOf(d.fieldtype)===-1) {
						return d.label;
					}
					return null;
				}
			)
			frappe.meta.get_docfield("VTigerCRM HelpDesk", "erpnext_issue", frm.docname).options = options.join("\n");
		});
		return frappe.call({
			method: "getFields",
			doc: cur_frm.doc,
			callback: function(data) {
				if(data.message) {
					let options = data.message;
					frappe.meta.get_docfield("VTigerCRM HelpDesk", "vtigercrm_helpdesk", frm.docname).options = options.join("\n");
				}
			}
		});
	},
});
