import json
import os
from typing import Dict, Any, List

class MapManager:
    _instance = None
    MAPS_DIR = './assets/maps/'
    NESESSARY_FILES = ['nav.json', 'view.json']
    _maps: Dict[str, Dict[str, Any]] = {}
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MapManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    @classmethod
    def _initialize(cls):
        """Инициализирует менеджер (вызывается автоматически при первом использовании)"""
        if not cls._initialized:
            cls._load_all_maps()
            cls._initialized = True
    
    @classmethod
    def _load_all_maps(cls):
        """Загружает все карты из директории"""
        cls._maps.clear()
    
        if not os.path.exists(cls.MAPS_DIR):
            os.makedirs(cls.MAPS_DIR, exist_ok=True)
            return

        # Получаем список поддиректорий с картами
        maps_dirs = [
            d for d in os.listdir(cls.MAPS_DIR) 
            if os.path.isdir(os.path.join(cls.MAPS_DIR, d))
        ]
        
        for map_dir in maps_dirs:
            map_path = os.path.join(cls.MAPS_DIR, map_dir)
            
            # Проверяем наличие всех необходимых файлов
            has_all_files = all(
                os.path.exists(os.path.join(map_path, file))
                for file in cls.NESESSARY_FILES
            )
            
            if not has_all_files:
                continue  # Пропускаем директории с неполным набором файлов
            
            # Загружаем данные из файлов
            map_data = {}
            try:
                for file in cls.NESESSARY_FILES:
                    with open(os.path.join(map_path, file), 'r', encoding='utf-8') as f:
                        key = os.path.splitext(file)[0]  # 'nav' или 'view'
                        map_data[key] = json.load(f)
                
                # Сохраняем данные карты под именем директории
                cls._maps[map_dir] = map_data
                
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка загрузки карты {map_dir}: {str(e)}")
                continue
    
    @staticmethod
    def get_available_maps() -> List[str]:
        """Возвращает список доступных карт"""
        MapManager._initialize()
        return list(MapManager._maps.keys())
    
    @staticmethod
    def get_map(map_name: str) -> Dict[str, Any]:
        """
        Возвращает данные карты по имени
        :param map_name: Название карты (без расширения)
        :raises KeyError: Если карта не существует
        """
        MapManager._initialize()
        
        if map_name not in MapManager._maps:
            available = MapManager.get_available_maps()
            raise KeyError(f"Map '{map_name}' not found. Available maps: {available}")
        
        return MapManager._maps[map_name]
    
    @staticmethod
    def reload_maps():
        """Перезагружает все карты из файлов"""
        MapManager._load_all_maps()