"""AI Assistant router for handling natural language commands."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user, get_db
from models import User
from schemas import AIResponse, AICommand

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/parse-command")
async def parse_ai_command(
    prompt: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIResponse:
    """
    Parse a natural language prompt and return structured commands.
    
    The frontend's LLM already processed the prompt. This endpoint
    takes the AI's response text and structures it into actionable commands.
    
    Args:
        prompt: The natural language prompt from the user
        current_user: Authenticated user
        db: Database session
    
    Returns:
        AIResponse with structured commands for frontend actions
    """
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    commands = []
    explanation = ""
    
    # Parse the prompt for common actions
    prompt_lower = prompt.lower()
    
    # STATUS FILTERS
    if "available" in prompt_lower:
        commands.append(
            AICommand(
                action="filter",
                target="status",
                value="Available",
                description="Show available devices"
            )
        )
    elif "in use" in prompt_lower or "in-use" in prompt_lower:
        commands.append(
            AICommand(
                action="filter",
                target="status",
                value="In Use",
                description="Show devices in use"
            )
        )
    elif "repair" in prompt_lower or "broken" in prompt_lower:
        commands.append(
            AICommand(
                action="filter",
                target="status",
                value="Repair",
                description="Show devices in repair"
            )
        )
    elif "all devices" in prompt_lower or "show all" in prompt_lower:
        commands.append(
            AICommand(
                action="filter",
                target="status",
                value="All",
                description="Show all devices"
            )
        )
    
    # SORTING
    if "sort by brand" in prompt_lower or "sorted by brand" in prompt_lower:
        commands.append(
            AICommand(
                action="sort",
                target="sort_by",
                value="brand",
                description="Sort devices by brand"
            )
        )
    elif "sort by date" in prompt_lower or "newest" in prompt_lower or "oldest" in prompt_lower:
        commands.append(
            AICommand(
                action="sort",
                target="sort_by",
                value="date",
                description="Sort devices by purchase date"
            )
        )
    elif "sort by name" in prompt_lower or "alphabetically" in prompt_lower:
        commands.append(
            AICommand(
                action="sort",
                target="sort_by",
                value="name",
                description="Sort devices by name"
            )
        )
    
    # SEARCH
    search_match = prompt_lower.find('"')
    if search_match != -1:
        end_match = prompt_lower.find('"', search_match + 1)
        if end_match != -1:
            search_term = prompt[search_match + 1:end_match]
            commands.append(
                AICommand(
                    action="search",
                    target="search",
                    value=search_term,
                    description=f"Search for '{search_term}'"
                )
            )
    
    # NAVIGATION
    if "rental" in prompt_lower or "my rental" in prompt_lower or "renting" in prompt_lower:
        commands.append(
            AICommand(
                action="navigate",
                target="view",
                value="rentals",
                description="Navigate to my rentals"
            )
        )
    elif "admin" in prompt_lower or "manage device" in prompt_lower or "management" in prompt_lower:
        commands.append(
            AICommand(
                action="navigate",
                target="view",
                value="admin-devices",
                description="Navigate to device management"
            )
        )
    
    # Generate explanation based on parsed commands
    if commands:
        explanation = f"I found {len(commands)} action(s): " + ", ".join(
            [c.description or f"{c.action} {c.value}" for c in commands]
        )
    else:
        explanation = (
            "I couldn't identify specific actions in your prompt. "
            "Try: 'Show available devices', 'Sort by brand', 'Show my rentals', etc."
        )
    
    return AIResponse(
        explanation=explanation,
        commands=commands,
        success=True
    )


@router.get("/suggestions")
async def get_ai_suggestions(
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get suggestions for AI commands to help users."""
    return {
        "filters": [
            "Show me available devices",
            "Display devices in repair",
            "Show all devices in use",
        ],
        "sorts": [
            "Sort devices by brand",
            "Sort by purchase date",
            "Sort alphabetically by name",
        ],
        "navigation": [
            "Take me to my rentals",
            "Show me the device management panel",
        ],
        "combined": [
            "Available devices sorted by brand",
            "Show me devices in repair sorted by date",
        ],
    }
