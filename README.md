# python-vatsim

This module aims to provide functionality to interact with VATSIM APIs and the datafeed. In the
future, it will also include parsers for different file formats like Sectorfiles or ESE files
for Euroscope as well as additional tooling for processing VATSIM related data.

## Current Features

 * Pydantic models for the VATSIM status endpoints and the VATSIM datafeed
 * Simple fetchers for endpoints and the datafeed

## Example

```python
import vatsim

data = vatsim.fetch_vatsim_data()
```
