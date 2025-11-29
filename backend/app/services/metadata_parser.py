"""
PDF metadata parsing service.
Extracts and analyzes PDF metadata for suspicious patterns.
"""
from PyPDF2 import PdfReader
import io
from datetime import datetime
from app.models.schemas import MetadataData


def parse_metadata(pdf_content: bytes) -> MetadataData:
    """
    Parse PDF metadata and check for suspicious patterns.
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        MetadataData object with metadata and flags
    """
    flags = []
    created_date = ""
    modified_date = ""
    author = ""
    software = ""
    
    try:
        # Read PDF from bytes
        pdf_file = io.BytesIO(pdf_content)
        reader = PdfReader(pdf_file)
        
        # Extract metadata
        metadata = reader.metadata
        
        if metadata:
            # Extract dates
            if '/CreationDate' in metadata:
                created_date = format_pdf_date(metadata['/CreationDate'])
            
            if '/ModDate' in metadata:
                modified_date = format_pdf_date(metadata['/ModDate'])
            
            # Extract author
            if '/Author' in metadata:
                author = str(metadata['/Author'])
            
            # Extract software
            if '/Producer' in metadata:
                software = str(metadata['/Producer'])
            elif '/Creator' in metadata:
                software = str(metadata['/Creator'])
            
            # Check for suspicious patterns
            if created_date and modified_date:
                try:
                    created = parse_date(created_date)
                    modified = parse_date(modified_date)
                    
                    # Flag if modified after creation (suspicious)
                    if created and modified and modified > created:
                        flags.append("PDF modified after creation date")
                except:
                    pass
            
            # Check for suspicious software
            if software:
                suspicious_software = ['photoshop', 'gimp', 'inkscape', 'illustrator']
                if any(sus in software.lower() for sus in suspicious_software):
                    flags.append(f"Suspicious creation software: {software}")
        
    except Exception as e:
        print(f"Error parsing metadata: {str(e)}")
        flags.append("Failed to parse metadata")
    
    return MetadataData(
        created_date=created_date,
        modified_date=modified_date,
        author=author,
        software=software,
        flags=flags
    )


def format_pdf_date(pdf_date: str) -> str:
    """Format PDF date string to readable format."""
    try:
        # PDF dates are in format: D:YYYYMMDDHHmmSSOHH'mm'
        if pdf_date.startswith('D:'):
            date_str = pdf_date[2:16]  # Extract YYYYMMDDHHmmSS
            year = date_str[0:4]
            month = date_str[4:6]
            day = date_str[6:8]
            hour = date_str[8:10]
            minute = date_str[10:12]
            second = date_str[12:14]
            return f"{year}-{month}-{day} {hour}:{minute}:{second}"
        return pdf_date
    except:
        return str(pdf_date)


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    try:
        # Try common formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
    except:
        pass
    return None
