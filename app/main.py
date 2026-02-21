from fastapi import FastAPI
from pydantic import ValidationError
from app.models import IngestionRequest, IngestionResponse, UserRecord

app = FastAPI(title="Data Ingestion & Validation API")


@app.get("/")
def home():
    return {"message": "Data Ingestion API Running"}


@app.post("/api/v1/ingest/users", response_model=IngestionResponse)
def ingest_users(payload: IngestionRequest):

    valid_count = 0
    errors = []

    for index, record in enumerate(payload.records):
        try:
            UserRecord.model_validate(record)
            valid_count += 1
        except ValidationError as e:
            errors.append({
                "record_index": index,
                "errors": e.errors()
            })

    return IngestionResponse(
        batch_id=payload.batch_id,
        total_records=len(payload.records),
        valid_records=valid_count,
        invalid_records=len(payload.records) - valid_count,
        errors=errors
    )