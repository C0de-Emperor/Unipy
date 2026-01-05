class ModuleType:
    """Classe de base pour typer les modules"""
    registry = {}
    
    def __init__(self, name, module_type):
        self.name = name
        self.module_type = module_type
        self.module = None
        ModuleType.registry[(module_type, name)] = self
    
    def set_module(self, module):
        if self.module is None:
            self.module = module

class Scene(ModuleType):
    """Classe pour définir une scène"""
    def __init__(self, name):
        super().__init__(name, "scene")

class Script(ModuleType):
    """Classe pour définir un script"""
    def __init__(self, name):
        super().__init__(name, "script")

class ModuleManager:
    @staticmethod
    def find_module(module_type, name):
        """Trouve un module par type et nom"""
        obj = ModuleType.registry.get((module_type, name))
        return obj.module if obj else None
    
    @staticmethod
    def get_modules_by_type(module_type):
        """Retourne tous les modules d'un type donné"""
        return [obj.module for (t, n), obj in ModuleType.registry.items() if t == module_type and obj.module]
    
    @staticmethod
    def register_all_modules():
        """Enregistre tous les ModuleType dans les modules importés"""
        import os
        import importlib
        import sys
        from UnipyEngine.Utils import Debug
        
        # Charger tous les modules Assets
        for root, dirs, files in os.walk('Assets'):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    rel_path = os.path.relpath(root, 'Assets')
                    if rel_path == '.':
                        mod_name = f'Assets.{os.path.splitext(file)[0]}'
                    else:
                        mod_name = f'Assets.{rel_path.replace(os.sep, ".")}.{os.path.splitext(file)[0]}'
                    try:
                        importlib.import_module(mod_name)
                    except ImportError:
                        pass
        
        for module_name, module in sys.modules.items():
            if module_name.startswith('Assets') and not hasattr(module, '__path__'):
                for attr_name in dir(module):
                    attr = getattr(module, attr_name, None)
                    if isinstance(attr, ModuleType):
                        attr.set_module(module)
                        Debug.LogRegistry(f"Registered {attr_name} '{attr.name}' in {module_name}")
