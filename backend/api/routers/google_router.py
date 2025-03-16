from typing import Annotated

from fastapi import APIRouter, Depends, Body
from backend.api.schemas.google_schema import CreateSheetSchema, SheetDataSchema, RowDataSchema
from backend.shared.utils.google_module import GoogleManager

gl = GoogleManager()

router = APIRouter(
  prefix='/google',
  tags=['Google Management']
  )

@router.post('/create-sheet')
async def create_spreadsheet(new_sheet_data: Annotated[CreateSheetSchema, Body()]):
  id_spr = gl.create_spreadsheet(new_sheet_data)
  return id_spr

@router.post('/input-headers')
async def input_headers(header_data: Annotated[SheetDataSchema, Body()]):
  if gl.input_headers(header_data):
    return True


@router.post('/input-row')
async def input_row(row_data: Annotated[RowDataSchema, Body()]):
    """Add new row data by mapping values to headers"""
    try:
        result = gl.sheets_service.spreadsheets().values().get(
            spreadsheetId=row_data.sheet_id,
            range=f"{row_data.sheet_name}!1:1"
        ).execute()
        
        headers = result.get('values', [[]])[0]

        ordered_data = []
        for header in headers:
            value = row_data.data.get(header, '')  # Empty string if header not found in data
            ordered_data.append(value)

        success = gl.input_row_data(
            sheet_id=row_data.sheet_id,
            sheet_name=row_data.sheet_name,
            row_data=ordered_data
        )

        return {"success": success}

    except Exception as e:
        return {"success": False, "error": str(e)}