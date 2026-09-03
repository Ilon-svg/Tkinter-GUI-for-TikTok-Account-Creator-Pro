# API Reference

## Authentication
All endpoints require `X-API-Key` header.

## Endpoints

### POST /v1/tiktok/create
Create single account.

**Request:**
```json
{
  "region": "US",
  "sms_verify": true,
  "bio": "Hello!"
}

