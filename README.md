# Tuya Manual Integration for Home Assistant

Integrazione manuale per dispositivi Tuya non riconosciuti automaticamente, con comunicazione diretta via API Tuya Cloud.

## Installazione

Copia la cartella `tuya_manual` in `config/custom_components/`.

Aggiungi in `configuration.yaml`:

```yaml
tuya_manual:
  client_id: TUYA_CLIENT_ID
  client_secret: TUYA_CLIENT_SECRET
  device_id: TUYA_DEVICE_ID
```

Riavvia Home Assistant.

## Funzionalità

- Sensori batteria e stato pioggia
- Switch per valvole e sensore pioggia

## Licenza

MIT License
