"""DRG Helper API"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from src.models.drg import PatientInfo, DRGGroup

app = FastAPI(title="DRG Helper", version="1.0.0")

# 初始化分组器
drg_group = DRGGroup()


class DiagnosisRequest(BaseModel):
    """诊断请求"""
    patient_id: str
    age: int
    gender: str
    admission_type: str
    principal_diagnosis: str
    secondary_diagnoses: Optional[List[str]] = []
    procedures: Optional[List[str]] = []


class DiagnosisResponse(BaseModel):
    """诊断响应"""
    mdc: str
    adrg: str
    drg: str
    weight: float
    description: str
    confidence: float


@app.get("/")
async def root():
    """健康检查"""
    return {"status": "ok", "service": "drg-helper"}


@app.post("/classify", response_model=DiagnosisResponse)
async def classify_drg(request: DiagnosisRequest):
    """DRG 分组"""
    try:
        patient = PatientInfo(
            patient_id=request.patient_id,
            age=request.age,
            gender=request.gender,
            admission_type=request.admission_type,
            principal_diagnosis=request.principal_diagnosis,
            secondary_diagnoses=request.secondary_diagnoses or [],
            procedures=request.procedures or []
        )
        
        result = drg_group.calculate(patient)
        
        return DiagnosisResponse(
            mdc=result.mdc,
            adrg=result.adrg,
            drg=result.drg,
            weight=result.weight,
            description=result.description,
            confidence=result.confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/drg/{drg_code}")
async def get_drg_info(drg_code: str):
    """获取 DRG 信息"""
    # 简化实现
    return {
        "code": drg_code,
        "description": "DRG 分组描述",
        "weight": 1.0,
        "average_cost": 10000.0,
        "average_stay": 7.0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
