# Configuración de Credenciales Google Sheets API

## Archivos requeridos

### 1. `credentials.json`
Archivo de configuración OAuth2 descargado desde Google Cloud Console.

**Ejemplo de estructura:**
```json
{
  "installed": {
    "client_id": "<CLIENT_ID>",
    "project_id": "<PROJECT_ID>",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "<SECRET>",
    "redirect_uris": ["http://localhost"]
  }
}
```

### 2. `token.json`
Archivo generado automáticamente después de la primera autenticación.

**Ejemplo de estructura:**
```json
{
  "token": "<ACCESS_TOKEN>",
  "refresh_token": "<REFRESH_TOKEN>",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "<CLIENT_ID>",
  "client_secret": "<SECRET>",
  "scopes": ["https://www.googleapis.com/auth/spreadsheets"],
  "universe_domain": "googleapis.com",
  "account": "",
  "expiry": "<EXPIRY_TIMESTAMP>"
}
```

## Cómo obtener los archivos

### Paso 1: Crear proyecto en Google Cloud Console
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Google Sheets API**

### Paso 2: Crear credenciales OAuth2
1. Ve a **"APIs & Services"** > **"Credentials"**
2. Haz clic en **"Create Credentials"** > **"OAuth client ID"**
3. Selecciona **"Desktop application"**
4. Completa el nombre de la aplicación
5. Haz clic en **"Create"**

### Paso 3: Descargar credentials.json
1. En la lista de credenciales, haz clic en el ícono de descarga
2. Descarga el archivo JSON
3. Renómbralo a `credentials.json`
4. Colócalo en `src/credentials/credentials.json`

### Paso 4: Primera ejecución (genera token.json)
1. Ejecuta el programa: `cd src && python main.py`
2. Se abrirá automáticamente el navegador
3. Inicia sesión con tu cuenta de Google
4. Autoriza el acceso a Google Sheets
5. Se creará automáticamente `token.json`

## Ubicación de archivos

```
src/credentials/
├── credentials.json    # Configuración OAuth2 (descargar manualmente)
├── token.json          # Token de acceso (generado automáticamente)
└── README.md          # Este archivo
```

## Renovación automática

El sistema renueva automáticamente los tokens expirados usando el `refresh_token`. No necesitas intervención manual.