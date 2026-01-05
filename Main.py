from UnipyEngine import *

# Charge tous les scripts custom
Engine.LoadScripts("Assets")

# Enregistrer les modules
ModuleManagement.ModuleManager.register_all_modules()

Engine.Init(900, 900, color=Color(54, 215, 247), renderCollider=True)

# Chargement de la scène
SceneManager.LoadScene("Game")

Engine.Run()