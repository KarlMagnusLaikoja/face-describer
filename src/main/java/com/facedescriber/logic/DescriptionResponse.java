package com.facedescriber.logic;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.stereotype.Component;

import java.io.Serializable;

@Component
@JsonInclude(JsonInclude.Include.NON_NULL)
public class DescriptionResponse implements Serializable {
    private static final long serialVersionUID = 1L;
    @JsonProperty
    private int errorCode;
    @JsonProperty
    private String errorMessage;
    @JsonProperty
    private String descriptionResult;

    public DescriptionResponse() {
    }
    public void setErrorCode(int errorCode) {
        this.errorCode = errorCode;
    }
    public void setDescriptionResult(String descriptionResult) {
        this.descriptionResult = descriptionResult;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public static Builder responseBuilder(int errorCode, String errorMessage, String descriptionResult){
        return new Builder()
                .errorCode(errorCode)
                .errorMessage(errorMessage)
                .descriptionResult(descriptionResult);
    }

    public static class Builder{
        private int errorCode;
        private String errorMessage;
        private String descriptionResult;
        public Builder errorCode(int errorCode) {
            this.errorCode = errorCode;
            return this;
        }
        public Builder errorMessage(String errorMessage) {
            this.errorMessage = errorMessage;
            return this;
        }
        public Builder descriptionResult(String descriptionResult) {
            this.descriptionResult = descriptionResult;
            return this;
        }
        public DescriptionResponse build(){
            DescriptionResponse response = new DescriptionResponse();
            response.setErrorCode(this.errorCode);
            response.setErrorMessage(this.errorMessage);
            response.setDescriptionResult(this.descriptionResult);
            return response;
        }
    }
}
