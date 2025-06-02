import json
import os
from typing import Dict, Any, Optional


class GBStandardConfig:
    """GB标准配置管理类 - 单例模式"""
    
    _instance: Optional['GBStandardConfig'] = None
    _config: Optional[Dict[str, Any]] = None
    
    def __new__(cls, config_file: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config_file: str = None):
        if self._config is None:
            if config_file is None:
                # 默认配置文件路径
                current_dir = os.path.dirname(os.path.abspath(__file__))
                config_file = os.path.join(current_dir, 'gb_standards.json')
            
            self._config = self._load_config(config_file)
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件未找到: {config_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件格式错误: {e}")
    
    def get_line_type(self, line_type: str) -> Optional[Dict[str, Any]]:
        """获取线型配置"""
        return self._config.get('line_types', {}).get(line_type)
    
    def get_layer_mapping(self, logical_layer: str) -> str:
        """获取图层映射"""
        return self._config.get('layer_mapping', {}).get(logical_layer, logical_layer)
    
    def get_line_weight(self, weight_type: str) -> Optional[float]:
        """获取线宽配置"""
        return self._config.get('line_weights', {}).get(weight_type)
    
    def get_text_height(self, height_type: str) -> Optional[float]:
        """获取文字高度配置"""
        return self._config.get('text_heights', {}).get(height_type)
    
    def get_arrow_size(self) -> float:
        """获取箭头尺寸"""
        return self._config.get('arrow_size', 3.0)
    
    def get_font_style(self) -> str:
        """获取字体样式"""
        return self._config.get('font_style', 'chinese')
    
    def get_scales(self) -> list:
        """获取标准比例列表"""
        return self._config.get('scales', [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000])
    
    def get_all_line_types(self) -> Dict[str, Dict[str, Any]]:
        """获取所有线型配置"""
        return self._config.get('line_types', {})
    
    def get_all_layer_mappings(self) -> Dict[str, str]:
        """获取所有图层映射"""
        return self._config.get('layer_mapping', {})
    
    def reload_config(self, config_file: str = None):
        """重新加载配置文件"""
        if config_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(current_dir, 'gb_standards.json')
        
        self._config = self._load_config(config_file) 