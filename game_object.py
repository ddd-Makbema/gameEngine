
import pygame
from data_types import Vector2D
from exceptions import SpriteNameError
import os
import math

class GameObject():
	"""Allows calling of user made packages amd inter-file communication 
 of instance variables.

	Auto imports files from data specified by when creating each instance 
	of game object. It allows communication between different game 
	objects in all files as well as overridable functions such as Update
	for each user made package.

	Attributes:
 		INSTANCES: list of all instances of game objects
   		NAMES: list of each user defined name for the game objects
	 	GAME_OBJECTS: dictionary keying the name of game objects to the instance
   		sprite: a string containing the name of the image from the data file
	 	screen: default value contains the instance of the pygame screen defined in main
   		transform: contains the Vector2D(x,y) screen coords for the image to be loaded
	 	scale: contains the Vector2D(x,y) scale amount with 1 being default pixel size
	 	rotation: contains a int of the degrees to rotate the image from up and down
   		parent: string with the name of the game object to inherit Transform from.
   		packages: a list of strings for file names you want to import
		last_scale: int of scale from last frame to reduce operations per frame
		last_parent_scale: int same as last_scale but for the parent object if there is one
		image_start: screen image of the sprite entered with 0 rotation and 1 scale modified each frame.
		package_instances: list of instances of classes loaded from packages entered in args
		packages_import: temporary list of imported packages from scripts folder to be instantiated
"""
	INSTANCES = []
	NAMES = []
	GAME_OBJECTS = {}

	def __init__(self, name ,screen, sprite="null.png", parent=None, *args):
		"""Initializes game object and adds the instance to all the lists"""
		self.sprite = "data/" + sprite #data/ is to pull the image files from the data folder
		self.screen = screen 
		self.packages = args
		self.parent = parent
		self.name = name
		self.image_start = None

		self.package_instances = [] 
		self.packages_import = []
		GameObject.NAMES.append(name) 
		GameObject.INSTANCES.append(self) 
		GameObject.GAME_OBJECTS[self.name] = self

		#makes sure there can not be two conflicting names.
		if name in GameObject.NAMES:
			i = 1
			while name in GameObject.NAMES:
				name = name + f"({i})"
				i += 1
		
		

	def start(self):
		"""Initializes the sprite as an object and imports all packages needed. And calls the start funtions for them."""

		self.image_start = _pyLoad(self.sprite)

		#initializes the parent instance if one was entered
		if self.parent:
			self.parent_instance = GameObject.GAME_OBJECTS[self.parent]
		else:
			self.parent_instance = None

		#initializes the packages for the game object
		for script in self.packages:
			full_module_name = "scripts." + script
			self.packages_import.append(self._import_class_from_string(full_module_name))
		for pack in self.packages_import:
			self.package_instances.append(pack(self))

		#calls the start function for all packages if they have them
		for p in self.package_instances:
			try:
				p.Start()
			except AttributeError:
				pass
		return


	def update(self):
		"""Called for each game object each frame from main. Calls the update 
  			function for all packages imported. Scales and Rotates 
	 the game object as needed."""

		#calls the update function for all packages if they have them
		for p in self.package_instances:
			try:
				p.update()
			except AttributeError:
				pass
		return
		
	def fixed_update(self):
		"""Same as update but for fixed update: physics calculations"""

		#calls the fixed update function for all packages if they have them
		for p in self.package_instances:
			try:
				p.fixed_update()
			except AttributeError:
				pass
		return

	
	def _import_class_from_string(self, string_name):
		"""Given a string like 'module.submodule.func_name' which refers to a 	function, return that function so it can be called
 		Returns:
  			instance of the package imported from the string"""

		mod_name, func_name = string_name.rsplit(".", 1)
		mod = __import__(mod_name)

		for i in mod_name.split(".")[1:]:
			mod = getattr(mod, i)
		return getattr(mod, func_name)

def _pyLoad(sprite_to_load):
	"""Shorter function to load and return a pygame image type variable while 
 		also calling a more descriptive exception if the sprite doesn't exist."""
		
	if not (os.path.exists(sprite_to_load)):
		raise SpriteNameError(sprite_to_load.strip("data/"))
	return pygame.image.load(sprite_to_load).convert_alpha()