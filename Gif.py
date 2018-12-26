import threading
from time import sleep
# Import Tkinter depending on the Python version
try:
    import Tkinter as tk
except:
    import tkinter as tk

class Gif (tk.Label):

	def __init__(self, root, gif):
		# Initialize Label
		tk.Label.__init__(self, root)
		# Set gif
		self._img  = tk.PhotoImage(file=gif)
		self.image = self._img
		self.configure(image=self._img)


	# Call this method to start the animation of the gif
	def animate(self, threaded=True, interval=150, n_repeats=-1):
		self.n_repeats = n_repeats

		if threaded:
			animator = threading.Thread(
									target = self._play_gif, 
									args = (interval, ))
			animator.start()
		else:
			self._play_gif(interval)
		

	def _play_gif(self, interval):
		# Preparing animation
		self.configure(image=self._img) 
		self.frame = 0
		self.repeats = 0
		sleep(interval)
		self._next_frame(interval)
            
    # This method runs recursive till the number of repetitions
   	# is reaced
	def _next_frame(self, interval):
		try:
			# Setting the next frame of the gif
			opt = "GIF -index {}".format(self.frame)
			self._img.configure(format=opt)
		except tk.TclError:
			# A TclError indicates that the maximum number of frames
			# has been reached
			self.frame = 0
			self.repeats += 1
			# In case the number of repeats has been set to a positive 
			# number check if the number of repeats has been exceded.
			if (self.repeats >= self.n_repeats and self.n_repeats > 0):
				opt = "GIF -index {}".format(0)
				self._img.configure(format=opt)
				return
			else:
				# Restart animation
				self._next_frame(interval)
				return
 		
 		# Go to next frame and wait for interval to show next frame
		self.frame += 1
		self.after(interval, self._next_frame, interval)
