package com.facedescriber.constants;

public enum BackendError {
    OK(0),
    MISSING_FIELD(1),
    INVALID_BASE64(2),
    UNSUPPORTED_LANGUAGE(3),
    BACKEND_FAILURE(4),
    INVALID_JSON(5),
    PYTHON_ERROR(101);
    int errorCode;

    BackendError(int errorCode) {
        this.errorCode = errorCode;
    }

    public int getErrorCode() {
        return errorCode;
    }
}
