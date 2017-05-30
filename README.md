Sonarr API Python Wrapper
==========================

Unofficial Python Wrapper for the [Sonarr](https://github.com/Sonarr/Sonarr) API

### Requirements
- requests

### Example Usage:

```
# Import SonarrAPI Class
from sonarr_api import SonarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com/api'
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate SonarrAPI Object
snr = SonarrAPI(host_url, api_key)

# Get and print TV Shows
print snr.get_series()
```

### Documentation

[Sonarr API Documentation](https://github.com/Sonarr/Sonarr/wiki/API)
