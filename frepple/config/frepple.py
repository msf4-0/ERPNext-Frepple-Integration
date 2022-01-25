from __future__ import unicode_literals
from frappe import _

def get_data():
    config = [
        {
            "label": _("Frepple Data"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Item Frepple",
                    "onboard": 1,
                },
                # {
                #     "type": "page",
                #     "name": "barcode-scanner",
                #     "label": "Barcode Scanner",
                #     "onboard": 1,
                # },
            ]
        },
        {
            "label": _("Settings"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Setting",
                    "label": "Frepple Setting",
                    "onboard": 1,
                },
            ]
        }
    ]
    return config