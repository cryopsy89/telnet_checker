# Telnet Checker

HTTP microservice for TCP port availability checks.
Used as a Zabbix external check — Zabbix calls the endpoint,
gets JSON back with connection status.

## Usage

```bash
docker compose up -d
curl "http://localhost:8080/check?ip=192.168.1.1&port=443"
```

## Response

```json
{
  "ip": "192.168.1.1",
  "port": 443,
  "status": 1,
  "message": "Connection successful"
}
```