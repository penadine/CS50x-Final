# Telegram bot for accounting of expenses
#### Video Demo:  <https://youtu.be/bgsPYW_0yYc>
#### Description:
Welcome to my final project.
My name is Nadiia Rychenko. I am from Kyiv, the capital of Ukraine.
The idea of my final project is to create a telegram bot for accounting of expenses, I used the python programming language to write this telegram bot.
The main menu consists of 4 main sections: Enter_the_type_of_expense, Enter_the_total_of_expense, View_entered_expenses and Help.
The first button of the Enter_the_type_of_expense is for entering the type of expenses, for example: food, clothing, credit, entertainment, etc. By clicking on which you can add an expense, edit its name, and also delete it.
With the Enter_the_total_of_expense button, you need to select the type of expense, then enter the total sum and select the month and year. You can also delete the total sum for some expense.
With the View_entered_expenses button, you can view all expenses, as well as by type of expenses and by date. You can also look at the graph for the expense for the entire period and for a specific month chart.
The Help button offers to watch a video of how to use the bot.
The main function of the bot is to control, store and display the archive of data on all costs. To correctly use the main function of the bot, you must first enter all types of costs that you want to record. This is done through the "Enter_the_type_of_expense" function, the button for which is displayed in the main menu. This feature also provides the ability to change the name of the expense type and remove the expense you do not need.
Also in the main menu there is a button "Enter_the_total_of_expense". This function is responsible for entering entries for individual expenses. To enter an entry, you need to specify the name of the expense, the date (year and month) and the total sum. You can also delete this entry if you entered incorrect data.
Finally, in the main menu you can click on the "View_entered_expenses" button. With this function, you can view your expenses using filters of your choice: view all records, filter by expense type, filter by date. Also, for convenient data visualization, by pressing the "show graph" button, the bot will send you an image with a graph for each individual filter: a Cartesian graph for all expenses and for a filter by type of expenses, as well as a "pie" for a filter by date.
To process requests from the user to the server, I use the aiogram framework. This is the core of asynchronous web application server based on aiohttp. For plotting, I use a framework called matplotlib and numpy to plot the data.
This final project has several files:
The buttons.py file contains all the buttons.
The create_bot.py file contains a telegram bot reference.
The request.py file enters data into SQL data.db.
Data.db is a SQLite database file that contains two tables. The first table collects data on expense types. The second table collects information on the total sum of expenses.
The basic.py file gives the command start, main menu and help.
The records.py file is responsible for the functionality of the Enter the total expense button.
The shedule.py file is responsible for the functionality of the View entered expenses button.
The servises.py file is responsible for the functionality of the Enter_the_type_of_expense button.
The bot.py file is responsible for running the entire bot.
Thank you for your attention.