import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from models import ReferenceFile, Comparison, AppSetting, ActivityLog, DatabaseConfig
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Buscar la base de datos en el directorio de Electron
            possible_paths = [
                os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "AlticeFileComparator", "database", "altice_comparator.db"),
                os.path.join(os.getcwd(), "database", "altice_comparator.db"),
                "altice_comparator.db"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    db_path = path
                    break
            else:
                # Crear en el primer directorio válido
                db_path = possible_paths[0]
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.config = DatabaseConfig(db_path)
        self.config.create_tables()
        logger.info(f"Base de datos inicializada en: {db_path}")
        
        # Insertar configuraciones por defecto
        self._insert_default_settings()
        
    def _insert_default_settings(self):
        """Inserta configuraciones por defecto si no existen"""
        session = self.config.get_session()
        try:
            default_settings = [
                ('app_version', '1.2.0', 'Versión de la aplicación'),
                ('max_file_size', '52428800', 'Tamaño máximo de archivo en bytes'),
                ('auto_backup', 'true', 'Backup automático habilitado'),
                ('backup_frequency', '7', 'Frecuencia de backup en días'),
                ('max_history_records', '1000', 'Máximo de registros en historial'),
                ('default_export_format', 'excel', 'Formato de exportación por defecto'),
                ('theme', 'light', 'Tema de la aplicación'),
                ('language', 'es', 'Idioma de la aplicación'),
                ('auto_save_comparisons', 'true', 'Guardar comparaciones automáticamente'),
                ('notification_enabled', 'true', 'Notificaciones habilitadas'),
                ('cleanup_temp_files', 'true', 'Limpiar archivos temporales automáticamente'),
                ('max_temp_file_age', '24', 'Edad máxima de archivos temporales en horas')
            ]
            
            for key, value, description in default_settings:
                existing = session.query(AppSetting).filter(AppSetting.key == key).first()
                if not existing:
                    setting = AppSetting(key=key, value=value, description=description)
                    session.add(setting)
            
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error al insertar configuraciones por defecto: {e}")
        finally:
            session.close()

    # Métodos para archivos de referencia
    def add_reference_file(self, file_data: Dict[str, Any]) -> int:
        """Agrega un archivo de referencia a la biblioteca"""
        session = self.config.get_session()
        try:
            # Verificar si ya existe un archivo con el mismo checksum
            if file_data.get('checksum'):
                existing = session.query(ReferenceFile).filter(
                    ReferenceFile.checksum == file_data['checksum'],
                    ReferenceFile.is_active == True
                ).first()
                
                if existing:
                    raise ValueError(f"Ya existe un archivo idéntico: {existing.name}")
            
            reference_file = ReferenceFile(
                name=file_data['name'],
                original_name=file_data['original_name'],
                file_path=file_data['file_path'],
                file_size=file_data['file_size'],
                mime_type=file_data['mime_type'],
                row_count=file_data.get('row_count', 0),
                column_count=file_data.get('column_count', 0),
                description=file_data.get('description'),
                tags=','.join(file_data.get('tags', [])) if file_data.get('tags') else None,
                checksum=file_data.get('checksum')
            )
            
            session.add(reference_file)
            session.commit()
            
            file_id = reference_file.id
            
            # Log de actividad
            self.log_activity(
                session,
                'REFERENCE_ADDED',
                f'Archivo de referencia agregado: {file_data["name"]}',
                file_data['name'],
                True
            )
            
            return file_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error al agregar archivo de referencia: {e}")
            raise
        finally:
            session.close()

    def get_reference_files(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtiene la lista de archivos de referencia"""
        session = self.config.get_session()
        try:
            query = session.query(ReferenceFile)
            
            if not include_inactive:
                query = query.filter(ReferenceFile.is_active == True)
            
            files = query.order_by(desc(ReferenceFile.upload_date)).all()
            return [file.to_dict() for file in files]
            
        except Exception as e:
            logger.error(f"Error al obtener archivos de referencia: {e}")
            return []
        finally:
            session.close()

    def get_reference_file(self, file_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un archivo de referencia específico"""
        session = self.config.get_session()
        try:
            file = session.query(ReferenceFile).filter(
                ReferenceFile.id == file_id,
                ReferenceFile.is_active == True
            ).first()
            
            return file.to_dict() if file else None
            
        except Exception as e:
            logger.error(f"Error al obtener archivo de referencia {file_id}: {e}")
            return None
        finally:
            session.close()

    def update_reference_file_usage(self, file_id: int) -> bool:
        """Actualiza el contador de uso de un archivo de referencia"""
        session = self.config.get_session()
        try:
            file = session.query(ReferenceFile).filter(ReferenceFile.id == file_id).first()
            if file:
                file.last_used = datetime.utcnow()
                file.usage_count += 1
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error al actualizar uso del archivo {file_id}: {e}")
            return False
        finally:
            session.close()

    def delete_reference_file(self, file_id: int) -> bool:
        """Marca un archivo de referencia como inactivo"""
        session = self.config.get_session()
        try:
            file = session.query(ReferenceFile).filter(ReferenceFile.id == file_id).first()
            if file:
                file.is_active = False
                session.commit()
                
                # Log de actividad
                self.log_activity(
                    session,
                    'REFERENCE_DELETED',
                    f'Archivo de referencia eliminado: {file.name}',
                    file.name,
                    True
                )
                
                return True
            return False
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error al eliminar archivo de referencia {file_id}: {e}")
            return False
        finally:
            session.close()

    # Métodos para comparaciones
    def save_comparison(self, comparison_data: Dict[str, Any]) -> int:
        """Guarda el resultado de una comparación"""
        session = self.config.get_session()
        try:
            comparison = Comparison(
                reference_file_id=comparison_data.get('reference_file_id'),
                compare_file_name=comparison_data['compare_file_name'],
                compare_file_path=comparison_data.get('compare_file_path'),
                compare_file_size=comparison_data.get('compare_file_size'),
                processing_time=comparison_data['processing_time'],
                total_differences=comparison_data['total_differences'],
                modified_cells=comparison_data.get('modified_cells', 0),
                added_rows=comparison_data.get('added_rows', 0),
                removed_rows=comparison_data.get('removed_rows', 0),
                added_columns=comparison_data.get('added_columns', 0),
                removed_columns=comparison_data.get('removed_columns', 0),
                unique_in_reference=comparison_data.get('unique_in_reference', 0),
                unique_in_compare=comparison_data.get('unique_in_compare', 0),
                identical=comparison_data['identical'],
                result_data=json.dumps(comparison_data['result_data']),
                summary_data=json.dumps(comparison_data.get('summary_data', {})),
                notes=comparison_data.get('notes')
            )
            
            session.add(comparison)
            session.commit()
            
            comparison_id = comparison.id
            
            # Actualizar uso del archivo de referencia
            if comparison_data.get('reference_file_id'):
                self.update_reference_file_usage(comparison_data['reference_file_id'])
            
            # Log de actividad
            self.log_activity(
                session,
                'COMPARISON_SAVED',
                f'Comparación guardada: {comparison_data["compare_file_name"]}',
                comparison_data['compare_file_name'],
                True
            )
            
            return comparison_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error al guardar comparación: {e}")
            raise
        finally:
            session.close()

    def get_comparison_history(self, limit: int = 50, offset: int = 0, 
                             reference_file_id: int = None) -> List[Dict[str, Any]]:
        """Obtiene el historial de comparaciones"""
        session = self.config.get_session()
        try:
            query = session.query(Comparison).join(
                ReferenceFile, 
                Comparison.reference_file_id == ReferenceFile.id,
                isouter=True
            )
            
            if reference_file_id:
                query = query.filter(Comparison.reference_file_id == reference_file_id)
            
            comparisons = query.order_by(desc(Comparison.comparison_date)).offset(offset).limit(limit).all()
            
            result = []
            for comp in comparisons:
                comp_dict = comp.to_dict(include_data=False)
                if comp.reference_file:
                    comp_dict['reference_file_name'] = comp.reference_file.name
                    comp_dict['reference_original_name'] = comp.reference_file.original_name
                result.append(comp_dict)
            
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener historial de comparaciones: {e}")
            return []
        finally:
            session.close()

    def get_comparison_details(self, comparison_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene los detalles completos de una comparación"""
        session = self.config.get_session()
        try:
            comparison = session.query(Comparison).filter(Comparison.id == comparison_id).first()
            
            if not comparison:
                return None
            
            result = comparison.to_dict(include_data=True)
            
            if comparison.reference_file:
                result['reference_file_name'] = comparison.reference_file.name
                result['reference_original_name'] = comparison.reference_file.original_name
                result['reference_file_path'] = comparison.reference_file.file_path
            
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener detalles de comparación {comparison_id}: {e}")
            return None
        finally:
            session.close()

    def mark_comparison_as_exported(self, comparison_id: int, export_format: str) -> bool:
        """Marca una comparación como exportada"""
        session = self.config.get_session()
        try:
            comparison = session.query(Comparison).filter(Comparison.id == comparison_id).first()
            if comparison:
                comparison.exported = True
                comparison.export_format = export_format
                comparison.export_date = datetime.utcnow()
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error al marcar comparación como exportada {comparison_id}: {e}")
            return False
        finally:
            session.close()

    # Métodos para configuraciones
    def get_setting(self, key: str) -> Optional[str]:
        """Obtiene el valor de una configuración"""
        session = self.config.get_session()
        try:
            setting = session.query(AppSetting).filter(AppSetting.key == key).first()
            return setting.value if setting else None
            
        except Exception as e:
            logger.error(f"Error al obtener configuración {key}: {e}")
            return None
        finally:
            session.close()

    def set_setting(self, key: str, value: str, description: str = None) -> bool:
        """Establece el valor de una configuración"""
        session = self.config.get_session()
        try:
            setting = session.query(AppSetting).filter(AppSetting.key == key).first()
            
            if setting:
                setting.value = value
                setting.updated_date = datetime.utcnow()
                if description:
                    setting.description = description
            else:
                setting = AppSetting(key=key, value=value, description=description)
                session.add(setting)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error al establecer configuración {key}: {e}")
            return False
        finally:
            session.close()

    def get_all_settings(self) -> List[Dict[str, Any]]:
        """Obtiene todas las configuraciones"""
        session = self.config.get_session()
        try:
            settings = session.query(AppSetting).order_by(AppSetting.key).all()
            return [setting.to_dict() for setting in settings]
            
        except Exception as e:
            logger.error(f"Error al obtener todas las configuraciones: {e}")
            return []
        finally:
            session.close()

    # Métodos para logs de actividad
    def log_activity(self, session: Session, action: str, details: str = None, 
                    file_name: str = None, success: bool = True, error_message: str = None):
        """Registra una actividad en el log"""
        try:
            log = ActivityLog(
                action=action,
                details=details,
                file_name=file_name,
                success=success,
                error_message=error_message
            )
            session.add(log)
            # No hacer commit aquí, se hará en la transacción principal
            
        except Exception as e:
            logger.error(f"Error al registrar actividad: {e}")

    def get_activity_logs(self, limit: int = 100, offset: int = 0, 
                         action_filter: str = None) -> List[Dict[str, Any]]:
        """Obtiene los logs de actividad"""
        session = self.config.get_session()
        try:
            query = session.query(ActivityLog)
            
            if action_filter:
                query = query.filter(ActivityLog.action.like(f'%{action_filter}%'))
            
            logs = query.order_by(desc(ActivityLog.timestamp)).offset(offset).limit(limit).all()
            return [log.to_dict() for log in logs]
            
        except Exception as e:
            logger.error(f"Error al obtener logs de actividad: {e}")
            return []
        finally:
            session.close()

    # Métodos de estadísticas y mantenimiento
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la aplicación"""
        session = self.config.get_session()
        try:
            stats = {}
            
            # Contadores básicos
            stats['total_reference_files'] = session.query(ReferenceFile).filter(ReferenceFile.is_active == True).count()
            stats['total_comparisons'] = session.query(Comparison).count()
            stats['identical_comparisons'] = session.query(Comparison).filter(Comparison.identical == True).count()
            stats['different_comparisons'] = session.query(Comparison).filter(Comparison.identical == False).count()
            
            # Tiempo promedio de procesamiento
            avg_time = session.query(func.avg(Comparison.processing_time)).scalar()
            stats['avg_processing_time'] = float(avg_time) if avg_time else 0.0
            
            # Total de diferencias encontradas
            total_diffs = session.query(func.sum(Comparison.total_differences)).scalar()
            stats['total_differences_found'] = int(total_diffs) if total_diffs else 0
            
            # Archivo de referencia más usado
            most_used = session.query(ReferenceFile).filter(ReferenceFile.is_active == True).order_by(desc(ReferenceFile.usage_count)).first()
            stats['most_used_reference'] = most_used.name if most_used else 'N/A'
            stats['most_used_reference_count'] = most_used.usage_count if most_used else 0
            
            # Última comparación
            last_comparison = session.query(Comparison).order_by(desc(Comparison.comparison_date)).first()
            stats['last_comparison'] = last_comparison.comparison_date.isoformat() if last_comparison else None
            
            # Comparaciones por mes (últimos 6 meses)
            six_months_ago = datetime.utcnow() - timedelta(days=180)
            monthly_stats = session.query(
                func.strftime('%Y-%m', Comparison.comparison_date).label('month'),
                func.count(Comparison.id).label('count')
            ).filter(
                Comparison.comparison_date >= six_months_ago
            ).group_by('month').order_by('month').all()
            
            stats['monthly_comparisons'] = [{'month': month, 'count': count} for month, count in monthly_stats]
            
            return stats
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {e}")
            return {}
        finally:
            session.close()

    def cleanup_old_data(self, days_to_keep: int = 30) -> bool:
        """Limpia datos antiguos de la base de datos"""
        session = self.config.get_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            # Limpiar logs antiguos
            deleted_logs = session.query(ActivityLog).filter(
                ActivityLog.timestamp < cutoff_date
            ).delete()
            # Limpiar comparaciones muy antiguas si hay demasiadas
            total_comparisons = session.query(Comparison).count()
            if total_comparisons > 1000:
                old_comparisons = session.query(Comparison).filter(
                    Comparison.comparison_date < cutoff_date
                ).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error al limpiar datos antiguos: {e}")
            return False
        finally:
            session.close()