"""
Workflow schemas module.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkflowInput(BaseModel):
    """Base model for workflow inputs."""
    workflow_id: str = Field(..., description="Unique identifier for the workflow")


class WorkflowOutput(BaseModel):
    """Base model for workflow outputs."""
    workflow_id: str = Field(..., description="Unique identifier for the workflow")
    node_results: List[Dict[str, Any]] = Field([], description="Results from each node in the workflow")
    final_report: Optional[str] = Field(None, description="Final generated report")
    status: str = Field("completed", description="Workflow execution status")


class DynamicWorkflowInput(BaseModel):
    """
    Dynamic model for workflow inputs that will be populated at runtime
    based on the LangGraph workflow schema.
    """
    workflow_id: str = Field(..., description="Unique identifier for the workflow")
    # Other fields will be dynamically added based on the workflow schema


class WorkflowExecutionRequest(BaseModel):
    """
    Request model for executing a workflow.
    """
    workflow_id: str
    inputs: Dict[str, Any] = Field(default_factory=dict)


class WorkflowStatusResponse(BaseModel):
    """
    Response model for workflow status.
    """
    workflow_id: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None


class WorkflowDefinition(BaseModel):
    """
    Model representing a workflow definition.
    """
    workflow_id: str
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any]
    created_at: Optional[str] = None 