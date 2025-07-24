import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
from sagemaker.workflow.parameters import ParameterString, ParameterInteger
from typing import Dict, List
from .config import MLPipelineConfig

class SageMakerPipeline:
    """Class to handle SageMaker Pipeline operations"""

    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.config = MLPipelineConfig()
        self.session = sagemaker.session.Session()
        self.role = sagemaker.get_execution_role()

    def _create_pipeline_parameters(self) -> List:
        """Create and return pipeline parameters"""
        return [
            ParameterString(
                name="InputDataUrl",
                default_value="s3://mlops-testing-bucket-kulsin/sample-data.csv"
            ),
            ParameterInteger(
                name="ProcessingInstanceCount",
                default_value=1
            ),
            ParameterInteger(
                name="TrainingInstanceCount",
                default_value=1
            )
        ]

    def _create_processing_step(self, processing_instance_count: ParameterInteger) -> ProcessingStep:
        """Create and return the data processing step"""
        processor = SKLearnProcessor(
            framework_version=self.config.SKLEARN_FRAMEWORK_VERSION,
            role=self.role,
            instance_type=self.config.PROCESSING_INSTANCE_TYPE,
            instance_count=processing_instance_count
        )

        return ProcessingStep(
            name="SampleProcessing",
            processor=processor,
            inputs=[
                sagemaker.processing.ProcessingInput(
                    source=self.parameters[0],  # InputDataUrl
                    destination="/opt/ml/processing/input"
                )
            ],
            outputs=[
                sagemaker.processing.ProcessingOutput(
                    output_name="train",
                    source="/opt/ml/processing/output/train"
                ),
                sagemaker.processing.ProcessingOutput(
                    output_name="validation",
                    source="/opt/ml/processing/output/validation"
                )
            ],
            code=self.config.PROCESSING_CODE
        )

    def _create_training_step(self, training_instance_count: ParameterInteger,
                            process_step: ProcessingStep) -> TrainingStep:
        """Create and return the model training step"""
        estimator = Estimator(
            image_uri=sagemaker.image_uris.retrieve(
                "xgboost",
                self.session.boto_region_name,
                version=self.config.XGBOOST_VERSION
            ),
            role=self.role,
            instance_count=training_instance_count,
            instance_type=self.config.TRAINING_INSTANCE_TYPE,
            output_path=f"s3://{self.session.default_bucket()}/output"
        )

        return TrainingStep(
            name="SampleTraining",
            estimator=estimator,
            inputs=self._get_training_inputs(process_step)
        )

    def _get_training_inputs(self, process_step: ProcessingStep) -> Dict:
        """Create and return training input configuration"""
        return {
            "train": TrainingInput(
                s3_data=process_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
                content_type="csv"
            ),
            "validation": TrainingInput(
                s3_data=process_step.properties.ProcessingOutputConfig.Outputs["validation"].S3Output.S3Uri,
                content_type="csv"
            )
        }

    def build(self) -> Pipeline:
        """Build and return the pipeline"""
        self.parameters = self._create_pipeline_parameters()
        process_step = self._create_processing_step(self.parameters[1])
        train_step = self._create_training_step(self.parameters[2], process_step)

        return Pipeline(
            name=self.pipeline_name,
            parameters=self.parameters,
            steps=[process_step, train_step],
            sagemaker_session=self.session
        )

    def deploy(self, pipeline: Pipeline) -> None:
        """Deploy the pipeline"""
        pipeline.upsert(role_arn=self.role)

    def execute(self, pipeline: Pipeline, input_data_url: str) -> None:
        """Execute the pipeline with given parameters"""
        execution = pipeline.start(
            parameters={"InputDataUrl": input_data_url}
        )
        print(f"Pipeline execution ARN: {execution.arn}")


def main():
    # Create and deploy pipeline
    pipeline_builder = SageMakerPipeline("SampleDataAnalysisPipeline")
    pipeline = pipeline_builder.build()
    pipeline_builder.deploy(pipeline)

    # Optional: Execute the pipeline
    pipeline_builder.execute(
        pipeline,
        "s3://mlops-testing-bucket-kulsin/sample-data.csv"
    )


if __name__ == "__main__":
    main()