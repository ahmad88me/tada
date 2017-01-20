
#The below two lines is to resolve the conflict of Tkinter with matplotlib
import matplotlib
matplotlib.use("TkAgg")


from kmeans_examples import dbscan_test, iris_test, sklean_example_text
import fcm_examples
#sklean_example_text()
#dbscan_test()
#iris_test()
#fcm_examples.sklean_example_text()
fcm_examples.dbscan_test()
#fcm_examples.iris_test()
#fcm_examples.example1()

# it works but doesn't wait for the image to be constructed
# import Tkinter
# root = Tkinter.Tk()
# photo = Tkinter.PhotoImage(file = "test.gif")
# label = Tkinter.Label(image = photo)
# label.pack()
# root.mainloop()
