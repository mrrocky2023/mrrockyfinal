// Copyright (c) 2022, Jorge Devia and contributors
// For license information, please see license.txt

frappe.ui.form.on('VTigerCRM Field', {
	helpdesk: function(frm) {
		frappe.model.with_doctype('Issue', function() {
			var options = $.map(frappe.get_meta('Issue').fields,
				function(d) {
					if(d.fieldname && frappe.model.no_value_type.indexOf(d.fieldtype)===-1) {
						return d.label + '(' + (d.fieldname)  + ')';
					}
					return null;
				}
			)
			frappe.meta.get_docfield("VTigerCRM HelpDesk", "erpnext_issue", frm.docname).options = options.join("\n");
		});
		return frappe.call({
			method: "get_fields",
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
			var options = $.map(frappe.get_meta('Contact').fields,
				function(d) {
					if(d.fieldname && frappe.model.no_value_type.indexOf(d.fieldtype)===-1) {
						console.log(d);
						return d.label + '(' + (d.fieldname)  + ')';
					}
					return null;
				}
			)
			frappe.meta.get_docfield("VTigerCRM Contact", "erpnext_contact", frm.docname).options = options.join("\n");
		});
		return frappe.call({
			method: "get_fields",
			args: {module:'Contacts'},
			doc: cur_frm.doc,
			callback: function(data) {
				if(data.message) {
					let options = data.message;
					frappe.meta.get_docfield("VTigerCRM Contact", "vtigercrm_contact", frm.docname).options = options.join("\n");
				}
			}
		});
	},
	salesorder: function(frm) {
		frappe.model.with_doctype('Sales Order', function() {
			var options = $.map(frappe.get_meta('Sales Order').fields,
				function(d) {
					if(d.fieldname && frappe.model.no_value_type.indexOf(d.fieldtype)===-1) {
						return d.label + '(' + (d.fieldname)  + ')';
					}
					return null;
				}
			)
			console.log(options.join("\n"));
			frappe.meta.get_docfield("VTigerCRM SalesOrder", "erpnext_sales_order", frm.docname).options = options.join("\n");
		});
		return frappe.call({
			method: "get_fields",
			args: {module:'SalesOrder'},
			doc: cur_frm.doc,
			callback: function(data) {
				if(data.message) {
					let options = data.message;
					frappe.meta.get_docfield("VTigerCRM SalesOrder", "vtigercrm_salesorder", frm.docname).options = options.join("\n");
				}
			}
		});
	},
});
