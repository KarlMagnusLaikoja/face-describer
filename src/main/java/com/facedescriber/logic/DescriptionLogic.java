package com.facedescriber.logic;

import com.facedescriber.constants.BackendError;
import com.facedescriber.validation.InvalidBase64Exception;
import com.facedescriber.validation.MissingFieldException;
import com.facedescriber.validation.UnsupportedLanguageException;
import com.facedescriber.validation.image.ImageValidator;
import com.facedescriber.validation.json.JsonValidator;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.Base64;
import java.util.concurrent.ThreadLocalRandom;

@Component
public class DescriptionLogic {
    private String data;
    @Autowired
    private JsonValidator jsonValidator;
    @Autowired
    private ImageValidator imageValidator;
    @Autowired
    private DescriptionResponse response;
    private static Logger logger = LogManager.getLogger();

    private static ObjectMapper mapper = new ObjectMapper();
    public DescriptionLogic() {
    }

    public void setData(String data) {
        this.data = data;
    }

    public String execute(){
        logger.info("Starting DescriptionLogic with data: "+data);
        try{
            DescriptionRequest request = validate(data);
            String fileName = saveImage(request.getImage()); //Can't use base64 image directly because it can be too long. Need to save to a file instead.
            String descriptionResult = executeDescription(fileName, request.getLanguage());
            deleteImage(fileName);
            return createResponse(BackendError.OK.getErrorCode(), null, descriptionResult);
        } catch (MissingFieldException e) {
            logger.warn("Error "+BackendError.MISSING_FIELD.getErrorCode()+": "+e.getMessage());
            return createResponse(
                    BackendError.MISSING_FIELD.getErrorCode(),
                    e.getMessage(),
                    null
            );
        } catch (UnsupportedLanguageException e) {
            logger.warn("Error "+BackendError.UNSUPPORTED_LANGUAGE.getErrorCode()+": "+e.getMessage());
            return createResponse(
                    BackendError.UNSUPPORTED_LANGUAGE.getErrorCode(),
                    e.getMessage(),
                    null
            );
        }catch (InvalidBase64Exception e) {
            logger.warn("Error "+BackendError.INVALID_BASE64.getErrorCode()+": "+e.getMessage());
            return createResponse(
                    BackendError.INVALID_BASE64.getErrorCode(),
                    e.getMessage(),
                    null
            );
        } catch (JsonProcessingException e) {
            logger.warn("Error "+BackendError.INVALID_JSON.getErrorCode()+": "+e.getMessage());
            return createResponse(
                    BackendError.INVALID_JSON.getErrorCode(),
                    "Request body contains invalid JSON",
                    null
            );
        } catch (InterruptedException | IOException | IllegalArgumentException e) {
            logger.warn("Error "+BackendError.BACKEND_FAILURE.getErrorCode()+": "+e.getMessage());
            return createResponse(
                    BackendError.BACKEND_FAILURE.getErrorCode(),
                    "Backend execution of facial description failed",
                    null
            );
        }
    }

    private void deleteImage(String image) throws IOException {
        if(!new File(image).delete()){
            logger.error("Failed to delete temporary image: "+image);
            throw new IOException("Failed to delete temporary image: "+image);
        }
        logger.info("Successfully deleted "+image+" from disk");
}

    private String saveImage(String image) throws IOException, IllegalArgumentException {
        String fileName = ThreadLocalRandom.current().nextInt()+".png";

        //Don't need the data:... part
        image = image.split(",")[1];

        try (OutputStream out = new FileOutputStream(fileName)){
            out.write(Base64.getDecoder().decode(image));
        }

        logger.info("Successfully saved "+fileName+" to disk");
        throw new IOException();
        //return fileName;
    }

    private String createResponse(int errorCode, String errorMessage, String descriptionResult) {
        try {
            return mapper.writeValueAsString(
                    DescriptionResponse.responseBuilder(
                            errorCode,
                            errorMessage,
                            descriptionResult
                    ).build()
            );
        } catch (JsonProcessingException e) {
            logger.error("Response creation failed: "+e.getMessage());
            throw new RuntimeException(e);
        }
    }

    private DescriptionRequest validate(String data) throws MissingFieldException, JsonProcessingException, InvalidBase64Exception, UnsupportedLanguageException {
        logger.info("Validating request against schema");
        DescriptionRequest request = jsonValidator.validate(data);
        logger.info("Validating base64 image");
        imageValidator.validate(request);
        return request;
    }

    private String executeDescription(String fileName, String language) throws InterruptedException, IOException {
        ProcessBuilder processBuilder = new ProcessBuilder("python3", "RequestHandler.py", fileName, language);
        processBuilder.directory(new File("src/main/python"));
        processBuilder.redirectErrorStream(true);
        logger.info(
                String.format("Executing OS command: %s %s %s %s",
                        "python3",
                        "RequestHandler.py",
                        fileName,
                        language)
        );
        Process process = processBuilder.start();
        int exitCode = process.waitFor();
        if(exitCode != 0) throw new IOException("Python execution exited with code "+exitCode);
        try(BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()))){
            return br.lines().findFirst().get(); //Expecting only 1 output line
        }
    }
}

