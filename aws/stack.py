from aws_cdk import (
    core,
    aws_lambda as _lambda,
)
import os
import subprocess

class Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        entrypoint_name = 'app1'
        
        _lambda.Function(
            self, 
            entrypoint_name,
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset(f'../{entrypoint_name}'),
            handler='index.handler',
            layers=[
                self.create_dependencies_layer(self.stack_name, entrypoint_name)
            ]
        )

    def create_dependencies_layer(self, project_name, function_name: str) -> _lambda.LayerVersion:
        requirements_file = f'../requirements.{function_name}.txt'
        output_dir = f'../.build/{function_name}'

        if not os.environ.get('SKIP_PIP'):
            subprocess.check_call(
                f'pip install -r {requirements_file} -t {output_dir}/python'.split()
            )

        layer_id = f'{project_name}-{function_name}-dependencies'
        layer_code = _lambda.Code.from_asset(output_dir)

        return _lambda.LayerVersion(self, layer_id, code=layer_code)