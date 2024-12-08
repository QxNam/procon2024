import aiofiles
import json
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import schemas, security
from ..database import get_async_db
from ..security import get_current_active_user
from ..models import Submit, User
from pathlib import Path
from datetime import datetime
PATH = Path("question_database")

router = APIRouter(
    prefix="/question",
    tags=["Questions"],
    dependencies=[Depends(get_current_active_user)],
)

# API lấy câu hỏi từ file JSON
@router.get("/{id}")
async def get_questions(id:int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_async_db)):
    try:
        user_id = current_user.id
        question_file = PATH / f"{id}.json"
        async with aiofiles.open(question_file, mode="r") as f:
            content = await f.read()
            data = json.loads(content)
            data['start_time'] = datetime.now()

        # kiểm tra xem user đã gọi câu này trước đó chưa
        stmt = select(Submit).where(
            Submit.user_id == user_id,
            Submit.question_id == id
        )
        result = await db.execute(stmt)
        result = result.scalars().first()

        # Nếu user chưa gọi câu này, tạo một đối tượng Submit mới
        if not result:
            # Tạo một đối tượng Submit mới
            submit = Submit(
                user_id=user_id,
                question_id=id,
                start_time=datetime.utcnow(),
                max_score=data['height']*data['width'],
            )
            
            # Thêm đối tượng vào phiên làm việc và commit
            db.add(submit)
            await db.commit()
            
            # Làm mới đối tượng để nhận giá trị từ cơ sở dữ liệu (như id tự tăng)
            await db.refresh(submit)
        
        return data
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading questions file: {str(e)}",
        )
