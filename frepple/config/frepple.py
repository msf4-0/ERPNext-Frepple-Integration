from __future__ import unicode_literals
from frappe import _

def get_data():
    config = [
        {
            "label": _("Frepple Data"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Item",
                    "label": "Frepple Item",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Customer",
                    "label": "Frepple Customer",
                    "onboard": 2,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Supplier",
                    "label": "Frepple Supplier",
                    "onboard": 3,
                },

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
        },
        {
            "label": _("Frepple Result"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Sales Order",
                    "label": "Frepple Sales Order",
                    "onboard": 1,
                },
                # {
                #     "type": "doctype",
                #     "name": "Frepple Manufacturing Order",
                #     "label": "Frepple Manufacturing Order",
                #     "onboard": 2,
                # },
            ]
        }
    ]
    return config