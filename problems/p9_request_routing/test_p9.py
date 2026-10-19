import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pytest
import solution_p9 as sol


CASES = [
    ("source_registration", [
        "REGISTER us-west 38 -122 100", "REGISTER us-east 41 -74 150",
        "REGISTER us-west 50 -100 50", "REGISTER invalid-node 91 0 100",
        "REGISTER invalid-cap 0 0 0", "SET_HEALTHY us-east false",
        "SET_HEALTHY fake-node true",
    ], ["OK", "OK", "ERROR", "ERROR", "ERROR", "OK", "ERROR"]),
    ("source_distances", ["DISTANCE 38 -122 41 -74", "DISTANCE 0 0 0 0", "DISTANCE 91 0 0 0"],
     ["4080", "0", "ERROR"]),
    ("source_routing", [
        "REGISTER node-A 0 0 1", "REGISTER node-B 0 0 1", "REGISTER node-C 10 10 100",
        "SET_HEALTHY node-C false", "ROUTE 0 0", "ROUTE 0 0", "ROUTE 0 0",
    ], ["OK", "OK", "OK", "OK", "node-A 0 node-A,node-B", "node-B 0 node-A,node-B", "None node-A,node-B"]),
    ("coordinate_boundaries", ["REGISTER north 90 180 1", "REGISTER south -90 -180 1"], ["OK", "OK"]),
    ("invalid_registration", [
        "REGISTER a -91 0 1", "REGISTER b 0 181 1", "REGISTER c 0 -181 1",
        "REGISTER d 0 0 0", "REGISTER e 0 0 -1", "ROUTE 0 0",
    ], ["ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "None"]),
    ("duplicate_keeps_load_and_coordinates", [
        "REGISTER a 0 0 1", "ROUTE 0 0", "REGISTER a 20 20 100", "ROUTE 0 0",
    ], ["OK", "a 0 a", "ERROR", "None a"]),
    ("duplicate_keeps_health", [
        "REGISTER a 0 0 1", "SET_HEALTHY a false", "REGISTER a 0 0 100", "ROUTE 0 0",
    ], ["OK", "OK", "ERROR", "None"]),
    ("health_case_insensitive", [
        "REGISTER a 0 0 1", "SET_HEALTHY a FaLsE", "ROUTE 0 0",
        "SET_HEALTHY a TRUE", "ROUTE 0 0",
    ], ["OK", "OK", "None", "OK", "a 0 a"]),
    ("invalid_health_preserves_state", [
        "REGISTER a 0 0 1", "SET_HEALTHY a maybe", "SET_HEALTHY missing true", "ROUTE 0 0",
    ], ["OK", "ERROR", "ERROR", "a 0 a"]),
    ("health_toggle_preserves_load", [
        "REGISTER a 0 0 1", "ROUTE 0 0", "SET_HEALTHY a false", "ROUTE 0 0",
        "SET_HEALTHY a true", "ROUTE 0 0",
    ], ["OK", "a 0 a", "OK", "None", "OK", "None a"]),
    ("no_centers", ["ROUTE 0 0", "ROUTE 90 -180"], ["None", "None"]),
    ("capacity_fallback_keeps_full_candidates", [
        "REGISTER near 0 0 1", "REGISTER far 0 1 1", "ROUTE 0 0", "ROUTE 0 0", "ROUTE 0 0",
    ], ["OK", "OK", "near 0 near,far", "far 111 near,far", "None near,far"]),
    ("distance_before_name", [
        "REGISTER alpha 0 1 1", "REGISTER zulu 0 0 1", "ROUTE 0 0",
    ], ["OK", "OK", "zulu 0 zulu,alpha"]),
    ("exact_tie_before_registration_order", [
        "REGISTER z 0 1 1", "REGISTER a 0 1 1", "ROUTE 0 0", "ROUTE 0 0",
    ], ["OK", "OK", "a 111 a,z", "z 111 a,z"]),
    ("unrounded_order", [
        "REGISTER alpha 0 0.002 1", "REGISTER zulu 0 0.001 1", "ROUTE 0 0",
    ], ["OK", "OK", "zulu 0 zulu,alpha"]),
    ("unhealthy_nearest_excluded", [
        "REGISTER near 0 0 1", "REGISTER far 0 1 1", "SET_HEALTHY near false", "ROUTE 0 0",
    ], ["OK", "OK", "OK", "far 111 far"]),
    ("invalid_distance_coordinates", [
        "DISTANCE -91 0 0 0", "DISTANCE 0 181 0 0",
        "DISTANCE 0 0 91 0", "DISTANCE 0 0 0 -181",
    ], ["ERROR", "ERROR", "ERROR", "ERROR"]),
    ("distance_geometry", [
        "DISTANCE 0 0 0 1", "DISTANCE 0 179 0 -179", "DISTANCE 0 0 0 180", "DISTANCE 0 0 0 0.001",
    ], ["111", "222", "20015", "0"]),
    ("distance_does_not_change_load", [
        "REGISTER a 0 0 1", "DISTANCE 0 0 0 1", "ROUTE 0 0",
    ], ["OK", "111", "a 0 a"]),
    ("invalid_route_preserves_capacity", [
        "REGISTER a 0 0 1", "ROUTE 91 0", "ROUTE 0 181", "ROUTE 0 0",
    ], ["OK", "ERROR", "ERROR", "a 0 a"]),
    ("unknown_command", ["UNKNOWN", "ROUTE 0 0"], ["ERROR", "None"]),
    ("whitespace", ["", "  REGISTER   a  0 0 1  ", "  ", "ROUTE 0 0", ""], ["OK", "a 0 a"]),
    ("empty", [], []),
]


@pytest.mark.parametrize("name,commands,expected", CASES, ids=[case[0] for case in CASES])
def test_routing(name, commands, expected):
    assert sol.solveRequestRoutingSystem("\n".join(commands)) == expected


def test_calls_have_independent_state():
    assert sol.solveRequestRoutingSystem("REGISTER a 0 0 1\nROUTE 0 0") == ["OK", "a 0 a"]
    assert sol.solveRequestRoutingSystem("ROUTE 0 0") == ["None"]
