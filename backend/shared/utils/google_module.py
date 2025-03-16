from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.exceptions import RefreshError
from typing import List


from backend.api.schemas.google_schema import CreateSheetSchema, SheetDataSchema


class GoogleManager():
  SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
  ]
  def __init__(self):
    """Инициализация Google API с сервисным аккаунтом"""
    self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'gsheets.json', 
        self.SCOPE
    )
    self.sheets_service = build("sheets", "v4", credentials=self.credentials)
    self.drive_service = build("drive", "v3", credentials=self.credentials)

  def create_spreadsheet(self, sheet_details: CreateSheetSchema) -> str | None:
    """Создаёт Google Spreadsheet и даёт доступ пользователю"""
    try:
      sheets = [{"properties": {"title": sheet}} for sheet in sheet_details.sheet_names]

      spreadsheet_body = {
        "properties": {"title": sheet_details.title},
        "sheets": sheets
      }

      spreadsheet = (
        self.sheets_service.spreadsheets()
        .create(body=spreadsheet_body, fields="spreadsheetId")
        .execute()
      )

      spreadsheet_id = spreadsheet.get("spreadsheetId")
      if sheet_details.email != None:
        permission_user = {
          "type": "user",
          "role": "writer",
          "emailAddress": sheet_details.email
        }
        self.drive_service.permissions().create(
          fileId=spreadsheet_id,
          body=permission_user,
          fields="id"
        ).execute()

      permission_sudo = {
        "type": "user",
        "role": "writer",
        "emailAddress": "sudo.feaskic@gmail.com"
      }

      self.drive_service.permissions().create(
        fileId=spreadsheet_id,
        body=permission_sudo,
        fields="id",
        sendNotificationEmail=False
      ).execute()

      return spreadsheet_id

    except HttpError as error:
      return f"Google API error: {error}"

    except RefreshError:
      return "Ошибка авторизации. Проверьте учетные данные."

  def input_headers(self, sheet_details: SheetDataSchema):
    """Input headers into Google Sheet with professional formatting"""
    try:
        headers = [row.header for row in sheet_details.rows]
        body = {
            "values": [headers]
        }
        
        # Update headers
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_details.sheet_id,
            range=f"{sheet_details.sheet_name}!A1:{chr(65+len(headers)-1)}1",
            valueInputOption="RAW",
            body=body
        ).execute()

        sheet_metadata = self.sheets_service.spreadsheets().get(
            spreadsheetId=sheet_details.sheet_id
        ).execute()
        
        sheet_id = None
        for s in sheet_metadata.get('sheets', ''):
            if s.get('properties', {}).get('title') == sheet_details.sheet_name:
                sheet_id = s.get('properties', {}).get('sheetId')
                break

        if sheet_id is not None:
            requests = [{
                # Сначала устанавливаем размер таблицы
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': sheet_id,
                        'gridProperties': {
                            'frozenRowCount': 1,
                            'rowCount': 100,  # Ограничиваем количество видимых строк
                            'columnCount': 26  # Устанавливаем количество столбцов до 'Z'
                        }
                    },
                    'fields': 'gridProperties(frozenRowCount,rowCount,columnCount)'
                }
            }, {
                # Форматирование заголовков
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 0,
                        'endRowIndex': 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': len(headers)
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {
                                'red': 0.1,
                                'green': 0.1,
                                'blue': 0.1
                            },
                            'textFormat': {
                                'bold': True,
                                'fontSize': 12,
                                'foregroundColor': {
                                    'red': 1.0,
                                    'green': 1.0,
                                    'blue': 1.0
                                }
                            },
                            'horizontalAlignment': 'CENTER',
                            'verticalAlignment': 'MIDDLE',
                            'padding': {
                                'top': 5,
                                'right': 5,
                                'bottom': 5,
                                'left': 5
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,padding)'
                }
            }, {
                # Автоматическая подгонка ширины используемых столбцов
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': len(headers)
                    }
                }
            }, {
                # Скрываем неиспользуемые столбцы
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': len(headers),
                        'endIndex': 26  # До столбца 'Z'
                    },
                    'properties': {
                        'hiddenByUser': True
                    },
                    'fields': 'hiddenByUser'
                }
            }]

            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=sheet_details.sheet_id,
                body={'requests': requests}
            ).execute()

            return True

    except HttpError as error:
        print(f"Google API error: {error}")
        return None
    except RefreshError:
        print("Ошибка авторизации. Проверьте учетные данные.")
        return None

  def input_row_data(self, sheet_id: str, sheet_name: str, row_data: List[str]):
    """Add new row data with automatic formatting and smart column resizing"""
    try:
        # Get the next empty row
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=f"{sheet_name}!A:A"
        ).execute()
        next_row = len(result.get('values', [])) + 1

        # Insert data
        body = {
            "values": [row_data]
        }
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{sheet_name}!A{next_row}",
            valueInputOption="RAW",
            body=body
        ).execute()

        # Get sheet ID
        sheet_metadata = self.sheets_service.spreadsheets().get(
            spreadsheetId=sheet_id
        ).execute()
        
        sheet_id_num = None
        for s in sheet_metadata.get('sheets', ''):
            if s.get('properties', {}).get('title') == sheet_name:
                sheet_id_num = s.get('properties', {}).get('sheetId')
                break

        if sheet_id_num is not None:
            requests = [{
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id_num,
                        'startRowIndex': next_row - 1,
                        'endRowIndex': next_row,
                        'startColumnIndex': 0,
                        'endColumnIndex': len(row_data)
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {
                                'red': 1.0,
                                'green': 1.0,
                                'blue': 1.0
                            },
                            'textFormat': {
                                'fontSize': 11,
                                'foregroundColor': {
                                    'red': 0.2,
                                    'green': 0.2,
                                    'blue': 0.2
                                }
                            },
                            'horizontalAlignment': 'CENTER',
                            'verticalAlignment': 'MIDDLE',
                            'padding': {
                                'top': 3,
                                'right': 3,
                                'bottom': 3,
                                'left': 3
                            },
                            'wrapStrategy': 'WRAP'
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat,padding,wrapStrategy,horizontalAlignment,verticalAlignment)'
                }
            }]

            # Умная подгонка ширины столбцов
            for i, value in enumerate(row_data):
                pixel_size = None
                if len(value) > 30:
                    pixel_size = 200  # Для очень длинных текстов
                elif len(value) > 15:
                    pixel_size = 150  # Для средних текстов
                elif len(value) > 3:
                    pixel_size = 100  # Для коротких текстов
                
                if pixel_size:
                    requests.append({
                        'updateDimensionProperties': {
                            'range': {
                                'sheetId': sheet_id_num,
                                'dimension': 'COLUMNS',
                                'startIndex': i,
                                'endIndex': i + 1
                            },
                            'properties': {
                                'pixelSize': pixel_size
                            },
                            'fields': 'pixelSize'
                        }
                    })

            # Автоматическая подгонка высоты строки
            requests.append({
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': sheet_id_num,
                        'dimension': 'ROWS',
                        'startIndex': next_row - 1,
                        'endIndex': next_row
                    }
                }
            })

            # Apply alternating colors based on row number
            if next_row % 2 == 0:
                requests[0]['repeatCell']['cell']['userEnteredFormat']['backgroundColor'] = {
                    'red': 0.97,
                    'green': 0.97,
                    'blue': 0.97
                }

            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=sheet_id,
                body={'requests': requests}
            ).execute()

            return True

    except HttpError as error:
        print(f"Google API error: {error}")
        return None
    except RefreshError:
        print("Ошибка авторизации. Проверьте учетные данные.")
        return None

  def delete_all_spreadsheets(self) -> str:
    """Удаляет все Google Spreadsheets навсегда"""
    try:
      results = self.drive_service.files().list(
        q="mimeType='application/vnd.google-apps.spreadsheet'",
        fields="files(id, name)"
      ).execute()
      items = results.get('files', [])

      if not items:
        return "No spreadsheets found."

      for item in items:
        self.drive_service.files().delete(fileId=item['id']).execute()

      return "All spreadsheets have been deleted."

    except HttpError as error:
      return f"Google API error: {error}"

    except RefreshError:
      return "Ошибка авторизации. Проверьте учетные данные."