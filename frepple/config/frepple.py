from __future__ import unicode_literals
from frappe import _

def get_data():
    config = [
        {
            "label": _("Frepple Sales"),
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
                    "name": "Frepple Location",
                    "label": "Frepple Location",
                    "onboard": 3,
                },

            ]
        },
        {
            "label": _("Frepple Inventory"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Buffer",
                    "label": "Frepple Buffer",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Item Distribution",
                    "label": "Frepple Item Distribution",
                    "onboard": 2,
                },
                # {
                #     "type": "doctype",
                #     "name": "Frepple Supplier",
                #     "label": "Frepple Supplier",
                #     "onboard": 3,
                # },

            ]
        },
        {
            "label": _("Frepple Capacity"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Resource",
                    "label": "Frepple Resource",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Skill",
                    "label": "Frepple Skill",
                    "onboard": 2,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Resource Skill",
                    "label": "Frepple Resource Skill",
                    "onboard": 3,
                },
            ]
        },
        {
            "label": _("Frepple Purchasing"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Supplier",
                    "label": "Frepple Supplier",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Item Supplier",
                    "label": "Frepple Item Supplier",
                    "onboard": 2,
                },
            ]
        },
        {
            "label": _("Frepple Manufacturing"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Operation",
                    "label": "Frepple Operation",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Operation Material",
                    "label": "Frepple Operation Material",
                    "onboard": 2,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Operation Resource",
                    "label": "Frepple Operation Resource",
                    "onboard": 3,
                },
            ]
        },
        {
            "label": _("Additional Data"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Frepple Calendar",
                    "label": "Frepple Calendar",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Calendar Bucket",
                    "label": "Frepple Calendar Bucket",
                    "onboard": 2,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Resource Skill",
                    "label": "Frepple Resource Skill",
                    "onboard": 3,
                },
                {
                    "type": "doctype",
                    "name": "Frepple Item Distribution",
                    "label": "Frepple Item Distribution",
                    "onboard": 4,
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

    ]
    return config