# Problem 9 — Request Routing System

**Suggested time:** 60 minutes · **One function**

Adapted from [FastPrep's Request Routing System](https://www.fastprep.io/problems/stripe-request-routing-system),
a public practice reconstruction, not an official Stripe statement. Implement
`solveRequestRoutingSystem(input_text: str) -> List[str]`: process newline-separated
commands sequentially and return one output string per command.

## Commands

| Command | Behavior |
|---|---|
| `REGISTER name lat lon capacity` | Add a unique datacenter, initially healthy with zero load. Valid latitude: −90 through 90; longitude: −180 through 180; capacity: positive integer. Return `OK`, otherwise `ERROR`. |
| `SET_HEALTHY name value` | Update an existing center using case-insensitive `true`/`false`. Return `OK`, otherwise `ERROR`. |
| `DISTANCE lat1 lon1 lat2 lon2` | Return great-circle kilometers rounded to an integer; invalid coordinates return `ERROR`. Use Earth radius 6371 km. |
| `ROUTE lat lon` | Rank every healthy center by unrounded distance, then name for exact ties. Select the first with available capacity and increment its load. |

For routing, `candidates` is the comma-joined ranking, including full healthy centers.
Success returns `name rounded-distance candidates`; exhausted capacity returns
`None candidates`; no healthy centers returns exactly `None`. Use single spaces
between fields, without trailing spaces. There is no disconnect command.

## Distance definition

Use the Haversine formula. With coordinates in radians:

```text
a = sin²((lat2-lat1)/2) + cos(lat1) * cos(lat2) * sin²((lon2-lon1)/2)
distance = 2 * 6371 * asin(sqrt(a))
```

Clamp `a` to `[0, 1]` to protect against floating-point drift near antipodal points.
Only display distances rounded; use unrounded values for ordering.

## Examples

```python
input_text = """REGISTER us-west 38 -122 100
REGISTER us-east 41 -74 150
REGISTER us-west 50 -100 50
REGISTER invalid-node 91 0 100
REGISTER invalid-cap 0 0 0
SET_HEALTHY us-east false
SET_HEALTHY fake-node true"""
# ["OK", "OK", "ERROR", "ERROR", "ERROR", "OK", "ERROR"]
```

```python
input_text = """DISTANCE 38 -122 41 -74
DISTANCE 0 0 0 0
DISTANCE 91 0 0 0"""
# ["4080", "0", "ERROR"]
```

```python
input_text = """REGISTER node-A 0 0 1
REGISTER node-B 0 0 1
REGISTER node-C 10 10 100
SET_HEALTHY node-C false
ROUTE 0 0
ROUTE 0 0
ROUTE 0 0"""
# ["OK", "OK", "OK", "OK", "node-A 0 node-A,node-B",
#  "node-B 0 node-A,node-B", "None node-A,node-B"]
```

## Local practice clarifications

These choices fill gaps in the public statement:

- Recognized commands have the documented number of arguments. Coordinates are
  finite numbers; capacities parse as integers; names are nonempty ASCII tokens
  without whitespace. Command names are case-sensitive.
- Unknown commands and out-of-range `ROUTE` coordinates return `ERROR`.
- Rejected commands leave state unchanged, including duplicate registrations and
  invalid health values. Health changes preserve load; failed routes consume no capacity.
- Round nonnegative displayed kilometers to the nearest integer, with halves up.
- Ignore blank lines and accept whitespace between arguments. Empty input returns
  `[]`. Each function call starts with an empty registry.

Start: `uv run python practice.py p9`

Grade: `uv run python practice.py p9 --test`

Manual stdin: `uv run python problems/p9_request_routing/solution_p9.py < input.txt`

Implement the single function in `problems/p9_request_routing/solution_p9.py`.
No reference solution is included.
