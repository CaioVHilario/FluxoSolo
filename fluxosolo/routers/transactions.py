from http import HTTPStatus
from typing import Annotated
from datetime import datetime
import calendar

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from fluxosolo.core.database import get_session
from fluxosolo.core.secrets import get_current_user
from fluxosolo.models.transactions import User, Transaction
from fluxosolo.schemas import Message, TransactionsList, FilterTransactions
from fluxosolo.services.parsers.factory import UnsupportedFormatErro
from fluxosolo.services.parsers.main import read_extract_file
from fluxosolo.services.save_df_to_sql import persist_on_db

router = APIRouter(prefix="/transactions", tags=["transactions"])
TSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
TFile = Annotated[
    UploadFile, File(description="Extrato bancário em PDF ou CSV")
]


@router.post("/", response_model=Message)
async def create_transactions(
    session: TSession, current_user: CurrentUser, file: TFile
):

    if not file.filename:
        raise HTTPException(status_code=400, detail="File without name")

    bytes_content = await file.read()
    file_name = file.filename

    try:
        df = read_extract_file(file_name, bytes_content)

        persist_on_db(df)

    except UnsupportedFormatErro as e:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE, detail=str(e)
        )

    except AttributeError:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Não foi possível ler o conteúdo do arquivo. Verifique se o extrato não está corrompido",
        )

    return {"message": "File processed successfully"}


@router.get('/', response_model=TransactionsList)
def get_transactions(
    session: TSession,
    current_user: CurrentUser,
    filter_transactions: Annotated[FilterTransactions, Query()]
):
    query = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .options(
            joinedload(Transaction.category),
            joinedload(Transaction.bank),
            joinedload(Transaction.transaction_type)
        )
    )

    if filter_transactions.month and filter_transactions.year:
        last_day_month = calendar.monthrange(
            filter_transactions.year, filter_transactions.month
        )[1]

        initial_date = datetime(
            filter_transactions.year, filter_transactions.month, 1, 0, 0, 0
        )
        final_date = datetime(
            filter_transactions.year,
            filter_transactions.month,
            last_day_month, 
            23,
            59,
            59
        )

        query = query.where(Transaction.date.between(initial_date, final_date))

    elif filter_transactions.year:
        initial_date = datetime(filter_transactions.year, 1, 1, 0, 0, 0)
        final_date = datetime(filter_transactions.year, 12, 31, 23, 59, 59)
        query = query.where(Transaction.date.between(initial_date, final_date))

    transactions = session.scalars(
        query
        .offset(filter_transactions.offset)
        .limit(filter_transactions.limit)
    )

    return {'transactions': transactions.all()}