from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import os
from pathlib import Path
import aiofiles
import json
import numpy as np
from datetime import datetime
from ..utils import apply_die_cutting, load_dies
from ..database import get_async_db
from .. import models
from ..security import get_current_active_user

router = APIRouter(
    prefix="/answer",
    tags=["Answer"],
    dependencies=[Depends(get_current_active_user)],
)

# Đường dẫn đến thư mục chứa database câu hỏi
QUESTION_DB_PATH = Path("question_database")

# Đường dẫn đến thư mục lưu bài nộp
SUBMISSIONS_PATH = Path("submissions")
SUBMISSIONS_PATH.mkdir(exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

async def load_question(question_id):
    question_file = QUESTION_DB_PATH / f"{question_id}.json"
    with open(question_file, "r") as f:
        content = f.read()
        question_data = json.loads(content)
    return np.array(question_data.get("start")), np.array(question_data.get("goal")), question_data.get("numDies", None), question_data.get("numSteps", None)

async def check_solve(id, ops):
    dies = load_dies()
    state, goal, limit_dies, limit_step = await load_question(id)
    num_dies = len(dies); num_step = 99999999999999; count_step = 0; count_die = set()
    if limit_dies:
        num_dies = 0
    if limit_step:
        num_step = 0

    check = np.all(state == goal)
    if check:
        return True
    
    while not check:
        op = ops[count_step]
        count_die.add(op['p'])
        if count_step > num_step or len(count_die) > num_dies:
            break
        state = apply_die_cutting(state, dies[op['p']], op['x'], op['y'], op['s'])
        count_step += 1
        check = np.all(state == goal)
    
    if check:
        return True
    return False
    
# API nộp bài
@router.post("")
async def submit_answer(data:dict, current_user: models.User = Depends(get_current_active_user), db: AsyncSession = Depends(get_async_db)):
    try:
        end_time = datetime.now()
        user_id = current_user.id
        step_factor = -0.3
        question_id = data.get("question_id")
        step_count = data.get("answer_data").get("n")
        ops = data.get("answer_data").get("ops")[:step_count]
        is_solved = await check_solve(question_id, ops)
        

        os.makedirs(f"{SUBMISSIONS_PATH}/{user_id}", exist_ok=True)
        with open(f"{SUBMISSIONS_PATH}/{user_id}/{question_id}.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Update thông tin kết quả vào user_id và question_id
        stmt = select(models.Submit).where(
            models.Submit.user_id == user_id,
            models.Submit.question_id == question_id
        )
        result = await db.execute(stmt)
        submit_record = result.scalars().first()
        total_time = (end_time - submit_record.start_time).total_seconds()

        points = submit_record.max_score + (step_factor * step_count) if is_solved else 0.0
        points = points - submit_record.resubmission_count

        if not submit_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy bản ghi Submit cho user_id và question_id đã cho."
            )

        # Cập nhật các trường cần thiết
        submit_record.end_time = end_time
        submit_record.step_count = step_count
        submit_record.resubmission_count += 1  # Tăng số lần nộp lại
        submit_record.total_time = total_time
        submit_record.status = 1 if is_solved else 0
        submit_record.score = points

        # Thực hiện commit thay đổi
        await db.commit()
        await db.refresh(submit_record)

        return {
            "question_id": question_id,
            "user_id": user_id,
            "start_time": submit_record.start_time,
            "end_time": end_time,
            "step_factor": step_factor,
            "step_count": step_count,
            "total_time": total_time,
            "status": is_solved,
            "match_count": submit_record.max_score,
            "score": points
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting answer: {str(e)}",
        )
    

@router.get("/{id}")
async def get_answer(id: int, current_user: models.User = Depends(get_current_active_user), db: AsyncSession = Depends(get_async_db)):
    try:
        user_id = current_user.id
        stmt = select(models.Submit).where(
            models.Submit.question_id == id,
            models.Submit.user_id == user_id
        )
        result = await db.execute(stmt)
        submit_record = result.scalars().first()

        if not submit_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy bản ghi Submit cho id đã cho."
            )

        return {
            "question_id": submit_record.question_id,
            "user_id": submit_record.user_id,
            "start_time": submit_record.start_time,
            "end_time": submit_record.end_time,
            "step_count": submit_record.step_count,
            "total_time": submit_record.total_time,
            "status": submit_record.status,
            "match_count": submit_record.max_score,
            "score": submit_record.score,
            "resubmission_count": submit_record.resubmission_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting answer: {str(e)}",
        )

# @router.get("/{id}")
# async def get_answer(
#     id: int,
#     current_user: models.User = Depends(get_current_active_user),  # Lấy người dùng hiện tại từ token
#     db: AsyncSession = Depends(get_async_db)
# ):
#     # print('🟢')
#     # print(current_user.id)
#     user_id = current_user.id
#     try:
#         stmt = select(models.Submit).where(
#             models.Submit.question_id == id,
#             models.Submit.user_id == user_id  # Sử dụng current_user.id thay vì user_id
#         )
#         result = await db.execute(stmt)
#         submit_record = result.scalars().first()

#         if not submit_record:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Không tìm thấy bản ghi Submit cho id đã cho.",
#             )

#         return {
#             "question_id": submit_record.question_id,
#             "user_id": submit_record.user_id,
#             "start_time": submit_record.start_time,
#             "end_time": submit_record.end_time,
#             "step_count": submit_record.step_count,
#             "total_time": submit_record.total_time,
#             "status": submit_record.status,
#             "match_count": submit_record.match_count,  # Giả sử bạn đã sửa lại tên trường đúng
#             "score": submit_record.score,
#             "resubmission_count": submit_record.resubmission_count,
#         }

#     except HTTPException as he:
#         # Truyền tiếp HTTPException đã ném
#         raise he
#     except Exception as e:
#         # Xử lý các ngoại lệ khác
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi khi lấy câu trả lời: {str(e)}",
#         )