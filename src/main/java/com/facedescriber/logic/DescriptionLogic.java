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

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

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
            String descriptionResult = runFaceDescriberPy(request);
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
        } catch (InterruptedException | IOException e) {
            logger.warn("Error "+BackendError.SCRIPT_FAILURE.getErrorCode()+": "+e.getMessage());
            return createResponse(
                    BackendError.SCRIPT_FAILURE.getErrorCode(),
                    "Script execution failed",
                    null
            );
        }
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

    private String runFaceDescriberPy(DescriptionRequest request) throws InterruptedException, IOException {
        String image = request.getImage();
        String language = request.getLanguage();
        ProcessBuilder processBuilder = new ProcessBuilder("python3", "RequestHandler.py", image, language);
        processBuilder.directory(new File("src/main/python"));
        processBuilder.redirectErrorStream(true);
        logger.info(
                String.format("Executing OS command: %s %s %s %s",
                        "python3",
                        "RequestHandler.py",
                        image,
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

