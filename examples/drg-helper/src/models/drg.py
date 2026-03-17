"""DRG 分组模型"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class DRGCategory(Enum):
    """DRG 分类"""
    MDC = "mdc"           # 主要诊断分类
    ADRG = "adrg"         # 邻近 DRG
    DRG = "drg"           # DRG 分组


@dataclass
class PatientInfo:
    """患者信息"""
    patient_id: str
    age: int
    gender: str  # M/F
    admission_type: str  # emergency/elective
    principal_diagnosis: str  # ICD-10
    secondary_diagnoses: List[str]  # ICD-10
    procedures: List[str]  # ICD-9-CM-3


@dataclass
class DRGResult:
    """DRG 分组结果"""
    mdc: str
    adrg: str
    drg: str
    weight: float
    description: str
    confidence: float


@dataclass
class DRGGroup:
    """DRG 分组器"""
    
    def calculate(self, patient: PatientInfo) -> DRGResult:
        """计算 DRG 分组"""
        # 简化逻辑：实际需要完整的 DRG 规则库
        mdc = self._get_mdc(patient.principal_diagnosis)
        adrg = self._get_adrg(mdc, patient.procedures)
        drg = self._get_drg(adrg, patient.secondary_diagnoses)
        
        return DRGResult(
            mdc=mdc,
            adrg=adrg,
            drg=drg,
            weight=self._get_weight(drg),
            description=self._get_description(drg),
            confidence=0.95
        )
    
    def _get_mdc(self, diagnosis: str) -> str:
        """获取主要诊断分类"""
        # 简化：按 ICD-10 首字母映射
        prefix = diagnosis[0].upper()
        mdc_map = {
            "A": "01", "B": "01",  # 传染病
            "C": "02",              # 肿瘤
            "D": "03", "E": "04",  # 内分泌/血液
            "F": "05", "G": "06",  # 精神/神经
            "H": "07", "I": "08",  # 循环/呼吸
            "J": "09", "K": "10",  # 消化/肝胆
            "L": "11", "M": "12",  # 肌肉/皮肤
            "N": "13", "O": "14",  # 泌尿/产科
            "P": "15", "Q": "16",  # 新生儿/肿瘤
            "R": "17", "S": "18",  # 症状/损伤
            "T": "19", "U": "20",  # 中毒/健康
            "V": "21", "W": "22",  # 环境/其他
            "X": "23", "Y": "24",  # 补充分类
            "Z": "25"               # 影响健康因素
        }
        return mdc_map.get(prefix, "00")
    
    def _get_adrg(self, mdc: str, procedures: List[str]) -> str:
        """获取邻近 DRG"""
        if procedures:
            return f"{mdc}{'C' if mdc < '10' else 'B'}"
        return f"{mdc}{'B' if mdc < '10' else 'A'}"
    
    def _get_drg(self, adrg: str, secondary: List[str]) -> str:
        """获取 DRG"""
        has_complication = len(secondary) > 2
        suffix = "3" if has_complication else "1" if not has_complication else "2"
        return f"{adrg}{suffix}"
    
    def _get_weight(self, drg: str) -> float:
        """获取权重"""
        weights = {
            "01": 1.2, "02": 1.5, "03": 1.1,
            "08": 1.3, "09": 0.9, "10": 1.0
        }
        base = drg[:2]
        return weights.get(base, 1.0)
    
    def _get_description(self, drg: str) -> str:
        """获取描述"""
        descriptions = {
            "01": "神经系统疾病",
            "02": "肿瘤疾病",
            "08": "呼吸系统疾病",
            "09": "消化系统疾病"
        }
        base = drg[:2]
        return descriptions.get(base, "其他疾病")
