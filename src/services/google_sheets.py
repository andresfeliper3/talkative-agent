import os
import os.path
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from models.state import LeadState


class GoogleSheetsService:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    
    def __init__(self):
        self.service = None
        self.spreadsheet_id = None
        self.sheet_name = None
        self.credentials = None
        self.SPREADSHEET_ID = "181M0QYYtFhEXB39Qal_htrYe5vI8hCFOdna3mglyGZQ"
        self.SHEET_NAME = "Leads"
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        try:
            creds = None
            token_path = Path(__file__).parent.parent / "credentials" / "token.json"
            
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(str(token_path), self.SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception as e:
                        print(f"Error renovando token: {e}")
                        creds = None
                
                if not creds or not creds.valid:
                    credentials_path = Path(__file__).parent.parent / "credentials" / "credentials.json"
                    
                    if not os.path.exists(credentials_path):
                        return
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(credentials_path), self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                
                with open(token_path, "w") as token:
                    token.write(creds.to_json())
            
            self.credentials = creds
            self.service = build("sheets", "v4", credentials=creds)
            self._auto_configure_spreadsheet()
            
        except Exception:
            self.service = None
            self.credentials = None
    
    def _ensure_valid_credentials(self) -> bool:
        """Ensure credentials are valid, refresh if needed."""
        if not self.credentials:
            return False
        
        if not self.credentials.valid:
            if self.credentials.expired and self.credentials.refresh_token:
                try:
                    self.credentials.refresh(Request())
                    # Save refreshed token
                    token_path = Path(__file__).parent.parent / "credentials" / "token.json"
                    with open(token_path, "w") as token:
                        token.write(self.credentials.to_json())
                    return True
                except Exception as e:
                    print(f"Error renovando token: {e}")
                    return False
            else:
                return False
        
        return True
    
    def _auto_configure_spreadsheet(self) -> None:
        try:
            if not self.service:
                return
            
            sheet = self.service.spreadsheets()
            spreadsheet_info = sheet.get(spreadsheetId=self.SPREADSHEET_ID).execute()
            sheets = spreadsheet_info.get('sheets', [])
            
            if not sheets:
                return
            
            first_sheet_name = sheets[0]['properties']['title']
            
            self.spreadsheet_id = self.SPREADSHEET_ID
            self.sheet_name = first_sheet_name
            
            self._setup_elegant_headers()
            
        except Exception:
            self.spreadsheet_id = None
            self.sheet_name = None
    
    def _setup_elegant_headers(self) -> None:
        try:
            read_range = f"{self.sheet_name}!A1:H1"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=read_range
            ).execute()
            
            values = result.get("values", [])
            
            if not values or not values[0]:
                headers = [
                    "Es Corporativo",
                    "Tipo de Evento", 
                    "Presupuesto",
                    "Nombre",
                    "Contacto",
                    "Tipo de Contacto",
                    "Calificado",
                    "Fecha de Registro"
                ]
                
                header_range = f"{self.sheet_name}!A1:H1"
                body = {'values': [headers]}
                
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=header_range,
                    valueInputOption='RAW',
                    body=body
                ).execute()
                
                self._format_headers()
                
        except Exception:
            pass
    
    def _format_headers(self) -> None:
        try:
            requests = [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 8
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": 0.2,
                                    "green": 0.4,
                                    "blue": 0.8
                                },
                                "textFormat": {
                                    "foregroundColor": {
                                        "red": 1.0,
                                        "green": 1.0,
                                        "blue": 1.0
                                    },
                                    "fontSize": 12,
                                    "bold": True
                                },
                                "horizontalAlignment": "CENTER"
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                    }
                }
            ]
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={"requests": requests}
            ).execute()
            
        except Exception:
            pass
    
    def set_spreadsheet_id(self, spreadsheet_id: str) -> bool:
        try:
            if not self.service:
                return False
            
            sheet = self.service.spreadsheets()
            spreadsheet_info = sheet.get(spreadsheetId=spreadsheet_id).execute()
            sheets = spreadsheet_info.get('sheets', [])
            
            if not sheets:
                return False
            
            first_sheet_name = sheets[0]['properties']['title']
            self.sheet_name = first_sheet_name
            self.spreadsheet_id = spreadsheet_id
            
            return True
            
        except HttpError:
            return False
        except Exception:
            return False
    
    def is_available(self) -> bool:
        if not self.service or not self.spreadsheet_id:
            return False
        
        return self._ensure_valid_credentials() and self.sheet_name is not None
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "service_initialized": self.service is not None,
            "spreadsheet_id_available": self.spreadsheet_id is not None,
            "sheet_name_available": self.sheet_name is not None,
            "fully_available": self.is_available(),
            "error_message": self._get_error_message()
        }
    
    def _get_error_message(self) -> Optional[str]:
        if self.is_available():
            return None
        
        if self.service is None:
            return "Google Sheets service not initialized. Check credentials.json file and authentication."
        elif self.spreadsheet_id is None:
            return "Spreadsheet ID not set. Use set_spreadsheet_id() to set your spreadsheet ID."
        elif self.sheet_name is None:
            return "Sheet name not detected. Check spreadsheet access."
        
        return "Unknown initialization error."
    
    def save_lead(self, state: LeadState) -> bool:
        if not self.is_available():
            return False
        
        if not self._ensure_valid_credentials():
            return False
        
        try:
            if self._is_duplicate(state):
                return False
            
            row_data = self._prepare_row_data(state)
            
            sheet = self.service.spreadsheets()
            
            read_range = f"{self.sheet_name}!A:H"
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id, 
                range=read_range
            ).execute()
            
            values = result.get("values", [])
            next_row = len(values) + 1 if values else 2
            
            write_range = f"{self.sheet_name}!A{next_row}:H{next_row}"
            
            body = {'values': [row_data]}
            
            write_result = (
                sheet.values()
                .update(
                    spreadsheetId=self.spreadsheet_id,
                    range=write_range,
                    valueInputOption='RAW',
                    body=body
                )
                .execute()
            )
            
            return True
            
        except HttpError as e:
            if e.resp.status == 403:
                pass
            elif e.resp.status == 400:
                pass
            return False
        except Exception:
            return False
    
    def _is_duplicate(self, state: LeadState) -> bool:
        try:
            sheet = self.service.spreadsheets()
            read_range = f"{self.sheet_name}!A:H"
            
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=read_range
            ).execute()
            
            values = result.get("values", [])
            if not values or len(values) <= 1:
                return False
            
            headers = values[0] if values else []
            data_rows = values[1:] if len(values) > 1 else []
            
            contact_col = None
            contact_type_col = None
            
            for i, header in enumerate(headers):
                if "Contacto" in header and "Tipo" not in header:
                    contact_col = i
                elif "Tipo de Contacto" in header:
                    contact_type_col = i
            
            if contact_col is None or contact_type_col is None:
                return False
            
            for row in data_rows:
                if (len(row) > max(contact_col, contact_type_col) and
                    row[contact_col] == state["contact"] and 
                    row[contact_type_col] == state["contact_type"]):
                    return True
            
            return False
            
        except HttpError:
            return False
        except Exception:
            return False
    
    def _prepare_row_data(self, state: LeadState) -> List[str]:
        return [
            "Sí" if state["is_corporate"] else "No",
            state["event_type"] or "No especificado",
            f"${state['budget']:,.2f}" if state["budget"] else "No especificado",
            state["name"] or "No especificado",
            state["contact"] or "No especificado",
            state["contact_type"] or "No especificado",
            "Sí" if state["qualified"] else "No",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
    
    def get_all_leads(self) -> List[Dict[str, Any]]:
        if not self.is_available():
            return []
        
        try:
            sheet = self.service.spreadsheets()
            read_range = f"{self.sheet_name}!A:H"
            
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=read_range
            ).execute()
            
            values = result.get("values", [])
            if not values:
                return []
            
            headers = values[0]
            data_rows = values[1:] if len(values) > 1 else []
            
            records = []
            for row in data_rows:
                record = {}
                for i, header in enumerate(headers):
                    record[header] = row[i] if i < len(row) else ""
                records.append(record)
            
            return records
            
        except HttpError:
            return []
        except Exception:
            return []
    
    def get_lead_count(self) -> int:
        if not self.is_available():
            return 0
        
        try:
            sheet = self.service.spreadsheets()
            read_range = f"{self.sheet_name}!A:H"
            
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=read_range
            ).execute()
            
            values = result.get("values", [])
            return max(0, len(values) - 1) if values else 0
            
        except HttpError:
            return 0
        except Exception:
            return 0


# Global instance
sheets_service = GoogleSheetsService()


def save_lead_to_sheets(state: LeadState) -> bool:
    return sheets_service.save_lead(state)


def is_sheets_available() -> bool:
    return sheets_service.is_available()


def get_leads_count() -> int:
    return sheets_service.get_lead_count()


def get_sheets_status() -> Dict[str, Any]:
    return sheets_service.get_status()


def set_spreadsheet_id(spreadsheet_id: str) -> bool:
    return sheets_service.set_spreadsheet_id(spreadsheet_id)