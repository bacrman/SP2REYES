from ShowDb import ShowDb
from ShowGuiCtk import ShowGuiCtk

def main():
    db = ShowDb(init=False, dbName='ShowDb.csv')
    app = ShowGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()