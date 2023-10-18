package com.facedescriber.validation;

public class MissingFieldException extends Exception{
    public MissingFieldException(String message) {
        super(message);
    }
}
