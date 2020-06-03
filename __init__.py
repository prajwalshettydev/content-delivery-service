import importlib
import sys
import os


allModules = ['main', 'config', 'twitterservice.tweet','googleservice.gsheet']
# modulesFullNames = {}


# for currentModuleName in allModules:
#     if 'DEBUG_MODE' in sys.argv:
#         modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
#     else:
#         modulesFullNames[currentModuleName] = (
#             '{}.{}'.format(__name__, currentModuleName))

# for currentModuleFullName in modulesFullNames.values():
#     if currentModuleFullName in sys.modules:
#         importlib.reload(sys.modules[currentModuleFullName])
#     else:
#         globals()[currentModuleFullName] = importlib.import_module(
#             currentModuleFullName)
#         setattr(globals()[currentModuleFullName],
#                 'modulesNames', modulesFullNames)

