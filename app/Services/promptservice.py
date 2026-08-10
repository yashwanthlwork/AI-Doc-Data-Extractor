from app.DBModels.prompt import Prompt
from app.Services.documenttypeservice import DocumentTypeService
from uuid import UUID
from app.Configuration.DBSession import SessionLocal
from app.DBModels.document_type import DocumentType
from sqlalchemy import select
from sqlalchemy.orm import Session


class PromptService:
    def create_prompt(self,prompt_name:str,prompt:str,document_type:UUID)-> Prompt:
        prompt_name=prompt_name.strip().upper()
        prompt=prompt.strip()
        if not prompt_name:
            raise ValueError("Prompt name cannot be empty.")

        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        if not document_type:
            raise ValueError("Document type cannot be empty.")
        
        session: Session = SessionLocal()
    
        try:
            document_type_exists=session.scalar(
                select(DocumentType).where(DocumentType.document_type_id==document_type)
            )
            if not document_type_exists:
                raise ValueError("Document type does not exist.")
            
            if session.scalar(
                select(Prompt).where(Prompt.prompt_name == prompt_name)
            ):
                raise ValueError("Prompt name already exists.")

            if session.scalar(
                select(Prompt).where(Prompt.document_type_id == document_type)
            ):
                raise ValueError("A prompt already exists for this document type.")

            new_prompt=Prompt(
                prompt_name=prompt_name,
                prompt=prompt,
                document_type_id=document_type
            )

            session.add(new_prompt)
            session.commit()
            session.refresh(new_prompt)

            return new_prompt
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        
    def fetch_prompt_by_prompt_id(self,session:Session,prompt_id:UUID)->Prompt:
        if not prompt_id:
            raise ValueError("Invalid Prompt ID.")
        
        prompt_details=session.scalar(
            select(Prompt).where(Prompt.prompt_id==prompt_id)
        )
        if not prompt_details:
            raise ValueError("Given Prompt ID does not exist.")
        return prompt_details
        

    def fetch_prompt_by_document_type_id(self,session:Session,document_type_id:UUID)->Prompt:
        if not document_type_id:
            raise ValueError("Invalid Document Type ID.")
        
        prompt_details=session.scalar(
            select(Prompt).where(Prompt.document_type_id==document_type_id)
        )
        if not prompt_details:
            raise ValueError("No prompt configured for given Document Type ID.")
        return prompt_details
    
    
    def fetch_all_prompts(self)->list[Prompt]:
        session:Session = SessionLocal()
        try:
            return session.scalars(
                select(Prompt).order_by(Prompt.prompt_name)
                ).all()
        finally:
            session.close()
            

    def update_prompt(self, prompt_id: UUID, prompt: str | None = None, document_type_id: UUID | None = None) -> Prompt:

        if not prompt_id:
            raise ValueError("Invalid Prompt ID.")

        if prompt is None and document_type_id is None:
            raise ValueError("No update data provided.")

        session: Session = SessionLocal()

        try:
            prompt_details = session.scalar(
                select(Prompt).where(Prompt.prompt_id == prompt_id)
            )

            if not prompt_details:
                raise ValueError("Given Prompt ID does not exist.")

            if prompt is not None:
                prompt = prompt.strip()

                if not prompt:
                    raise ValueError("Invalid Prompt.")

                prompt_details.prompt = prompt

            if document_type_id is not None:
                documenttypeservice = DocumentTypeService()

                if not documenttypeservice.check_document_type_id_exists(
                    session,
                    document_type_id
                ):
                    raise ValueError("Invalid Document Type ID.")

                existing_prompt = session.scalar(
                    select(Prompt).where(
                        Prompt.document_type_id == document_type_id,
                        Prompt.prompt_id != prompt_id
                    )
                )

                if existing_prompt:
                    raise ValueError(
                        f"Document type already linked to "
                        f"{existing_prompt.prompt_name}."
                    )

                prompt_details.document_type_id = document_type_id

            session.commit()
            session.refresh(prompt_details)

            return prompt_details

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()