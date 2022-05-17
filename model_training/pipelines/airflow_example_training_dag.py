from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from great_expectations.core.batch import BatchRequest
from great_expectations.data_context.types.base import (
    DataContextConfig,
    CheckpointConfig

@provide_session
def on_success_callback(context, session=None):
    pass

def on_failure_callback(context):
    # Raise slack alert
    pass

with DAG(DAG_ID,
         ) as dag:

    ge_data_context_root_dir_with_checkpoint_name_pass = GreatExpectationsOperator(
        task_id="ge_data_context_root_dir_with_checkpoint_name_pass",
        data_context_root_dir=ge_root_dir,
        checkpoint_name="some.pass.chk",
    )

    ge_data_context_config_with_checkpoint_config_pass = GreatExpectationsOperator(
        task_id="ge_data_context_config_with_checkpoint_config_pass",
        data_context_config=example_data_context_config,
        checkpoint_config=example_checkpoint_config,
    )

ge_data_context_root_dir_with_checkpoint_name_pass >> ge_data_context_config_with_checkpoint_config_pass
