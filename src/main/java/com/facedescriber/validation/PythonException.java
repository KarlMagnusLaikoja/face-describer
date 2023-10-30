package com.facedescriber.validation;

public class PythonException extends Exception {
    private int exitCode;

    public PythonException(int exitCode, String message) {
        super(message);
        this.exitCode = exitCode;
    }

}
