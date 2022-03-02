import pytest
import sys
import os
import notifier


def test_parse_message():
    message = "Affected Bus:\n\nBus # -- 201\n\nTime -- AM & PM\n\nSchool -- OLD MILL HS\n\nSub # -- 254\n\nImpact -- LESS THAN 20 MINUTES"
    bus_num, bus_time, bus_school, bus_sub, bus_impact = notifier.parse_message(message)
    assert bus_num == "201"
    assert bus_time == "AM & PM"
    assert bus_school == "OLD MILL HS"
    assert bus_sub == "254"
    assert bus_impact == "LESS THAN 20 MINUTES"


def test_notify_users_general_no_logging_no_history(current_dir, get_request):
    configs = {"general": {"users": "resources/recipients_0.db"}}
    raw_texts, always_raw_texts, carrier_map = notifier.notify_users_map(
        get_request, current_dir, configs, logging=False
    )
    assert carrier_map == {'+18888888888': 'verizon', '+28888888888': 'verizon', '+38888888888': 'verizon', '+48888888888': 'verizon'}
    assert raw_texts == {
        "+18888888888": [
            "Affected Bus:\n\nBus # -- 202\n\nTime -- AM & PM\n\nSchool -- MEADE HS\n\nSub # -- NO SUB!\n\nImpact -- NO SERVICE"
        ],
        "+28888888888": [
            "Affected Bus:\n\nBus # -- 201\n\nTime -- AM & PM\n\nSchool -- OLD MILL HS\n\nSub # -- 202\n\nImpact -- 20 MINS LATE"
        ],
    }
    assert always_raw_texts == {
        "+18888888888": [
            "Affected Bus:\n\nBus # -- 71\n\nTime -- AM & PM\n\nSchool -- JESSUP ES\n\nSub # -- NO SUB!\n\nImpact -- NO SERVICE"
        ],
        "+38888888888": ["Bus 72 Jessup is running as scheduled."],
    }


def test_raw_text_filter_general_no_reversal(current_dir, get_request):
    configs = {
        "general": {
            "users": "resources/recipients_0.db",
            "logged_texts": "resources/previous_state_0.json",
        }
    }
    raw_texts, always_raw_texts, carrier_map = notifier.notify_users_map(
        get_request, current_dir, configs, logging=False
    )
    assert carrier_map == {'+18888888888': 'verizon', '+28888888888': 'verizon', '+38888888888': 'verizon', '+48888888888': 'verizon'}
    filtered_texts = notifier.filter_texts(raw_texts, current_dir, configs, True)
    assert filtered_texts == {
        "+18888888888": [
            "Affected Bus:\n\nBus # -- 202\n\nTime -- AM & PM\n\nSchool -- MEADE HS\n\nSub # -- NO SUB!\n\nImpact -- NO SERVICE"
        ],
        "+38888888888": [
            "Bus 72 with school(s) JESSUP ES is now running as scheduled."
        ],
    }
    assert always_raw_texts == {
        "+18888888888": [
            "Affected Bus:\n\nBus # -- 71\n\nTime -- AM & PM\n\nSchool -- JESSUP ES\n\nSub # -- NO SUB!\n\nImpact -- NO SERVICE"
        ],
        "+38888888888": ["Bus 72 Jessup is running as scheduled."],
    }
