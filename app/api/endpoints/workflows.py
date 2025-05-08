"""
Workflow API endpoints.
"""
import uuid
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.workflow import (
    WorkflowDefinition,
    WorkflowExecutionRequest,
    WorkflowOutput,
    WorkflowStatusResponse
)
from app.services.workflow_service import workflow_registry

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get(
    "",
    response_model=List[WorkflowDefinition],
    status_code=status.HTTP_200_OK,
    summary="Get all workflows",
    response_description="Returns a list of all registered workflows",
)
async def get_workflows():
    """
    Get a list of all registered workflows.
    
    Returns:
        List[WorkflowDefinition]: A list of workflow definitions
    """
    return workflow_registry.get_all_workflows()


@router.get(
    "/{workflow_id}",
    response_model=WorkflowDefinition,
    status_code=status.HTTP_200_OK,
    summary="Get workflow by ID",
    response_description="Returns the workflow definition",
)
async def get_workflow(workflow_id: str):
    """
    Get a workflow by ID.
    
    Args:
        workflow_id (str): The ID of the workflow
        
    Returns:
        WorkflowDefinition: The workflow definition
        
    Raises:
        HTTPException: If the workflow is not found
    """
    metadata = workflow_registry.get_workflow_metadata(workflow_id)
    
    if metadata is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found: {workflow_id}",
        )
    
    return metadata


@router.post(
    "/execute",
    response_model=WorkflowOutput,
    status_code=status.HTTP_200_OK,
    summary="Execute a workflow",
    response_description="Returns the workflow execution results",
)
async def execute_workflow(request: WorkflowExecutionRequest):
    """
    Execute a workflow with the provided inputs.
    
    Args:
        request (WorkflowExecutionRequest): The workflow execution request
        
    Returns:
        WorkflowOutput: The workflow execution results
        
    Raises:
        HTTPException: If the workflow is not found or execution fails
    """
    try:
        result = workflow_registry.execute_workflow(
            request.workflow_id, 
            request.inputs
        )
        
        # Ensure expected structure or provide defaults
        if isinstance(result, dict):
            # Enhance with workflow ID
            result["workflow_id"] = request.workflow_id
            
            # Add defaults for expected fields if missing
            if "node_results" not in result:
                result["node_results"] = []
            
            return result
        else:
            # Handle non-dict results
            return {
                "workflow_id": request.workflow_id,
                "status": "completed",
                "node_results": [],
                "result": result,
            }
            
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing workflow: {str(e)}",
        )


@router.post(
    "",
    response_model=WorkflowDefinition,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new workflow",
    response_description="Returns the registered workflow definition",
)
async def register_workflow(
    name: str,
    code_files: Dict[str, str],
    workflow_id: str = None
):
    """
    Register a new workflow.
    
    Args:
        name (str): The name of the workflow
        code_files (Dict[str, str]): Dictionary of code files (filename to content)
        workflow_id (str, optional): The ID for the workflow. Defaults to None, which generates a UUID.
        
    Returns:
        WorkflowDefinition: The registered workflow definition
        
    Raises:
        HTTPException: If the workflow registration fails
    """
    # Generate workflow ID if not provided
    if workflow_id is None:
        workflow_id = str(uuid.uuid4())
    
    # Register the workflow
    success = workflow_registry.register_workflow(
        workflow_id=workflow_id,
        name=name,
        code_files=code_files,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register workflow",
        )
    
    # Get the workflow metadata
    metadata = workflow_registry.get_workflow_metadata(workflow_id)
    
    return metadata


@router.delete(
    "/{workflow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a workflow",
    response_description="No content",
)
async def delete_workflow(workflow_id: str):
    """
    Delete a workflow.
    
    Args:
        workflow_id (str): The ID of the workflow to delete
        
    Returns:
        None
        
    Raises:
        HTTPException: If the workflow is not found or deletion fails
    """
    success = workflow_registry.delete_workflow(workflow_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found or could not be deleted: {workflow_id}",
        )
    
    return None 