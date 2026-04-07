# Environment Setup Guide

All configuration for the FDA Players Intelligence System is managed through environment variables in the `.env` file. **No hardcoding** - everything is configurable and secure.

## Quick Setup

### 1. Create `.env` File

```bash
cp .env.example .env
```

### 2. Add Your Wyscout API Credentials

Edit `.env` with your credentials:

```env
WYSCOUT_CLIENT_ID=your_client_id_here
WYSCOUT_CLIENT_SECRET=your_client_secret_here
```

**That's it!** All other settings have sensible defaults.

## Configuration Variables

### Required

| Variable | Purpose |
|----------|---------|
| `WYSCOUT_CLIENT_ID` | Your Wyscout API client ID |
| `WYSCOUT_CLIENT_SECRET` | Your Wyscout API client secret |

### Optional (with defaults)

| Variable | Purpose | Default |
|----------|---------|---------|
| `API_BASE_URL` | Wyscout API endpoint | `https://apirest.wyscout.com/v3` |
| `API_TIMEOUT` | Request timeout (seconds) | `30` |
| `ACTIVE_COMPETITION_IDS` | Competitions to process | `524,527,520` (Serie A, B, C) |
| `CACHE_DIR` | Cache location | `data/cache` |
| `RAW_DATA_DIR` | Raw data location | `data/raw` |
| `PROCESSED_DATA_DIR` | Processed data location | `data/processed` |
| `ENVIRONMENT` | Environment (development/production) | `development` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |

## How It Works

The application loads configuration automatically:

```python
from src.config import CLIENT_ID, ACTIVE_COMPETITIONS, API_BASE

# All values come from .env - no parameters needed!
print(f"Credentials loaded: {bool(CLIENT_ID)}")
print(f"Active competitions: {list(ACTIVE_COMPETITIONS.keys())}")
```

## Verification

Test your configuration:

```python
from src.config import CLIENT_ID, CLIENT_SECRET, KNOWN_COMPETITIONS, ACTIVE_COMPETITIONS

print(f"✓ Credentials loaded: {bool(CLIENT_ID and CLIENT_SECRET)}")
print(f"✓ Active competitions: {list(ACTIVE_COMPETITIONS.keys())}")
print(f"✓ Known competitions: {list(KNOWN_COMPETITIONS.keys())}")
```

## Environment-Specific Setups

### Development
```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_TIMEOUT=30
```

### Production
```env
ENVIRONMENT=production
LOG_LEVEL=WARNING
API_TIMEOUT=60
```

### Using Multiple .env Files

Create separate configuration files:
```bash
.env                  # Default (development)
.env.production       # Production config
.env.staging          # Staging config
```

## Troubleshooting

### Error: "Missing Wyscout API credentials!"

**Problem**: Config can't find CLIENT_ID or CLIENT_SECRET

**Solutions**:
1. Verify `.env` exists in project root: `ls .env`
2. Check credentials are set: `grep WYSCOUT_ .env`
3. Ensure no extra spaces: `WYSCOUT_CLIENT_ID=value` (no spaces around `=`)
4. Verify values aren't quoted: `WYSCOUT_CLIENT_ID=your_id` (not `"your_id"`)
5. Restart Python interpreter after editing `.env`

### Variables Not Loading

**Problem**: `.env` file exists but variables aren't being read

**Solutions**:
1. Verify `python-dotenv` installed: `pip list | grep dotenv`
2. If missing: `pip install python-dotenv`
3. Verify `.env` is in project root (not in subdirectories)
4. Try explicit load: `from dotenv import load_dotenv; load_dotenv('.env')`

### Custom Competition IDs

**Problem**: Want to analyze different competitions

**Solution**: Update `ACTIVE_COMPETITION_IDS` in `.env`:

```env
# Original (default)
ACTIVE_COMPETITION_IDS=524,527,520

# Custom (only Serie A)
ACTIVE_COMPETITION_IDS=524

# Custom (only Primavera)
ACTIVE_COMPETITION_IDS=516
```

## Security Best Practices

✅ **DO**
- Store credentials in `.env` only
- Add `.env` to `.gitignore` (already done)
- Rotate credentials regularly
- Use different credentials for dev/prod
- Keep `.env` file private

❌ **DON'T**
- Hardcode credentials in source files
- Commit `.env` to version control
- Share credentials via email/chat
- Use weak/placeholder credentials in production
- Store credentials in comments

## References

- [Python-dotenv Documentation](https://github.com/theyak/python-dotenv)
- [12 Factor App - Config](https://12factor.net/config)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)