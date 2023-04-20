## Predict-student-test-score
This project aims to create a predictive model for student test scores using IBM SPSS Modeler and Python. The dataset used for this project contains information on students' demographics, academic background, and other relevant factors that may affect their test scores.

## IBM SPSS Moduler
We have used four different machine learning algorithms in this project: linear regression, neural network, XGBoost, and random forest. The dataset was split into training and testing sets, and each algorithm was trained on the training set and tested on the testing set.

After comparing the performance of the four algorithms, we found that linear regression achieved the highest accuracy, with an accuracy of 95%. The other algorithms also performed well, with neural network achieving an accuracy of 92%, XGBoost achieving an accuracy of 93%, and random forest achieving an accuracy of 94%.

<b>Node Explanatiion:-</b>
1. **Data Asset Node** - used to import, manage, and prepare data for analysis. This node allows you to connect to various data sources such as databases, spreadsheets, and text files, and perform various data manipulation tasks such as filtering, merging, aggregating, and transforming data.
2. **Reclassify** - The Reclassify node in IBM SPSS Modeler is a data transformation node that allows you to modify the values of one or more fields in your data by creating new categories or changing the values of existing categories. This node is useful when you need to recode or transform data into a new format that is more suitable for your analysis.
3. **Type Node** - The Type node in IBM SPSS Modeler is a data transformation node that allows you to change the data type of one or more fields in your data. This node is useful when you need to convert data from one type to another in order to perform specific analyses or modeling tasks.
4. **Filter Node** - The Filter node in IBM SPSS Modeler is a data manipulation node that allows you to subset your data based on certain criteria. This node is useful when you need to focus on a specific subset of your data or remove unwanted records from your data.
5. **Short Node** - The Short Node in IBM SPSS Modeler is a data manipulation node that allows you to reduce the number of fields in your data. This node is useful when you have a large number of fields in your data and need to focus on a specific subset of those fields.
6. **Partition Node** - The Partition node in IBM SPSS Modeler is a data manipulation node that allows you to split your data into two or more partitions for training and testing purposes. This node is useful when you need to evaluate the performance of a predictive model on new, unseen data.
7. **Aggregate Node** - The Aggregate Node in IBM SPSS Modeler is a data transformation node that allows you to group and summarize data based on one or more fields. This node is useful when you need to aggregate data at a higher level, such as summarizing sales data by product or by region.
8. **Select Node** - The Select Node in IBM SPSS Modeler is a data transformation node that allows you to select and filter specific fields from your data. This node is useful when you need to reduce the number of fields in your data or focus on a specific subset of fields.

## Python Files Discription
in the models_accurecy Python file, we import the necessary libraries and load your data. Then we split the data into training and testing sets.

Next, we create four different models - linear regression, neural network, XGBoost, and random forest. then fit each model to training data and evaluate its accuracy using the mean squared error or another appropriate metric.

After evaluating the accuracy of each model, you would select the one with the highest accuracy. In this case, you mentioned that the linear regression model had the highest accuracy of 95%.

In the linear_regrassion Python file, we import the linear regression model from scikit-learn and load test data. Then we apply the predict method to the test data using the linear regression model to predict the student test scores. Finally,output the predicted scores and possibly evaluate the accuracy of the model using a metric such as mean squared error.
