from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

Base = declarative_base()

class ReferenceFile(Base):
    __tablename__ = 'reference_files'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    original_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)
    description = Column(Text)
    tags = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    usage_count = Column(Integer, default=0)
    checksum = Column(String(32))
    is_active = Column(Boolean, default=True)
    
    # Relación con comparaciones
    comparisons = relationship("Comparison", back_populates="reference_file")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'original_name': self.original_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'row_count': self.row_count,
            'column_count': self.column_count,
            'description': self.description,
            'tags': self.tags.split(',') if self.tags else [],
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'usage_count': self.usage_count,
            'checksum': self.checksum,
            'is_active': self.is_active
        }

class Comparison(Base):
    __tablename__ = 'comparisons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_file_id = Column(Integer, ForeignKey('reference_files.id'))
    compare_file_name = Column(String(255), nullable=False)
    compare_file_path = Column(Text)
    compare_file_size = Column(Integer)
    comparison_date = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float, nullable=False)
    total_differences = Column(Integer, default=0)
    modified_cells = Column(Integer, default=0)
    added_rows = Column(Integer, default=0)
    removed_rows = Column(Integer, default=0)
    added_columns = Column(Integer, default=0)
    removed_columns = Column(Integer, default=0)
    unique_in_reference = Column(Integer, default=0)
    unique_in_compare = Column(Integer, default=0)
    identical = Column(Boolean, default=False)
    result_data = Column(Text)  # JSON
    summary_data = Column(Text)  # JSON
    exported = Column(Boolean, default=False)
    export_format = Column(String(50))
    export_date = Column(DateTime)
    notes = Column(Text)
    
    # Relación con archivo de referencia
    reference_file = relationship("ReferenceFile", back_populates="comparisons")
    
    def to_dict(self, include_data=False):
        result = {
            'id': self.id,
            'reference_file_id': self.reference_file_id,
            'compare_file_name': self.compare_file_name,
            'compare_file_size': self.compare_file_size,
            'comparison_date': self.comparison_date.isoformat() if self.comparison_date else None,
            'processing_time': self.processing_time,
            'total_differences': self.total_differences,
            'modified_cells': self.modified_cells,
            'added_rows': self.added_rows,
            'removed_rows': self.removed_rows,
            'added_columns': self.added_columns,
            'removed_columns': self.removed_columns,
            'unique_in_reference': self.unique_in_reference,
            'unique_in_compare': self.unique_in_compare,
            'identical': self.identical,
            'exported': self.exported,
            'export_format': self.export_format,
            'export_date': self.export_date.isoformat() if self.export_date else None,
            'notes': self.notes
        }
        
        if include_data:
            result['result_data'] = json.loads(self.result_data) if self.result_data else None
            result['summary_data'] = json.loads(self.summary_data) if self.summary_data else None
        
        return result

class AppSetting(Base):
    __tablename__ = 'app_settings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text)
    description = Column(Text)
    updated_date = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_date': self.updated_date.isoformat() if self.updated_date else None
        }

class ActivityLog(Base):
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(100), nullable=False)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    file_name = Column(String(255))
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'file_name': self.file_name,
            'success': self.success,
            'error_message': self.error_message
        }

# Configuración de la base de datos
class DatabaseConfig:
    def __init__(self, db_path="altice_comparator.db"):
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        return self.SessionLocal()