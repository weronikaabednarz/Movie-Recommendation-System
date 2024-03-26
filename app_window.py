import tkinter as tk

window = tk.Tk()
window.title("Movie Recommendation System")
window.geometry('640x360')

background_image = tk.PhotoImage(file="cinema.png")
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)       # 0,0 - lewy górny róg; width, height - szerokość i wysokość etykiety będą równe
# szerokości i wysokości okna głównego, co oznacza, że etykieta będzie w pełni zajmować obszar okna.


movie_name_label = tk.Label(window, text="Entry movie title:", bg="#f3f6fb", fg="#000000")
movie_name_label.grid(row=0, column=0, padx = 50, pady = 45) 

movie_name_entry = tk.Entry(window, width = 50)
movie_name_entry.grid(row=0, column=1, padx = 10)

searching_button = tk.Button(window, text = "Search", bg="#f3f6fb", fg="#000000")
searching_button.grid(row = 0, column = 3, padx = 10, pady = 45)

# Label do wyświetlania wyników operacji
result_name_label = tk.Label(window, text="Recommended movies:", bg="#f3f6fb", fg="#000000")
result_name_label.grid(row=1, column=0, sticky="n")

result_text = tk.Text(window, width=38, height=7.5)  # Ustawienia szerokości i wysokości pola tekstowego
result_text.grid(row=1, column=1, sticky="n")

window.mainloop()