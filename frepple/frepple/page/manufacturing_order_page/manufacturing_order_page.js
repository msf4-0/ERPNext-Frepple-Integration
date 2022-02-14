frappe.pages['manufacturing-order-page'].on_page_load = (wrapper) => {
	const page = frappe.ui.make_app_page({
		'parent': wrapper,
		'title': 'Frepple Manufacturing Order Page',
		'single_column': true
	});
	new ManufacturingOrderPage(page, wrapper);
}

class ManufacturingOrderPage {
	constructor(page, wrapper) {
		this.currentDashboard = false;
		this.wrapper = wrapper;
		this.pageMain = $(page.main);
		this.pageTitle = $(this.wrapper).find('div.title-text');
		this.showIframe();
	}

	showIframe() {
		this.getSettings().then(
			(r) => {
				this.URL = r.message;
				if (this.URL) {					
					// prepare html
					const iFrameHtml = `
						<iframe
							src=${this.URL}
							width="100%"
							height="590"
							marginwidth="0"
							marginheight="0"
							frameborder="no"
							scrolling="yes"
						/>
					`;
					// append html to page
					this.iFrame = $(iFrameHtml).appendTo(this.pageMain);
				}
			}
		);
	}

	getSettings() {
		return frappe.call({
			'method': 'frepple.frepple.doctype.manufacturing_order_page.manufacturing_order_page.get_iframe_url'
		});
	}
}
