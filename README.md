# A machine learning based tennis matches prediction webapp
 
Great thanks to JeffSackmann for the [WTA data set](https://github.com/JeffSackmann/tennis_wta).
In this project, we decided to use data from 2000 to 2021 for the prediction model, because the difference in racquet manufacturing technology and court surface from the 2000s and earlier can falsify the results. The total number of matches from 2000 to 2021 that the team collected is 60638 matches with 2481 athletes participating. Once the data set is obtained, the group will conduct preprocessing of the data. After redesigning the new features, we will proceed to fill the data or remove the data that cannot be filled. After preprocessing the data, a dataset of 19143 matches was obtained, which will be the official data set for training. In which, the team will take out the matches from 2018 to 2021 including more than 3500 matches with 507 athletes to serve as a database for building the project's website system. The dataset was used as a input to train a binary classifier (win vs lose) model that predict result of the match.

Beside the match predictions, we also create a graph of performance over time of each player in the dataset with great help of Kick-off library.

# Model accuracy evaluation

| MODEL                        | TRAIN ACCURACY | TEST ACCURACY |
|------------------------------|----------------|---------------|
| Base line                    | 66.03%         | 66.03%        |
| *Gradient boosting*            | 72.5%          | 69.4%         |
| Random forest                | 71.9%          | 68.5%         |
| Logistic regression          | 70.3%          | 69.4%         |
| Linear discriminant analysis | 70.1%          | 69.4%         |
| Gassian naive Bayes          | 68.5%          | 67.9%         |

# Tech stack

- Flask + Dashed
- HTML5 CSS3
- VanillaJS
- jQuery

# Demo
[here] 

