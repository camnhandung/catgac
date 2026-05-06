from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel, create_engine

# 1. BẢNG ĐƠN VỊ
class Unit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True) # VD: d1, c14...
    password: str 
    role: str = Field(default="unit") # "admin" hoặc "unit"

# 2. BẢNG VỌNG GÁC
class GuardPost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

# 3. KHO CÁN BỘ (Danh sách Sĩ quan của từng đơn vị)
class Officer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    phone_number: str = Field(index=True)
    unit_id: int = Field(foreign_key="unit.id")

# 4. LỊCH GÁC TỔNG (CQTM tạo khung)
class MasterShift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    guard_date: date 
    shift_time: str # VD: "02.00-04.00"
    post_id: int = Field(foreign_key="guardpost.id")
    unit_id: int = Field(foreign_key="unit.id") # Giao cho đơn vị nào

# 5. LỊCH GÁC CHI TIẾT (Đơn vị điền tên người vào)
class ShiftAssignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    master_shift_id: int = Field(foreign_key="mastershift.id")
    officer_id: int = Field(foreign_key="officer.id")

# 6. BÁO CÁO KỶ LUẬT (Đi muộn)
class LateReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shift_id: int = Field(foreign_key="mastershift.id")
    reporter_id: int = Field(foreign_key="officer.id") # Người báo cáo
    reported_officer_id: int = Field(foreign_key="officer.id") # Người bị đi muộn
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ==========================================
# KẾT NỐI LÊN SUPABASE CLOUD
# ==========================================
supabase_url = "postgresql://postgres.tdnexkmyvkkovoldhrnf:ETEw199juLtunC1v@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres"

engine = create_engine(supabase_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)