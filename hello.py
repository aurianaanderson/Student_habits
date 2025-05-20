import preswald
from preswald import connect, get_df, text, table, plotly, sidebar
import pandas as pd
import plotly.express as px

connect()

student_perf = pd.read_csv("data/student_habits_performance.csv")

text("# Student Data App")


student_perf = student_perf.drop(columns=["student_id"])

low_scores = student_perf[student_perf["exam_score"] < 75]

text("## Students with Low Scores")
table(low_scores, "Students with Low Scores")




Average_Study_exams = student_perf[["study_hours_per_day", "exam_score"]].agg({
    "study_hours_per_day" : "mean"
    , "exam_score" : "mean"
}).round(2).reset_index()

Average_Study_exams.columns =["Metric", "Average Value"]
text("## Average study hours and exam Score of students with Low Scores")
table(Average_Study_exams, "Average study hours and exam Score of students with Low Scores")

avg_study = Average_Study_exams.loc[Average_Study_exams["Metric"] == "study_hours_per_day", "Average Value"].values[0]
avg_score =  Average_Study_exams.loc[Average_Study_exams["Metric"] == "exam_score", "Average Value"].values[0]

#Scatter plot of Study hours vs. Exam Scores

text("## Plot of Study hours vs. Exam Scores for Low Scorers")
fig = px.scatter(
    low_scores
    ,x = "study_hours_per_day"
    ,y ="exam_score"
    ,color = "gender"
    ,labels = {"study_hours_per_day" :"Study Hours per Day"
    ,"exam_score" : "Exam Score"}
)

fig.add_vline(
    x =avg_study
    ,line_dash = "dash"
    ,line_color = "purple"
    ,annotation_text = f"Average Hours Studying {avg_study}"
    ,annotation_position = "top right"
)

fig.add_hline(
    y =avg_score
    ,line_dash = "dash"
    ,line_color = "orange"
    ,annotation_text = f"Average Exam Score {avg_score}"
    ,annotation_position = "bottom right"
)

#fig.update_layout(
#    xaxis_title= "Study Hours per Day"
#    , yaxis_title = "Exam Score"
#)



plotly(fig)

numeric = student_perf.select_dtypes (include = "number")
correlation_mat =numeric.corr()

text("## Table of Relationships Bewtween Student personal and Academic Habits")
table(correlation_mat, title = "Correlation Matrix of numeric features only")

fig_corr =px.imshow(correlation_mat
,text_auto = True
,color_continuous_scale = "Blackbody")


text("## Relationships Bewtween Student personal and Academic Habits")
plotly(fig_corr)

with sidebar():
    text("### Navigate Student Data")
    text("- Student Scores\n- Trends\n- Correlation Matrix")