class MLPipelineConfig:
    """Configuration class for ML Pipeline parameters"""
    def __init__(self):
        self.SKLEARN_FRAMEWORK_VERSION = "0.23-1"
        self.PROCESSING_INSTANCE_TYPE = "ml.t3.medium"
        self.TRAINING_INSTANCE_TYPE = "ml.m5.xlarge"
        self.XGBOOST_VERSION = "1.2-1"
        self.PROCESSING_CODE = "processing_script.py"