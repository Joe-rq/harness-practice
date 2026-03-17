"""DRG 分组器测试"""

import pytest
from src.models.drg import PatientInfo, DRGGroup


class TestDRGGroup:
    """DRG 分组器测试"""
    
    def setup_method(self):
        """测试前准备"""
        self.group = DRGGroup()
    
    def test_mdc_classification(self):
        """测试主要诊断分类"""
        # 测试肺炎 (J18.9)
        patient = PatientInfo(
            patient_id="P001",
            age=65,
            gender="M",
            admission_type="emergency",
            principal_diagnosis="J18.9",
            secondary_diagnoses=[],
            procedures=[]
        )
        
        result = self.group.calculate(patient)
        
        assert result.mdc == "09"  # 呼吸系统疾病
        assert result.adrg == "09B"
        assert result.drg == "09B1"
    
    def test_with_procedures(self):
        """测试有手术的情况"""
        patient = PatientInfo(
            patient_id="P002",
            age=45,
            gender="F",
            admission_type="elective",
            principal_diagnosis="J18.9",
            secondary_diagnoses=[],
            procedures=["45.13"]  # 胃镜检查
        )
        
        result = self.group.calculate(patient)
        
        assert result.adrg == "09C"  # 有手术
    
    def test_with_complications(self):
        """测试有合并症的情况"""
        patient = PatientInfo(
            patient_id="P003",
            age=70,
            gender="M",
            admission_type="emergency",
            principal_diagnosis="J18.9",
            secondary_diagnoses=["I10", "E11.9", "E78.5"],  # 高血压、糖尿病、高血脂
            procedures=[]
        )
        
        result = self.group.calculate(patient)
        
        assert result.drg == "09B3"  # 有严重合并症
    
    def test_oncology(self):
        """测试肿瘤病例"""
        patient = PatientInfo(
            patient_id="P004",
            age=55,
            gender="M",
            admission_type="elective",
            principal_diagnosis="C34.9",  # 肺癌
            secondary_diagnoses=[],
            procedures=["32.41"]  # 肺叶切除
        )
        
        result = self.group.calculate(patient)
        
        assert result.mdc == "02"  # 肿瘤
    
    def test_weight(self):
        """测试权重"""
        patient = PatientInfo(
            patient_id="P005",
            age=30,
            gender="F",
            admission_type="emergency",
            principal_diagnosis="J18.9",
            secondary_diagnoses=[],
            procedures=[]
        )
        
        result = self.group.calculate(patient)
        
        assert result.weight > 0
        assert isinstance(result.weight, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
