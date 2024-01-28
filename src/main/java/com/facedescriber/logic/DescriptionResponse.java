package com.facedescriber.logic;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
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
    private JSONObject description;

    public DescriptionResponse() {
    }
    public void setErrorCode(int errorCode) {
        this.errorCode = errorCode;
    }
    public void setDescription(JSONObject description) {
        this.description = description;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public static Builder responseBuilder(int errorCode, String errorMessage, String descriptionResult) throws ParseException {
        return new Builder()
                .errorCode(errorCode)
                .errorMessage(errorMessage)
                .descriptionResult(descriptionResult);
    }

    public static class Builder{
        private static JSONParser parser = new JSONParser();
        private int errorCode;
        private String errorMessage;
        private JSONObject descriptionResult;
        public Builder errorCode(int errorCode) {
            this.errorCode = errorCode;
            return this;
        }
        public Builder errorMessage(String errorMessage) {
            this.errorMessage = errorMessage;
            return this;
        }
        public Builder descriptionResult(String descriptionResult) throws ParseException {
            if(descriptionResult == null) return this;
            this.descriptionResult = (JSONObject)
                    parser.parse(
                            descriptionResult.replace("\'", "\"")
                    );
            return this;
        }
        public DescriptionResponse build(){
            DescriptionResponse response = new DescriptionResponse();
            response.setErrorCode(this.errorCode);
            response.setErrorMessage(this.errorMessage);
            response.setDescription(this.descriptionResult);
            return response;
        }
    }
}
