"""
Workflow service module for managing and executing LangGraph workflows.
"""
import importlib.util
import json
import logging
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

class WorkflowRegistry:
    """Service for managing and executing workflows."""
    
    def __init__(self, workflows_dir: str = "workflows"):
        """
        Initialize the workflow service.
        
        Args:
            workflows_dir: Directory where workflow modules are stored
        """
        self.workflows_dir = workflows_dir
        self._ensure_workflows_dir()
        self.workflows = {}
        self.load_all_workflows()
        
    def _ensure_workflows_dir(self):
        """Ensure the workflows directory exists."""
        os.makedirs(self.workflows_dir, exist_ok=True)
        init_file = os.path.join(self.workflows_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("# Automatically generated\n")
        
    def load_all_workflows(self):
        """Load all available workflows from the workflows directory."""
        try:
            workflow_dirs = [d for d in os.listdir(self.workflows_dir) 
                           if os.path.isdir(os.path.join(self.workflows_dir, d)) 
                           and not d.startswith("__")]
            
            for workflow_dir in workflow_dirs:
                self.load_workflow(workflow_dir)
        except Exception as e:
            logger.error(f"Error loading workflows: {e}")
    
    def load_workflow(self, workflow_id: str) -> bool:
        """
        Load a specific workflow module.
        
        Args:
            workflow_id: ID of the workflow to load
            
        Returns:
            bool: True if workflow was loaded successfully
        """
        try:
            workflow_path = os.path.join(self.workflows_dir, workflow_id)
            
            if not os.path.exists(workflow_path):
                logger.error(f"Workflow directory does not exist: {workflow_path}")
                return False
            
            # Attempt to import the module
            spec = importlib.util.spec_from_file_location(
                f"workflows.{workflow_id}.main", 
                os.path.join(workflow_path, "main.py")
            )
            
            if spec is None or spec.loader is None:
                logger.error(f"Could not load workflow module: {workflow_id}")
                return False
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Register the workflow
            if hasattr(module, "run_graph"):
                self.workflows[workflow_id] = {
                    "module": module,
                    "run_func": module.run_graph,
                    "loaded_at": datetime.now().isoformat()
                }
                logger.info(f"Successfully loaded workflow: {workflow_id}")
                return True
            else:
                logger.error(f"Workflow module does not have run_graph function: {workflow_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading workflow {workflow_id}: {e}")
            return False
    
    def register_workflow(self, 
                          workflow_id: str, 
                          name: str,
                          code_files: Dict[str, str]) -> bool:
        """
        Register a new workflow from code files.
        
        Args:
            workflow_id: Unique identifier for the workflow
            name: Name of the workflow
            code_files: Dictionary of code files (filename to content)
            
        Returns:
            bool: True if workflow was registered successfully
        """
        try:
            # Create workflow directory
            workflow_dir = os.path.join(self.workflows_dir, workflow_id)
            os.makedirs(workflow_dir, exist_ok=True)
            
            # Write files
            for filename, content in code_files.items():
                with open(os.path.join(workflow_dir, filename), "w") as f:
                    f.write(content)
            
            # Create __init__.py
            with open(os.path.join(workflow_dir, "__init__.py"), "w") as f:
                f.write(f"# Workflow: {name}\n")
            
            # Create metadata.json
            metadata = {
                "workflow_id": workflow_id,
                "name": name,
                "created_at": datetime.now().isoformat(),
            }
            
            with open(os.path.join(workflow_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Load the workflow
            return self.load_workflow(workflow_id)
            
        except Exception as e:
            logger.error(f"Error registering workflow {workflow_id}: {e}")
            return False
    
    def execute_workflow(self, workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a workflow with the given inputs.
        
        Args:
            workflow_id: ID of the workflow to execute
            inputs: Input parameters for the workflow
            
        Returns:
            Dict[str, Any]: Workflow execution results
        
        Raises:
            ValueError: If workflow not found or execution fails
        """
        if workflow_id not in self.workflows:
            if not self.load_workflow(workflow_id):
                raise ValueError(f"Workflow not found: {workflow_id}")
        
        try:
            # Call the run_graph function from the workflow module
            result = self.workflows[workflow_id]["run_func"](inputs)
            return result
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_id}: {e}")
            raise ValueError(f"Error executing workflow: {str(e)}")
    
    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """
        Get a list of all registered workflows.
        
        Returns:
            List[Dict[str, Any]]: List of workflow metadata
        """
        workflow_list = []
        
        for workflow_id in self.workflows:
            workflow_dir = os.path.join(self.workflows_dir, workflow_id)
            metadata_path = os.path.join(workflow_dir, "metadata.json")
            
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                        workflow_list.append(metadata)
                except Exception as e:
                    logger.error(f"Error reading metadata for workflow {workflow_id}: {e}")
            
        return workflow_list
    
    def get_workflow_metadata(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific workflow.
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Optional[Dict[str, Any]]: Workflow metadata or None if not found
        """
        workflow_dir = os.path.join(self.workflows_dir, workflow_id)
        metadata_path = os.path.join(workflow_dir, "metadata.json")
        
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading metadata for workflow {workflow_id}: {e}")
        
        return None
        
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.
        
        Args:
            workflow_id: ID of the workflow to delete
            
        Returns:
            bool: True if workflow was deleted successfully
        """
        try:
            workflow_dir = os.path.join(self.workflows_dir, workflow_id)
            
            if not os.path.exists(workflow_dir):
                logger.warning(f"Workflow directory does not exist: {workflow_dir}")
                return False
            
            # Remove workflow from registry
            if workflow_id in self.workflows:
                del self.workflows[workflow_id]
            
            # Delete workflow files
            import shutil
            shutil.rmtree(workflow_dir)
            
            logger.info(f"Successfully deleted workflow: {workflow_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting workflow {workflow_id}: {e}")
            return False


# Create singleton instance
workflow_registry = WorkflowRegistry() 