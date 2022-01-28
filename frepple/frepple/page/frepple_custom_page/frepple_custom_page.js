frappe.pages['frepple-custom-page'].on_page_load = (wrapper) => {
	// init page
	const page = frappe.ui.make_app_page({
		'parent': wrapper,
		'title': 'Frepple Custom Page',
		'single_column': true,
	});

	new FreppleCustomPage(page, wrapper);
};

class FreppleCustomPage {
	constructor(page, wrapper) {
		this.currentPage = false;
		this.wrapper = wrapper;
		this.pageMain = $(page.main);
		this.pageAction = (
			$(this.wrapper)
				.find('div.page-head div.page-actions')
		);
		this.pageTitle = $(this.wrapper).find('div.title-text');

		this.init();
	}

	init() {
		this.createSelectionField();
	}

	showIframe() {
		this.getSettings().then(
			(r) => {
				// console.log(r.message);
				this.URL = r.message.URL;
				this.iframeHeight = r.message.iframeHeight;

				if (this.URL) {					
					// prepare html
					const iFrameHtml = `
						<iframe
							src=${this.URL}
							width="100%"
							height=${this.iframeHeight}
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
			'method': 'frepple.frepple.doctype.frepple_custom_page_settings.frepple_custom_page_settings.get_iframe_url',
			'args': {
				'pageName': this.pageName,
			},
		});
	}

	createSelectionField() {
		// create page selection field
		this.selectionField = frappe.ui.form.make_control({
			'parent': this.pageAction,
			'df': {
				'fieldname': 'Page',
				'fieldtype': 'Link',
				'options': 'Frepple Custom Page Settings',
				'onchange': () => {
					const pageName = this.selectionField.get_value();
					// console.log(pageName);
					if (pageName) {
						this.pageName = pageName;
						if (this.currentPage != this.pageName) {
							// clear page html
							this.pageMain.empty();

							this.showIframe();
							this.changeTitle();

							// set current dashboard
							this.currentPage = this.pageName;
						}
						// clear input
						this.selectionField.set_input('');
					}
				},
				// 'get_query': () => {
				// 	return {
				// 		'filters': {
				// 			'is_active': 1,
				// 		},
				// 	};
				// },
				'placeholder': 'Select Page',
			},
			'render_input': true,
		});

		// change css
		this.pageAction.removeClass('page-actions');
		this.selectionField.$wrapper.css('text-align', 'left');
	}

	changeTitle() {
		this.pageTitle.text(`${this.pageName}`);
	}
}
