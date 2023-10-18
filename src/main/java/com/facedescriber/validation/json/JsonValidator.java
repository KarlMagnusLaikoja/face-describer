package com.facedescriber.validation.json;

import com.facedescriber.logic.DescriptionRequest;
import com.facedescriber.validation.MissingFieldException;
import com.facedescriber.validation.UnsupportedLanguageException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.networknt.schema.JsonSchema;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion;
import com.networknt.schema.ValidationMessage;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Set;

@Configuration
public class JsonValidator {
    private static ObjectMapper objectMapper = new ObjectMapper();

    @Bean
    public JsonValidator getJsonValidator(){
        return new JsonValidator();
    }

    public DescriptionRequest validate(String json) throws JsonProcessingException, MissingFieldException, UnsupportedLanguageException {
        JsonSchema schema = findSchema("schema.json");
        JsonNode node = objectMapper.readTree(json);
        Set<ValidationMessage> errors = schema.validate(node);


        for (ValidationMessage validationMessage : errors.stream().toList()) {
            if(validationMessage.getMessage().contains("is missing but it is required"))
                throw new MissingFieldException("Request is missing required field \""+validationMessage.getMessage().split(": ")[0].substring(2)+"\"");
            if(validationMessage.getMessage().contains("language: does not have a value in the enumeration"))
                throw new UnsupportedLanguageException("Language \""+node.get("language").asText()+"\" is not supported.");
        }
        return objectMapper.treeToValue(node, DescriptionRequest.class);
    }


    private JsonSchema findSchema(String schema) {
        JsonSchemaFactory factory = JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V7);
        return factory.getSchema(
                Thread.currentThread().getContextClassLoader().getResourceAsStream(schema)
        );
    }



}
