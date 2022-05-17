import os
from jinja2 import Template
import kfp
from kfp.components import func_to_container_op
from kfp.gcp import use_gcp_secret

# Data quality check of the training dataset using Great Expectations (GE) integration in Kubeflow

from kfp.components import ComponentStore
store = ComponentStore.default_store
validate_csv_step = store.load_component(“great-expectations/validate/CSV”)

# Have the Expectations suite in a bucket or in a directory
with open('expectation_suite.json') as file:
    expectation_suite = file.read()

# Validate training data before feeding into ML algorithms
validate_csv = validate_csv_op(training_data_csv, expectation_suite)

# Further Kubeflow training steps e.g. hyperparameter tuning, model evaluation etc.




# Another way to validate training dataset could be using tensorflow-data-validation on notebook
import tensorflow as tf
import tensorflow_data_validation as tfdv
train_stats = tfdv.generate_statistics_from_csv(data_location=TRAIN_DATA)
# Compute stats for evaluation data
eval_stats = tfdv.generate_statistics_from_csv(data_location=EVAL_DATA)
# Compare evaluation data with training data
tfdv.visualize_statistics(lhs_statistics=eval_stats, rhs_statistics=train_stats,
                          lhs_name='EVAL_DATASET', rhs_name='TRAIN_DATASET')
# Does our evaluation dataset match the schema from our training dataset?
# Check eval data for errors by validating the eval data stats using the previously inferred schema.
anomalies = tfdv.validate_statistics(statistics=eval_stats, schema=schema)
