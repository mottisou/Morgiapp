from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from tkinter import StringVar, IntVar

dropDownData = [
    {
    "name": "Chest",
    "link": "https://www.strengthlog.com/chest-exercises/",
    "Exercises": {
        "chest press": "https://www.muscleandstrength.com/exercises/dumbbell-bench-press.html",
        "incline chest press": "https://www.muscleandstrength.com/exercises/incline-dumbbell-bench-press.html",
        "Chest Fly": "https://www.muscleandstrength.com/exercises/cable-crossovers-%28mid-chest%29.html"
    }
},
    {
    "name": "Back",
    "link": "https://www.strengthlog.com/back-exercises/",
    "Exercises": {
        "Lat Pulldown": "https://www.muscleandstrength.com/exercises/lat-pull-down.html",
        "pull-ups": "https://www.muscleandstrength.com/exercises/wide-grip-pull-up.html",
        "Chin-Up":"https://www.muscleandstrength.com/exercises/chin-up.html"
    }
},
{
    "name": "Shoulders",
    "link": "https://www.strengthlog.com/shoulder-exercises/",
    "Exercises": {
        "Shoulder Press": "https://www.muscleandstrength.com/exercises/seated-dumbbell-press.html",
        "Upright Row":"https://www.muscleandstrength.com/exercises/cable-upright-row.html"    
    }
}
]

class App(tb.Window):
    def __init__(self, size):
        super().__init__(title="MorgiApp", themename="litera")
        # Set the window size
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - size[1] / 2)
        position_right = int(screen_width / 2 - size[0] / 2)
        self.geometry(f"+{position_right}+{position_top}")

        self.table_frame = tableFrame(self)
        self.table_frame.pack(padx=10, pady=10)


        self.mainloop()
    
class PlaceholderEntry(tb.Entry):
    def __init__(self, container, placeholder, **kwargs):
        super().__init__(container, **kwargs)
        self.placeholder = placeholder
        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, END)

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)


class tableFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent,padding=3, style='light.TFrame')
        self.grid_columnconfigure(0, weight=1)
        for col in range(1, 7):
            self.grid_columnconfigure(col, weight=1)
        
        self.workout_name_entry = PlaceholderEntry(self, "Please Type Workout Name", style='info.TEntry')
        self.workout_name_entry.grid(row=0, column=2, columnspan=4, sticky='ews', padx=5, pady=0.5)

        self.create_header_row()
        self.rows = []
        for _ in range(3):
            self.add_row()
        
        self.add_row_button = tb.Button(self, text="Add Row", command=self.add_row, style="success.TButton",width=5)
        self.add_row_button.grid(row=0, column=6, sticky="ew", padx=5)

        self.del_row_button = tb.Button(self, text="Del Row", command=self.delete_row, style="danger.TButton",width=5)
        self.del_row_button.grid(row=0, column=7, sticky="ew", padx=5)




    def create_header_row(self):
        headers = ["Muscle", "Exercise", "Equipment Required", "Body Poses", "Sets", "Rep"]
        tableLatter =[]

        #widgets
        letter_Lable = tb.Label(self, text="A", font=("Arial", 10, 'bold'), style="secondary.Inverse.TLabel",width=8, anchor="center")
        musle_label = tb.Label(self, text="Muscle", font=("Arial", 10, 'bold'), style="warning.Inverse.TLabel",width=12,anchor="center")
        exercise_label = tb.Label(self, text="Exercise", font=("Arial", 10, 'bold'), style="Primary.Inverse.TLabel",width=15, anchor="center")
        equipment_label = tb.Label(self, text="Equipment Required", font=("Arial", 10, 'bold'), style="Primary.Inverse.TLabel", width=25, anchor="center")
        body_label = tb.Label(self, text="Body Poses", font=("Arial", 10, 'bold'), style="Primary.Inverse.TLabel", width=15, anchor="center")
        Sets_label = tb.Label(self, text="Sets", font=("Arial", 10, 'bold'), style="warning.Inverse.TLabel", width=10, anchor="center")
        rep_label = tb.Label(self, text="Rep", font=("Arial", 10, 'bold'), style="warning.Inverse.TLabel", width=10, anchor="center")
        
        #placement
        letter_Lable.grid(row=1, column=0, sticky="news")
        musle_label.grid(row=1, column=1, sticky="news")
        exercise_label.grid(row=1, column=2, sticky="news")
        equipment_label.grid(row=1, column=3,columnspan=2, sticky="news")
        body_label.grid(row=1, column=5, sticky="news")
        Sets_label.grid(row=1, column=6, sticky="news")
        rep_label.grid(row=1, column=7, sticky="news")
        

    def add_row(self):
        row_number = len(self.rows) + 2  
        muscles = [item["name"] for item in dropDownData]
        exercises = [exercise for item in dropDownData for exercise in item["Exercises"]] 
        row = WorkoutDataRow(self,row_number, muscles, exercises)
        row.grid(row=row_number, column=0, columnspan=8, sticky="ew", pady=1)
        self.rows.append(row)

    def delete_row(self):
        if len(self.rows) > 1:
            row = self.rows.pop()
            row.grid_forget()
            row.destroy()

    def createButtons(self):
        add_row_button = tb.Button(self, text="Add Row", command=self.add_row, style="success.TButton")
        add_row_button.grid(row=len(self.rows) + 2, column=4, sticky="ew")

        del_row_button = tb.Button(self, text="Del Row", command=self.delete_row, style="danger.TButton")
        del_row_button.grid(row=len(self.rows) + 2, column=5, sticky="ew") 


class WorkoutDataRow(tb.Frame):
    # Custom widgets
    class MuscleSelector(tb.Menubutton):
        def __init__(self, parent, muscles, exercise_selector=None):
            super().__init__(parent, text="Muscle",width=8)
            self.muscles = muscles
            self.exercise_selector = exercise_selector
            self.menu = Menu(self, tearoff=0)
            self["menu"] = self.menu
            for muscle in muscles:
                self.menu.add_command(label=muscle, command=lambda muscle=muscle: self.update_selection(muscle))

        def update_selection(self, muscle):
            muscle_data = next(item for item in dropDownData if item["name"] == muscle)
            exercises = list(muscle_data["Exercises"].keys())
            if self.exercise_selector:
                self.exercise_selector.update_exercises(exercises)
            self.configure(text=muscle)

    class ExerciseSelector(tb.Menubutton):
        def __init__(self, parent, exercises):
            super().__init__(parent, text="Exercise",width=10)
            self.exercises = exercises
            self.menu = Menu(self, tearoff=0)
            self["menu"] = self.menu
            for exercise in exercises:
                self.menu.add_command(label=exercise, command=lambda exercise=exercise: self.update_selection(exercise))

        def update_selection(self, exercise):
            self.configure(text=exercise)

        def update_exercises(self, exercises):
            self.menu.delete(0, 'end')
            for exercise in exercises:
                self.menu.add_command(label=exercise, command=lambda exercise=exercise: self.update_selection(exercise))

    class EquipmentSelector(tb.Menubutton):
        def __init__(self, parent):
            super().__init__(parent, text="Equipment", width=21)
            self.equipments = ["Barbell", "Dumbbell", "Cable","High Pulley","Low Pulley", "Machine", "Bodyweight", "Kettlebell", "Resistance Band", "None"]
            self.menu = Menu(self, tearoff=0)
            self["menu"] = self.menu
            for equipment in self.equipments:
                self.menu.add_command(label=equipment, command=lambda equipment=equipment: self.update_selection(equipment))

        def update_selection(self, equipment):
            self.configure(text=equipment)

    class BodyPoses(tb.Menubutton):
        def __init__(self, parent):
            super().__init__(parent, text="body poses", width=10)
            self.Poses = ["bench", "Seated", "Standing","Parelar","Incline", "Decline", "Bodyweight", "Kettlebell", "Resistance Band", "None"]
            self.menu = Menu(self, tearoff=0)
            self["menu"] = self.menu
            for pose in self.Poses:
                self.menu.add_command(label=pose, command=lambda pose=pose: self.update_selection(pose))

        def update_selection(self, pose):
            self.configure(text=pose)

    def __init__(self, parent,row_number,muscles, exercises):
        super().__init__(parent, padding=3, style='light.TFrame')
        self.grid(sticky="ew")

        # Row number
        self.row_number_label = tb.Label(self, text=str(row_number-1), width=8, anchor="center", style="dark.TLabel")
        self.row_number_label.grid(row=0, column=0, sticky="news")

        # Muscle selector
        self.Muscle_Selector = self.MuscleSelector(self, muscles)
        self.Muscle_Selector.grid(row=0, column=1, sticky='ew')

        # Exercise selector
        self.Exercise_Selector = self.ExerciseSelector(self, exercises)
        self.Exercise_Selector.grid(row=0, column=2, sticky='ew',padx=2)

        # Equipment selector
        self.Equipment_Selector = self.EquipmentSelector(self)
        self.Equipment_Selector.grid(row=0, column=3, sticky='ew',padx=2)

        # Body Poses selector
        self.Body_Poses = self.BodyPoses(self)
        self.Body_Poses.grid(row=0, column=4, sticky='ew',padx=2)

        # Sets Entry
        self.Sets_Entry = tb.Entry(self, width=10,justify="center")
        self.Sets_Entry.grid(row=0, column=5, sticky='ew',padx=2,)

        # Rep Entry
        self.Rep_Entry = tb.Entry(self, width=10,justify="center")
        self.Rep_Entry.grid(row=0, column=6, sticky='ew',padx=2)

        # Now that ExerciseSelector is created, pass it to MuscleSelector
        self.Muscle_Selector.exercise_selector = self.Exercise_Selector

    

App((800,1000))