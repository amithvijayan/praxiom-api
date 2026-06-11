import importlib
import pkgutil
import inspect
from typing import Dict, Any, Type

class EngineRegistry:
    """
    The Universal Registry for all Praxiom Zero-Hallucination Mathematics and Physics Engines.
    """
    _engines: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register an engine class."""
        def wrapper(engine_class):
            cls._engines[name] = engine_class()
            return engine_class
        return wrapper

    @classmethod
    def get_engine(cls, name: str) -> Any:
        if name not in cls._engines:
            raise ValueError(f"Engine '{name}' is not registered in the Praxiom Universe.")
        return cls._engines[name]

    @classmethod
    def list_engines(cls) -> list:
        return list(cls._engines.keys())

    @classmethod
    def execute(cls, engine_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a registered engine with the provided parameters.
        This is where the deterministic math happens.
        """
        engine = cls.get_engine(engine_name)
        return engine.calculate(**parameters)

    @classmethod
    def get_gemini_tools(cls) -> list:
        """
        Dynamically generates a list of functions that Gemini can use as tools,
        based on the registered engines.
        """
        tools = []
        for name, engine_instance in cls._engines.items():
            calc_method = getattr(engine_instance, "calculate")
            sig = inspect.signature(calc_method)
            
            params = []
            for param_name, param in sig.parameters.items():
                if param_name == 'self': continue
                annot = param.annotation.__name__ if hasattr(param.annotation, '__name__') else "float"
                if param.default != inspect.Parameter.empty:
                    params.append(f"{param_name}: {annot} = {repr(param.default)}")
                else:
                    params.append(f"{param_name}: {annot}")
            
            sig_str = ", ".join(params)
            func_name = f"execute_{name}"
            doc_str = engine_instance.__doc__ or f"Execute {name}"
            
            # Using exec to create a function with a physical signature so the SDK extracts it flawlessly
            code = f'''
def {func_name}({sig_str}):
    """{doc_str}"""
    # Remove _cls from locals to just get the arguments
    args = locals().copy()
    return _cls.execute("{name}", args)
'''
            namespace = {"_cls": cls}
            exec(code, namespace)
            tools.append(namespace[func_name])
            
        return tools
