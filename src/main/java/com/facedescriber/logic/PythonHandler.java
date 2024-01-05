package com.facedescriber.logic;

import com.facedescriber.constants.BackendError;
import com.facedescriber.validation.PythonException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

@Component
@Scope("request")
public class PythonHandler {
    private static Logger logger = LogManager.getLogger();

    @Autowired
    public PythonHandler(){}

    public String executeDescription(String fileName, String language) throws Exception {
        ProcessBuilder processBuilder = new ProcessBuilder("python3", "FaceDescriber.py", fileName, language);
        processBuilder.directory(new File("src/main/python"));
        processBuilder.redirectErrorStream(true);
        logger.info(
                String.format("Executing OS command: %s %s %s %s",
                        "python3",
                        "FaceDescriber.py",
                        fileName,
                        language)
        );
        Process process = processBuilder.start();
        int exitCode = process.waitFor();
        try(BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()))){
            if(exitCode == BackendError.PYTHON_ERROR.getErrorCode()) throw new PythonException(exitCode, br.lines().findFirst().get());

            if(exitCode == 0) return br.lines().findFirst().get(); //Expecting only 1 output line

            throw new Exception();
        }
    }
}
