from pydantic import BaseModel, Field


class TicketNoteInput(BaseModel):
    author: str = Field(min_length=1, max_length=80)
    body: str = Field(min_length=1, max_length=1000)


class TicketAnalysisInput(BaseModel):
    ticket_id: str = Field(min_length=1)
    risk: str = Field(pattern="^(low|medium|high|critical)$")
    summary: str = Field(min_length=1, max_length=2000)
    evidence: list[str] = Field(default_factory=list)

