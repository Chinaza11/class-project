This was the capstone project for the UGA course INFO8000 (Foundations of Informatics for Research and Practice; 
https://bulletin.uga.edu/Link?cid=info8000). I took this course in 2020 during my master’s degree program. It is a recent 
commit on GitHub because I pulled a copy of this program from the assignment repository where I submitted it on GitHub 
while taking the class and added it here (my personal repository).

The expectation of the project by the instructor (Dr. Kyle Johnson) was for every student to build a useful service for 
their research that demonstrated proficiency in most of the topics covered in the course. Some topics covered in the course 
were:  python programming, data transformation (Pandas), plotting (Matplotlib, Seaborn, Plotly), regular expression, 
handling geographic and image data, web servers, databases and supervised machine learning.

My project used several independent variables (weed density, crop vigor rating, gall rating, southern blight incidence, soil 
population density of root-knot nematode at planting, midseason and at the end of the season) to predict the crop fruit 
yield (target/dependent variable). Aside the machine learning component, my project also incorporated several other 
components such as database, plotting, summary statistics, data upload and storage platform.

After running the program (project1.py), type 127.0.0.1 on your local browser, this should lead to the homepage where you 
have three options to select from: 1) add data via manual input 2) add data via a form 3) view dashboard.

If you proceed to the dashboard, you have several options to choose from: sum stat, sum stat by year, graphs, map, input 
data for predictions and view your predictions.

Building of machine learning model was done in jupyter. File is titled "machine_learning.ipynb". Joblib was used for saving 
built model.

Two databases were made: one was for building the model and the other was for collecting data inputs for predictions.
