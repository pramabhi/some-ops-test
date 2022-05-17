
## MLOps and DataOps examples

* Thank you so much for giving me the opportunity of work on this assignment. 
* I really enjoyed and also learned many things during the process.
* I tried to show how ML training and API deployment pipelines could look like that address many of the issues provided in the assignment.
* However, I didn't have time to debug and make everything running. Please, consider them as pseudocode. 
* Since, it's an ops test, I focused on the pipelines and dependencies. I didn't have time to look into the issues in the model itself as well as in the training dataset. [If this test doesn't work, I would like to try the data science challenge :) ]
* Bellow is a summary of the solution.

### This is really quick and dirty - how would you do this better?

* There are two separate directories for model training pipeline and API deployment pipeline.
* In the model training section, there are components of a TFX/Kubeflow training pipeline in Google Cloud.
* The steps are in the `cloudbuild.yaml` file which is run using `deploy.sh` containing a sample `gcloud` command.
* There is also a sample airflow dag in the pipelines directory.
* In the model API section, various components of gunicorn/flask app deployment were provided.
* Gunicorn adds multithreading option. The `Main` directory has the flask app.
* There are functions for prediction, healthcheck, authentication, api user tracking, unit test etc.
* The `Makefile` has steps for local development using `docker-compose`.


### Come up with tests for container or requests failure

* There is a step to test the docker container in the `cloudbuild.yaml` that uses a google provided tool `container-structure-test`.
* The code to test the docker container is in `text_docker_image.py`.
* The `model_api/test/` folder has unit tests for the flask API.

### Come up with tests for data quality in this context

* Great Expectations has been integrated in the Kubeflow pipeline to run automated data quality check on the training data before feeding it to the ML model. If the Great Expectations test fails, pipeline won't go to the ML training stage.
* There is an airflow operator available for Great Expectations.
* Also, data quality check could be performed using tensorflow-data-validattion in the notebook during experiments.
* Data quality tool `WhyLabs` could be integrated with flask API. I started adding snippets but there are too many boilerplate files in their example repo.
* `WhyLabs` would identify sudden changes in the incoming data. It has a nice dashboard.
* Alternatively, a json with distributions in the training data could be used to compare with the incoming data in the data processing stage inside the flask app.

### Introduce slack alerts for failure of either of the above

* A snippet for the slack alert has been provided. In case of failure slack message could be sent.
* Alternatively, python package `requests` [requests.post()] containing a slack webhook could be used to send message in case of any failure.
* Using the user tracking functionality, we can keep a record of the timestamp of the latest slack message either in a dictionary or a table to avoid duplicate messages in a certain time period.
* If the number of users is very high, cache services like Redis, Memcached etc. could be usd to store some data.
