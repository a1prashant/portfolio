# Clean Code Notes

## Naming

### Reveal Intentions

| Bad | Good|
| --- | --- |
| `int d;` | `int days;` |
| `int a;` | `int age;` |
| `List<int> list;` | `List<int> listOfFilenames;` |
| `return 4;` | `return ErrorCode.INVALID;` |

### Avoid Misinformation

| Bad | Good|
| --- | --- |
| `String accountList;` | `String csvAccounts;` |
| `copy(char[] a1, char[] a2);` | `copy(char[] src, char[] dest);` |


### Meaningful distinction

| Bad | Good|
| --- | --- |
| `ProductInfo`, `ProductData` | to get the distinction between the two and name them specifically as per their purpose; instead of using the synonymous names. |


### Use 'Pronounceable' names

| Bad | Good|
| --- | --- |
| `class DtaRcrd` | `class DataRecord` |
| `Date genymdhms`| `Date generationTimestamp`|

---

### Searchable names

| Bad | Good|
| --- | --- |
| `s += t[j]` | `sum += hours;` |


### Avoid Encoding

| Bad | Good|
| --- | --- |
| `iDays` | `days` |
| `m_time` | `time` |
| `IShape` | `Shape` |
| `CShape` | `ShapeImpl` |


### One word per concept

| Bad | Good|
| --- | --- |
| `fetch, retrieve, get` | `get` |
| `controller, manager, driver` | `controller` |
| `DeviceManager, ProtocolController` | `DeviceManager, ProtocolManager` |

