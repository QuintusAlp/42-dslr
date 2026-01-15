class DataDescribeError(Exception):
    """Base exception for describe.py errors"""
    pass

class FileValidationError(DataDescribeError):
    """Raised when file validation fails"""
    pass

class DataProcessingError(DataDescribeError):
    """Raised when data processing fails"""
    pass