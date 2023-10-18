package com.facedescriber.validation.image;

import com.facedescriber.logic.DescriptionRequest;
import com.facedescriber.validation.InvalidBase64Exception;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ImageValidator {
    @Bean
    public ImageValidator getImageValidator(){
        return new ImageValidator();
    }

    public void validate(DescriptionRequest request) throws InvalidBase64Exception {

        //should filter out possible command injection when passing input to python
        if(!request.getImage().matches("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")) throw new InvalidBase64Exception("Provided image is not base64");


    }

}
