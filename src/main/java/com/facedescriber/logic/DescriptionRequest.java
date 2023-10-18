package com.facedescriber.logic;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

public class DescriptionRequest implements Serializable {
    private static final long serialVersionUID = 1L;
    @JsonProperty
    private String image;
    @JsonProperty
    private String language;

    public String getImage() {
        return image;
    }

    public String getLanguage() {
        return language;
    }
}
