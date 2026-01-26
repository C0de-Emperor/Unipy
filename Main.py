from UnipyEngine import *

# Charge tous les scripts custom
Engine.LoadScripts("Assets")

# Enregistrer les modules
ModuleManagement.ModuleManager.register_all_modules()

Engine.Init()

# Chargement de la scène initiale
SceneManager.LoadInitialScene()

Engine.Run()