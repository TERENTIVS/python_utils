import sys
from importlib.machinery import ModuleSpec
from importlib.machinery import all_suffixes as module_suffixes
from importlib.util import spec_from_file_location
from itertools import chain
from pathlib import Path

MAPPING = {}
NAMESPACES = {}
PATH_PLACEHOLDER = '__editable__.sklearnutils-0.1.0.finder' + ".__path_hook__"


class _EditableFinder:  # MetaPathFinder
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        for pkg, pkg_path in reversed(list(MAPPING.items())):
            if fullname == pkg or fullname.startswith(f"{pkg}."):
                rest = fullname.replace(pkg, "", 1).strip(".").split(".")
                return cls._find_spec(fullname, Path(pkg_path, *rest))

        return None

    @classmethod
    def _find_spec(cls, fullname, candidate_path):
        init = candidate_path / "__init__.py"
        candidates = (candidate_path.with_suffix(x) for x in module_suffixes())
        for candidate in chain([init], candidates):
            if candidate.exists():
                return spec_from_file_location(fullname, candidate)


class _EditableNamespaceFinder:  # PathEntryFinder
    @classmethod
    def _path_hook(cls, path):
        if path == PATH_PLACEHOLDER:
            return cls
        raise ImportError

    @classmethod
    def _paths(cls, fullname):
        # Ensure __path__ is not empty for the spec to be considered a namespace.
        return NAMESPACES[fullname] or MAPPING.get(fullname) or [PATH_PLACEHOLDER]

    @classmethod
    def find_spec(cls, fullname, target=None):
        if fullname in NAMESPACES:
            spec = ModuleSpec(fullname, None, is_package=True)
            spec.submodule_search_locations = cls._paths(fullname)
            return spec
        return None

    @classmethod
    def find_module(cls, fullname):
        return None


def install():
    if not any(finder == _EditableFinder for finder in sys.meta_path):
        sys.meta_path.append(_EditableFinder)

    if not NAMESPACES:
        return

    if not any(hook == _EditableNamespaceFinder._path_hook for hook in sys.path_hooks):
        # PathEntryFinder is needed to create NamespaceSpec without private APIS
        sys.path_hooks.append(_EditableNamespaceFinder._path_hook)
    if PATH_PLACEHOLDER not in sys.path:
        sys.path.append(PATH_PLACEHOLDER)  # Used just to trigger the path hook